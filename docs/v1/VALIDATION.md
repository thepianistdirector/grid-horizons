# v1.0 validation ledger

This ledger distinguishes tests from claims. Root source tests: 67 preserved
legacy tests passed; seven added AC tests passed (analytic/no-load controls,
independent mutation rejection, infeasible storage without clipping, cancellation,
nonconvergence, invalid input and study archive round trip). Exact integrated
candidate checks are retained under runs/ and referenced by final release status.

RC1 browser: 22 automated assertions passed in HeadlessChrome 140.0.7339.186,
using the real packaged report. Desktop 1440×1000 and phone 390×844 screenshots
were visually inspected; narrow 320px and 720px reflow proxy were also captured.
No horizontal document overflow. Keyboard skip link, policy selector, interval
slider, failure disclosure and exact scenario export were exercised. No browser
runtime or console errors. The large comparison table intentionally scrolls.
The 720px viewport at DPR2 is a reflow proxy, not actual browser UI zoom.

The agent-browser CLI is unavailable on this host. The existing project-local
Chromium/CDP QA path was reused with its sandbox enabled and original local
libraries; no host package or shared setting was changed. QA does not establish
screen-reader compatibility, formal WCAG conformance, physical device testing,
or external-human first-use. Browser export opens exact JSON in the tested
file context; forced save-to-disk is browser-dependent.

RC1 retained path: runs/browser-ac-rc1/results.json. Source/image hashes and
browser version are in that record. RC1 product smoke: runs/rc1-study.
An observed decoder size defect (legacy 1 MiB limit applied to v2 campaigns)
is fixed for the next candidate with an explicit 64 MiB bounded reader.
The old candidate and its investigators' attempts remain retained.

Clean packaged verification uses a new venv without pip, a fresh directory,
Python isolated mode and an environment without private credentials. It remains
on the same Linux host: not a container, second physical machine, or real person.
The full script exercises install-free run, verification, archive reopen,
byte-identical raw rerun, bad inputs, nonconvergence, cancellation/resume,
interrupted-manifest recovery, corruption, a >1 MiB campaign and legacy workflow.
See tools/check_release.py and its actual result.json for measured cost.

Separate skeptical review identified an RC2 custom-policy filename collision:
`summary`, `scenario`, `manifest`, or `checksums` passed validation but collided
with study metadata. RC3 will reject those identifiers before creating a study.
The four-name rejection and ordinary custom-name success have regression tests;
the original RC2 failure remains under research/reproduction. Scientific policy
identifiers are unaffected. Later-candidate bridges must still confirm equality.

Root planning regressions initially exposed test-fixture drift after status
reconciliation: ignored runs/ evidence was absent in disposable copies, and an
unfinished-prerequisite probe assumed a task was still PLANNED. Evidence snapshots
now live in docs/v1/evidence; fixtures copy only referenced small research artifacts,
and the negative probe explicitly sets its prerequisite unfinished. All 34 plan
regressions then passed, including rejection of fabricated evidence and status
advancing beyond prerequisites. The 255-task canonical ledger preserves original
identities/contracts while adding the bounded v1.0 waves.

RC3 complete clean-venv check: 20 recorded commands, 2.743 s wall time,
40,320 KiB maximum child RSS on the shared Linux x86_64 host. The workload
includes a 37-case campaign (one rejected input), not just a single solve.
No runtime package was installed; Python used isolated mode and no credential
environment. RC3 browser: 22 assertions pass; current desktop screenshot visually
inspected. Durable snapshots: evidence/rc3-clean.json and evidence/rc3-browser.json.
Current app SHA-256: 64ffa6a61548d212438506747c0ad194f4d2c71ec960cf23ec30730bf5bcdee7.

## Final RC4 local acceptance

75 runtime tests and 34 plan regressions pass. The final clean packaged test
executes 22 commands, including a 38-case campaign with two retained rejected
inputs, huge-integer structured rejection, archive round trip, exact numerical
rerun, interruption recovery, corruption detection and legacy calculation.
Measured 2.915 s wall, 40,912 KiB max child RSS. Browser 22/22 assertions pass.
Durable logs/snapshots are in docs/v1/evidence; complete QA commands and raw
example/failure bundles accompany the review package.

The skeptical agent reviewed 153 retained study bundles, 827 claim/table checks,
20 bounded run attempts, 1,224 second-solver intervals and the input-defect fixes.
All three research verdicts are SUPPORTED_WITH_BOUNDED_SCOPE. RC4 final identity:
implementation b2eeb117a34ea3423136a0082442d1b93f01b0c6e13dab429772a0d2c3a8f8e3;
zipapp 15aaa7913e4069b9483fcb721032c812a8babc865968d652bb681f031abc7c6e.
RC4 sample policy records match RC1 byte-for-byte; current application source
members match the frozen RC4 archive exactly. The producer/evaluator functions
were unchanged by the later input-validation fixes. See research/reproduction.

The reviewer found RC3's 401-digit JSON integer caused math.isfinite overflow
before a bound check. RC4 checks the numeric range first. Structured validate/run
rejections and retained campaign rejection now pass; original failure is preserved.
The final plan regression fixtures use read-only hard links for research evidence,
while files subject to mutation remain copied. This avoids repeated hundreds-of-MiB
copies without weakening navigation or evidence checks.

These are local software/computational gates. External human first-use, qualified
model interpretation, public release/downloads and Tanduna readback are not done.
