# Launch draft — not published

## Proposed GitHub release title

Grid Horizons 1.0.0rc4 — a bounded, reproducible feeder laboratory

## English launch copy

Grid Horizons is an offline laboratory for exploring a synthetic distribution
feeder day. Run balanced AC calculations, compare chronological storage and ideal
source-tap schedules, inspect voltage/current/storage constraints, and export a
complete study that can be reopened with the same build.

Its first three computational studies test numerical validity, policy tradeoffs
and robustness. They retain unfavorable results: solver convergence can fail
independent equation checks; lower line loss can be outweighed by storage
conversion loss; and a policy that restores nominal feasibility can lose it
under changed operating assumptions. Reports distinguish these observations
from broader physical claims.

The Python package has no third-party runtime dependencies or private account
requirement. A browser opens its offline workbench. Supported and tested resources:
Linux x86_64 with CPython 3.12; browser details, measured costs and reproduction
instructions accompany the exact release artifacts.

This release uses original synthetic data and a declared balanced constant-PQ
model. It does not model unbalanced operation, thermal/degradation behavior,
physical tap-changing dynamics or outage restoration. It does not provide
real-grid dispatch, certification or deployment advice. Agent checks are not
human or institutional validation; the release notes state review status.

Repository: [Grid Horizons on GitHub](https://github.com/thepianistdirector/grid-horizons)
Project and contributor coordination: [Grid Horizons on Tanduna](https://tanduna.com/projects/grid-horizons)

Contributors can reproduce the studies, admit a lawful public feeder with source
observables, improve keyboard/screen-reader access, test external first use, or
independently justify a richer model. Each extension needs explicit provenance,
reference checks, failures and limits. Original code/data are AGPL-3.0-only.

## Publication state

This is prepared English copy. It has not been posted, submitted or adopted.
Exact release asset hashes, review gates and destinations belong to RELEASE-REVIEW.md.
