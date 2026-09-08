# Standalone study packaging audit — 2026-09-08

The first goal turn completed implementation, studies, review and local package
verification: progress. The next completion audit found a remaining distribution
gap. The complete archive has the required dependencies, but the separate
robustness study archive lacks source files hashed by rerun.py and the frozen
policy selection read by appendix.py. The documented standalone main command was
executed from that extracted archive and failed with FileNotFoundError before
simulation. Its input, partial attempt and error remain in runs/package-replay-audit.

Packaging revision 2 includes source files in each study archive and the frozen
cross-study selection/preregistration in robustness. Application RC4, numerical
functions, study inputs, scientific conclusions and prior evidence are unchanged.
Original archives and checksums are retained. Historical investigator/model labels
in replay scripts identify the original investigation, not the current operator;
new replay Python/platform identity is recorded separately.

Finite validation: extract each revised standalone archive in a project-local
fresh directory, run its documented primary and bridge commands sequentially,
compare all policy records against the corresponding originals, and retain exit
codes, actual costs and failures. This is distribution reproduction on the same
host, not additional independent scientific samples or external human evidence.
At most 53 benchmark, 38 policy and 62 robustness replay scenarios; <=300 CPU
seconds per study, no parallel solver jobs. No publication or participant contact.

## Observed result

All seven documented script invocations passed from the revised standalone archives.
Benchmark: 53 scenarios/59 policy records; policies: 38/396; robustness: 62/260.
All 715 raw-plus-evaluation records are byte-identical to the original archived
records. Total measured replay CPU: 42.189954 seconds, sequential
subprocesses in a clean venv/environment on the same host. This does not establish
external human first-use or qualified engineering review. Final record:
releases/v1.0.0rc4-review-r2/PACKAGING-REPLAY.json; complete commands, comparisons
and original failure: packaging-replay-evidence.zip in that directory.

Current proposed release assets are packaging revision 2. RC4 application hash is
unchanged; previous archives remain retained. Public release, external first-use
and qualified review still have no completion evidence or new owner authorization.
