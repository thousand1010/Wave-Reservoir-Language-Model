"""Diagnostics for nonlinear mode generation and finite-time stability."""

from __future__ import annotations

from typing import Any, Iterable

import numpy as np

from .field import DNLSField


def new_fwm_modes(modes: Iterable[int], n_sites: int) -> list[int]:
    """Return cubic-mixing modes k_i + k_j - k_l outside input modes and DC."""

    modes = list(modes)
    input_set = {mode % n_sites for mode in modes} | {0}
    output = set()
    for mode_i in modes:
        for mode_j in modes:
            for mode_l in modes:
                candidate = (mode_i + mode_j - mode_l) % n_sites
                if candidate not in input_set:
                    output.add(candidate)
    return sorted(output)


def initial_mode_state(n_sites: int, modes: Iterable[int], amplitude: float) -> np.ndarray:
    positions = np.arange(n_sites)
    return sum(
        amplitude * np.exp(1j * 2.0 * np.pi * mode * positions / n_sites)
        for mode in modes
    )


def run_fwm_case(
    n_sites: int,
    modes: Iterable[int],
    gamma: float,
    amplitude: float = 0.8,
    steps: int = 60,
    dt: float = 0.05,
    alpha: float = 0.05,
) -> tuple[np.ndarray, float]:
    """Evolve input Fourier modes and return final spectral energy and peak state."""

    field = DNLSField(n_sites=n_sites, gamma=gamma, alpha=alpha, dt=dt)
    state = initial_mode_state(n_sites, modes, amplitude)
    peak_amplitude = float(np.abs(state).max())
    for _ in range(steps):
        state = field.step(state)
        peak_amplitude = max(peak_amplitude, float(np.abs(state).max()))
    spectrum = np.abs(np.fft.fft(state)) ** 2
    return spectrum, peak_amplitude


def finite_time_stability(
    field: DNLSField,
    drive_sequence: list[np.ndarray | None],
    initial_scale: float = 1.0,
    perturbation: float = 1e-4,
    esp_rate_tolerance: float = 1e-3,
    lyapunov_threshold: float = 1.0,
) -> dict[str, float | bool]:
    """Return the same finite-time Gate S reference metrics as the lab source."""

    state_a = field.random_state(initial_scale)
    state_b = field.random_state(initial_scale)
    state_c = state_a + perturbation * field.random_state(1.0)
    initial_distance = np.linalg.norm(state_a - state_b)
    initial_perturbation = np.linalg.norm(state_a - state_c)
    distances = np.empty(len(drive_sequence))
    perturbations = np.empty(len(drive_sequence))
    energies = np.empty(len(drive_sequence))

    for index, drive in enumerate(drive_sequence):
        state_a = field.step(state_a, drive)
        state_b = field.step(state_b, drive)
        state_c = field.step(state_c, drive)
        distances[index] = np.linalg.norm(state_a - state_b)
        perturbations[index] = np.linalg.norm(state_a - state_c)
        energies[index] = np.sum(np.abs(state_a) ** 2)

    duration = max(len(drive_sequence) * field.dt, 1e-9)
    esp_ratio = float(distances[-1] / (initial_distance + 1e-12))
    esp_rate = float(
        np.log((distances[-1] + 1e-12) / (initial_distance + 1e-12)) / duration
    )
    finite_time_lyapunov = float(
        np.log(
            (perturbations[-1] + 1e-12) / (initial_perturbation + 1e-12)
        )
        / duration
    )
    bounded = bool(np.all(np.isfinite(energies)) and energies.max() < 1e6)
    esp_ok = bool(esp_rate < -esp_rate_tolerance)
    usable = bool(bounded and esp_ok and finite_time_lyapunov < lyapunov_threshold)
    return {
        "esp_ratio": esp_ratio,
        "esp_rate": esp_rate,
        "esp_ok": esp_ok,
        "finite_time_lyapunov": finite_time_lyapunov,
        "energy_max": float(energies.max()),
        "energy_final": float(energies[-1]),
        "bounded": bounded,
        "usable": usable,
    }


def evaluate_gate_nl(config: dict[str, Any]) -> dict[str, Any]:
    """Run the complete public Gate NL diagnostic from a JSON-compatible config."""

    n_sites = int(config["n_sites"])
    amplitude = float(config["amplitude"])
    steps = int(config["steps"])
    dt = float(config["dt"])
    alpha = float(config["alpha"])
    gammas = [float(value) for value in config["gammas"]]
    thresholds = config["thresholds"]
    cases = []

    for mode_list in config["mode_sets"]:
        modes = [int(value) for value in mode_list]
        predicted = new_fwm_modes(modes, n_sites)
        initial_state = initial_mode_state(n_sites, modes, amplitude)
        representative_drive = [initial_state] * 5 + [None] * 45
        gamma_results: dict[str, Any] = {}

        for gamma in gammas:
            spectrum, peak_amplitude = run_fwm_case(
                n_sites=n_sites,
                modes=modes,
                gamma=gamma,
                amplitude=amplitude,
                steps=steps,
                dt=dt,
                alpha=alpha,
            )
            new_energy = float(sum(spectrum[index] for index in predicted))
            input_energy = float(sum(spectrum[index % n_sites] for index in modes))
            new_fraction = new_energy / (input_energy + 1e-18)
            stability = finite_time_stability(
                DNLSField(
                    n_sites=n_sites,
                    gamma=gamma,
                    alpha=alpha,
                    dt=dt,
                    seed=0,
                ),
                representative_drive,
            )
            gamma_results[f"{gamma:g}"] = {
                "new_mode_energy": new_energy,
                "input_mode_energy": input_energy,
                "new_to_input_fraction": new_fraction,
                "peak_amplitude": peak_amplitude,
                "stability_reference": stability,
            }

        spectrum_dt, _ = run_fwm_case(
            n_sites=n_sites,
            modes=modes,
            gamma=-1.0,
            amplitude=amplitude,
            steps=steps,
            dt=dt,
            alpha=alpha,
        )
        spectrum_half_dt, _ = run_fwm_case(
            n_sites=n_sites,
            modes=modes,
            gamma=-1.0,
            amplitude=amplitude,
            steps=2 * steps,
            dt=dt / 2.0,
            alpha=alpha,
        )
        energy_dt = float(sum(spectrum_dt[index] for index in predicted))
        energy_half_dt = float(sum(spectrum_half_dt[index] for index in predicted))
        dt_ratio = energy_half_dt / (energy_dt + 1e-18)

        linear_energy = gamma_results["0"]["new_mode_energy"]
        nonlinear_max_fraction = max(
            gamma_results[f"{gamma:g}"]["new_to_input_fraction"]
            for gamma in gammas
            if gamma != 0.0
        )
        dt_ok = bool(
            thresholds["dt_ratio_min"] <= dt_ratio <= thresholds["dt_ratio_max"]
        )
        passed = bool(
            linear_energy < thresholds["linear_new_energy_max"]
            and nonlinear_max_fraction >= thresholds["nonlinear_new_fraction_min"]
            and dt_ok
        )
        cases.append(
            {
                "input_modes": modes,
                "predicted_new_modes": predicted,
                "gamma_results": gamma_results,
                "dt_halving": {
                    "new_mode_energy_dt": energy_dt,
                    "new_mode_energy_half_dt": energy_half_dt,
                    "ratio": dt_ratio,
                    "passed": dt_ok,
                },
                "nonlinear_max_fraction": nonlinear_max_fraction,
                "passed": passed,
            }
        )

    return {
        "schema_version": 1,
        "evidence_class": "diagnostic",
        "reproduction_tier": "full-reproduction",
        "source_lab_commit": config["source_lab_commit"],
        "config": config,
        "cases": cases,
        "overall_pass": bool(all(case["passed"] for case in cases)),
    }
