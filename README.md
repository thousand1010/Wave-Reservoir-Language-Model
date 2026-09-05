# Wave Reservoir Language Model (WRLM)

WRLM is a research prototype for studying whether driven nonlinear wave fields
can provide useful state, memory, and interaction features for
language-oriented sequence models. The project is at the substrate-validation
stage; this repository does not claim a working language model or an advantage
over Transformers or other reservoir computers.

This public portfolio contains selected, reviewable exports from a separate
private research lab. It starts with one deterministic diagnostic: Kerr
nonlinearity in a discrete nonlinear Schrödinger (DNLS) field generates the
four-wave-mixing (FWM) modes predicted from the injected modes, while the
linear control keeps those modes at numerical zero.

## Quick start

Python 3.11 is used in CI.

```bash
python -m venv .venv
python -m pip install -r requirements.txt
python examples/wave_field_demo.py
python experiments/gate-nl/reproduce.py --check-reference
python -m unittest discover -s tests -v
```

The example is a `smoke-demo`. The reproduction command is a
`full-reproduction` of the complete public Gate NL diagnostic. It uses no
training data, learned parameters, or random experimental seeds. Floating
point values are compared with documented tolerances; the decision thresholds
are the primary reproducibility contract.

## What the result supports

Gate NL is a **diagnostic** result. It supports the narrow claim that this DNLS
implementation contains a nonlinear FWM primitive under the published
configuration. It does not establish language-model performance, end-to-end
utility, or a wave-specific advantage over other nonlinear reservoirs.

See [the experiment narrative](experiments/gate-nl/README.md),
[the theory note](docs/theory.md), and [the experiment index](docs/experiments.md).

## Artifacts

Large or learned artifacts are assigned to
[Hugging Face](https://huggingface.co/Thousand1010/Wave-Reservoir-Language-Model).
The model repository remains private while no reviewed weights are ready for
release. This GitHub repository contains only source, compact configuration,
and small result records.

## Development and disclosure

The public history is curated independently from the private lab history.
AI assistants contributed to implementation, documentation, and review; the
human owner selected the research direction, publication scope, and claims.
Published results remain tied to runnable code and saved outputs.

## License

Code is available under the [MIT License](LICENSE). Artifact licenses are
declared separately on Hugging Face when artifacts are released.
