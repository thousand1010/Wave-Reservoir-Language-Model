"""Small smoke demo: contrast linear and nonlinear generation of FWM modes."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from wrlm import new_fwm_modes, run_fwm_case  # noqa: E402


def main() -> None:
    n_sites = 32
    modes = [3, 7]
    predicted = new_fwm_modes(modes, n_sites)
    rows = []
    for gamma in (0.0, -1.0):
        spectrum, _ = run_fwm_case(
            n_sites=n_sites,
            modes=modes,
            gamma=gamma,
            steps=20,
        )
        new_energy = float(sum(spectrum[index] for index in predicted))
        rows.append((gamma, new_energy))
        print(f"gamma={gamma:>4g} predicted-new-mode energy={new_energy:.6e}")
    if not (rows[0][1] < 1e-12 and rows[1][1] > rows[0][1]):
        raise SystemExit("smoke diagnostic failed")


if __name__ == "__main__":
    main()
