"""Reproduce the public Gate NL diagnostic and optionally check its reference."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from wrlm import evaluate_gate_nl  # noqa: E402

EXPERIMENT_DIR = Path(__file__).resolve().parent
DEFAULT_CONFIG = EXPERIMENT_DIR / "configs" / "full.json"
DEFAULT_REFERENCE = EXPERIMENT_DIR / "results" / "reference.json"


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def compare_reference(
    actual: Any,
    expected: Any,
    relative_tolerance: float,
    absolute_tolerance: float,
    location: str = "result",
) -> list[str]:
    """Compare nested JSON values, using tolerances only for finite numbers."""

    errors: list[str] = []
    if isinstance(actual, bool) or isinstance(expected, bool):
        if actual is not expected:
            errors.append(f"{location}: expected {expected!r}, got {actual!r}")
    elif isinstance(actual, (int, float)) and isinstance(expected, (int, float)):
        if not math.isfinite(float(actual)) or not math.isfinite(float(expected)):
            errors.append(f"{location}: non-finite number")
        elif not math.isclose(
            float(actual),
            float(expected),
            rel_tol=relative_tolerance,
            abs_tol=absolute_tolerance,
        ):
            errors.append(f"{location}: expected {expected!r}, got {actual!r}")
    elif isinstance(actual, dict) and isinstance(expected, dict):
        if actual.keys() != expected.keys():
            errors.append(
                f"{location}: key mismatch expected={sorted(expected)} got={sorted(actual)}"
            )
        else:
            for key in actual:
                errors.extend(
                    compare_reference(
                        actual[key],
                        expected[key],
                        relative_tolerance,
                        absolute_tolerance,
                        f"{location}.{key}",
                    )
                )
    elif isinstance(actual, list) and isinstance(expected, list):
        if len(actual) != len(expected):
            errors.append(
                f"{location}: length mismatch expected={len(expected)} got={len(actual)}"
            )
        else:
            for index, (actual_item, expected_item) in enumerate(zip(actual, expected)):
                errors.extend(
                    compare_reference(
                        actual_item,
                        expected_item,
                        relative_tolerance,
                        absolute_tolerance,
                        f"{location}[{index}]",
                    )
                )
    elif actual != expected:
        errors.append(f"{location}: expected {expected!r}, got {actual!r}")
    return errors


def validate_contract(result: dict[str, Any]) -> list[str]:
    """Check scientific decision invariants independently of reference values."""

    errors: list[str] = []
    thresholds = result["config"]["thresholds"]
    for index, case in enumerate(result["cases"]):
        linear_energy = case["gamma_results"]["0"]["new_mode_energy"]
        if linear_energy >= thresholds["linear_new_energy_max"]:
            errors.append(f"case {index}: linear control generated excess new-mode energy")
        if case["nonlinear_max_fraction"] < thresholds["nonlinear_new_fraction_min"]:
            errors.append(f"case {index}: nonlinear new-mode fraction is below threshold")
        if not case["dt_halving"]["passed"]:
            errors.append(f"case {index}: dt-halving stability is outside threshold")
        if not case["passed"]:
            errors.append(f"case {index}: diagnostic verdict failed")
    if not result["overall_pass"]:
        errors.append("overall diagnostic verdict failed")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check-reference", action="store_true")
    parser.add_argument("--reference", type=Path, default=DEFAULT_REFERENCE)
    args = parser.parse_args()

    config = load_json(args.config)
    result = evaluate_gate_nl(config)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")

    errors = validate_contract(result)
    if args.check_reference:
        expected = load_json(args.reference)
        tolerance = config["reference_tolerances"]
        errors.extend(
            compare_reference(
                result,
                expected,
                relative_tolerance=float(tolerance["relative"]),
                absolute_tolerance=float(tolerance["absolute"]),
            )
        )
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
