from __future__ import annotations

import json
import unittest
from pathlib import Path

import numpy as np

from wrlm import DNLSField, evaluate_gate_nl, new_fwm_modes


ROOT = Path(__file__).resolve().parents[1]


class TestFwmDiagnostic(unittest.TestCase):
    def test_predicted_modes_exclude_inputs_and_dc(self) -> None:
        modes = [3, 7]
        predicted = new_fwm_modes(modes, 64)
        self.assertTrue(predicted)
        self.assertTrue(set(predicted).isdisjoint({0, *modes}))

    def test_linear_step_is_finite_and_damped(self) -> None:
        field = DNLSField(n_sites=16, gamma=0.0, alpha=0.05, dt=0.05)
        state = field.random_state()
        initial_energy = np.sum(np.abs(state) ** 2)
        final = field.step(state)
        self.assertTrue(np.all(np.isfinite(final)))
        self.assertLess(np.sum(np.abs(final) ** 2), initial_energy)

    def test_full_gate_contract(self) -> None:
        config_path = ROOT / "experiments" / "gate-nl" / "configs" / "full.json"
        config = json.loads(config_path.read_text(encoding="utf-8"))
        result = evaluate_gate_nl(config)
        self.assertTrue(result["overall_pass"])
        for case in result["cases"]:
            self.assertLess(
                case["gamma_results"]["0"]["new_mode_energy"],
                config["thresholds"]["linear_new_energy_max"],
            )
            self.assertGreaterEqual(
                case["nonlinear_max_fraction"],
                config["thresholds"]["nonlinear_new_fraction_min"],
            )
            self.assertTrue(case["dt_halving"]["passed"])


if __name__ == "__main__":
    unittest.main()
