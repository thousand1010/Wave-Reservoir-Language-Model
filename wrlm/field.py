"""Driven, damped one-dimensional discrete nonlinear Schrödinger field.

The state follows

    i dpsi_n/dt = -C D2 psi_n + gamma |psi_n|^2 psi_n
                  - i alpha_n psi_n + V_n psi_n + drive_n(t).

The implementation uses Strang splitting: a Fourier-space dispersion half
step, a real-space damping/nonlinear/potential step, optional drive injection,
and a second dispersion half step. Periodic boundaries follow from the FFT.

Public provenance: ported from the private lab at commit
4da14c1cf702e5785655ebe35c101bff6adc25d9.
"""

from __future__ import annotations

import numpy as np


class DNLSField:
    """A small NumPy DNLS field used by the public diagnostics."""

    def __init__(
        self,
        n_sites: int = 64,
        coupling: float = 1.0,
        gamma: float = 0.5,
        alpha: float | np.ndarray = 0.05,
        potential: np.ndarray | None = None,
        dt: float = 0.05,
        seed: int = 0,
    ) -> None:
        self.n_sites = int(n_sites)
        self.coupling = float(coupling)
        self.gamma = float(gamma)
        self.dt = float(dt)
        self.alpha = (
            np.full(self.n_sites, float(alpha))
            if np.isscalar(alpha)
            else np.asarray(alpha, dtype=float)
        )
        self.potential = (
            np.zeros(self.n_sites)
            if potential is None
            else np.asarray(potential, dtype=float)
        )
        if self.alpha.shape != (self.n_sites,):
            raise ValueError("alpha must be scalar or have shape (n_sites,)")
        if self.potential.shape != (self.n_sites,):
            raise ValueError("potential must have shape (n_sites,)")

        wave_number = 2.0 * np.pi * np.fft.fftfreq(self.n_sites)
        laplacian = 2.0 * np.cos(wave_number) - 2.0
        self._dispersion_half_phase = np.exp(
            1j * self.coupling * laplacian * (self.dt / 2.0)
        )
        self.rng = np.random.default_rng(seed)

    def zero_state(self) -> np.ndarray:
        return np.zeros(self.n_sites, dtype=complex)

    def random_state(self, scale: float = 1.0) -> np.ndarray:
        state = self.rng.standard_normal(self.n_sites) + 1j * self.rng.standard_normal(
            self.n_sites
        )
        return scale * state / np.sqrt(2.0)

    def _dispersion_half(self, state: np.ndarray) -> np.ndarray:
        spectrum = np.fft.fft(state, axis=-1)
        return np.fft.ifft(
            spectrum * self._dispersion_half_phase,
            axis=-1,
        )

    def step(self, state: np.ndarray, drive: np.ndarray | None = None) -> np.ndarray:
        """Advance one split-step integration interval."""

        state = self._dispersion_half(state)
        state = state * np.exp(-self.alpha * self.dt)
        phase = self.gamma * np.abs(state) ** 2 + self.potential
        state = state * np.exp(-1j * phase * self.dt)
        if drive is not None:
            state = state + (-1j) * drive * self.dt
        return self._dispersion_half(state)
