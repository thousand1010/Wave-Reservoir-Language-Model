# Public Repository Guidelines

This repository is the curated public portfolio for WRLM. Keep it runnable,
small, and understandable without access to the private lab. Do not copy the
lab history or bulk-export lab files.

Every experiment must declare its evidence class (`confirmatory`,
`exploratory`, or `diagnostic`), reproduction tier, exact configuration,
commands, compact results, limitations, and source provenance. A successful
primitive diagnostic does not authorize a system-level or mechanism claim.

Use topic branches and pull requests. Keep `main` runnable, require the public
smoke check, and use squash merges. Never commit credentials, private paths,
raw large runs, model weights, data dumps, or agent state. Large learned
artifacts belong in the paired Hugging Face repository after review.

AI assistance must be disclosed in public documentation. The human owner is
responsible for publication decisions and claims.
