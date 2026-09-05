# Gate NL: four-wave-mixing primitive diagnostic

## Question and classification

Does the cubic Kerr term in the published DNLS implementation generate the
new Fourier modes predicted by four-wave mixing, while a linear control does
not?

- Evidence class: `diagnostic`
- Reproduction tier: `full-reproduction`
- Source lab commit: `4da14c1cf702e5785655ebe35c101bff6adc25d9`
- Training/data: none
- Random experimental seeds: none

## Method

The diagnostic initializes a periodic 64-site field with mode sets `[3, 7]`
and `[3, 7, 11]`. It evolves each state for 60 steps at `dt=0.05`,
`alpha=0.05`, and amplitude `0.8`, comparing `gamma=0` with three nonlinear
settings. It measures final state energy at cubic-mixing modes
`k_i + k_j - k_l` that are absent from the input. A second nonlinear run halves
`dt` and doubles the step count to hold simulated time fixed.

The pass contract is fixed in [`configs/full.json`](configs/full.json):

1. linear new-mode energy is below `1e-12`;
2. at least one nonlinear setting has new/input mode energy ratio at least
   `0.01`;
3. the new-mode energy ratio after halving `dt` lies in `[0.8, 1.25]`.

Gate S finite-time stability values are included as reference measurements,
matching the original diagnostic. They do not replace a stability evaluation
for a learned end-to-end system.

## Reproduce

From the repository root:

```bash
python -m pip install -r requirements.txt
python experiments/gate-nl/reproduce.py --check-reference
```

The command reruns every public case, checks the decision contract, and
compares the output with [`results/reference.json`](results/reference.json).
Numeric comparison uses `relative=1e-8` and `absolute=1e-12`; exact JSON byte
equality is not required across platforms.

## Result and limits

The fixed public cases pass: the linear control remains below the numerical
zero threshold, nonlinear runs create the predicted modes, and the result is
stable to halving the integration step.

This supports a narrow implementation-level FWM claim. It does not demonstrate
language-model behavior, useful recall, sample efficiency, or superiority over
another nonlinear reservoir. During selection, a separate matched-reader lab
comparison found that an echo-state network reproduced the downstream
degree-parity effect with much better sample efficiency. That comparison is not
reproduced by this package, so it is stated only as a claim boundary and not as
publicly reproducible evidence here.

AI assistants helped port, document, and review this public package. The human
owner selected the experiment and approved the publication scope and claims.
