# Selected-policy transfer and RC2 bridge, declared 2026-09-08

Declared before reading robustness confirmation outputs. The original 48-case
study and its fixed example schedules remain unchanged. An external investigator
selected policies using only seeds 11/13 and load scales 0.7/0.85; the immutable
input selection will be copied and hashed from `research/policies/selection.json`.
Those are finite-grid winners among tested active schedules, not universal optima.

Test all four selected schedules (storage_loss, combined_loss, storage_peak,
combined_peak) against idle, with no tuning: loss schedules charge 2 kW 10–14 h,
discharge 1.805 kW 17–21 h; peak schedules charge 8 kW 9–13 h, discharge 7.22 kW
17–21 h. Combined schedules have constant tap +4; storage schedules tap zero.
Cross the same held-out seeds 101/103/107/109 with nominal, load_late (+3 h), and
joint_adverse (exact original definition): 12 scenarios × 5 policies. The three
treatments test nominal transfer, time mismatch, and compound physical stress;
they were selected without examining robustness outcomes. Use the same metrics,
feasibility gates, practical thresholds and finite-range reporting as the main
preregistration. No population inference. Report both successes and reversals.

Use frozen RC2 implementation
`3f46ec88b717c2811186fe2c4c7f2c926a37e110281c115798720bd87e143023`.
RC2 addresses the RC1 1 MiB reader failure; solver/evaluator source identity will
be checked by comparing archive member hashes. Re-run one original nominal RC1
scenario with RC2 and require exact policy raw/evaluation JSON equality as a
bridge. Preserve RC1 outputs and all reader failures. Combined budget: original
48 cases + one repeat + one rejected outage + 12 appendix cases + one RC2 bridge
= 63 scenario attempts, below 100; at most 96 intervals and 300 measured CPU
seconds total. One sequential producer process on one CPU. Primary outputs are
the real packaged CLI campaign/run/verify; no solver imports or bypass.
