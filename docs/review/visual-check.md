# Browser and visual review

Agent review, 2026-09-08 UTC. Actual execution model: GPT-6 Astra, confirmed from the reviewer’s runtime turn context before writes. This is software/browser evidence, not human accessibility testing or domain validation.

## Reviewed snapshot

The real numerical/evaluator report at `runs/first-study/report.html`, SHA-256 `98ef517aa2f43ebeb7195c0296ccb3285cd0220a0d05507cabec3993bc62332f`, was loaded directly with `file://` in sandboxed HeadlessChrome 140.0.7339.186. Screenshots were inspected visually, not inferred from HTML. A retained cancelled/not-run snapshot was also reviewed at `runs/first-recovery/reports/078958bc439fcacf021d978709108fbe33487c8c5d616fe2ec056c0236e62a0d/report.html`.

This is an early executable snapshot. Later renderer changes require a fresh run against the final artifact; this record does not certify later source builds.

## Result

25 automated browser assertions passed; no captured browser runtime or console errors. Evidence: `runs/browser/results.json` and PNG files in the same directory.

| Fixed review dimension | Score (0–2) | Observed evidence |
| --- | ---: | --- |
| Legibility and units | 1 | Desktop and phone quantity cards have readable separate kW/kWh labels and explicit full quantity tables. Minor polish defect: interval discharge/export values include signed zero (`0 / -0`, `-0`). |
| Nonclaims and noncolor cues | 2 | Fictional scenario, model limits, and no overall winner are explicit. Baseline/candidate roles and model states appear as text, independent of blue/gold borders. |
| Navigation and focus | 2 | Browser keyboard events expose first-Tab skip link; Enter reaches main and section anchors; Enter/Space open/close details; focused table scrolls with Right Arrow. Solid visible focus outlines captured. |
| Narrow layout | 2 | 390×844 and 320×844 have no document horizontal overflow. Tables scroll within focused regions. Cards stack; no data clipped outside table regions. Wordmark wraps at 320px without losing text. |
| Unsuccessful result | 2 | Cancelled baseline and not-run candidate show explicit states and unavailable quantities. Verdict says comparison is ineligible; missing metrics are not replaced by zero. |

Desktop first view is 1440×1000. A 200% reflow proxy was checked using a 720×500 CSS viewport at DPR 2, equivalent layout space to 1440×1000 at 200%; it had no page horizontal overflow. This is **not an actual browser UI zoom test**. No screen-reader, physical touch-device, browser-family matrix, user study, or formal WCAG conformance claim is made.

All ten export links resolve to nonempty local files. Activating Scenario JSON with keyboard Enter opens its exact parsed JSON in this Chromium `file://` context; the browser does not force a download despite the HTML download attribute. Evidence therefore supports access to the local export, not guaranteed save-to-disk behavior across browsers.

## Visual evidence

- `runs/browser/desktop.png` and `desktop-full.png`: rendered desktop overview and full report.
- `runs/browser/phone.png` and `phone-full.png`: rendered phone overview and full report.
- `runs/browser/phone-comparison.png`: both policy cards and actual numerical results.
- `runs/browser/narrow320.png` and `zoom200-reflow.png`: constrained layout checks.
- `runs/browser/keyboard-skip.png`, `keyboard-details.png`, `keyboard-table-scroll.png`: visible focus and exercised controls.
- `runs/browser/phone-unsuccessful.png` and `phone-unsuccessful-full.png`: real cancelled/not-run snapshot.

The reproduction command in the early report predates the root’s CLI wrapper rename; final-artifact QA must use a newly generated report.

## Repeat

The QA driver uses Node’s built-in WebSocket/CDP and filesystem APIs; no npm package or production dependency was added. Run from this repository:

```sh
node tools/test_report_browser.mjs runs/first-study/report.html runs/browser runs/first-recovery/reports/078958bc439fcacf021d978709108fbe33487c8c5d616fe2ec056c0236e62a0d/report.html
```

Arguments are the report, an output directory under `runs/browser`, and an optional real unsuccessful snapshot. `GRID_BROWSER` can select a local Chromium executable. Default executable is the already available Chromium headless shell revision 1193 in the user Playwright cache. The driver starts an isolated profile and loopback-only CDP endpoint; it closes its own browser on completion. No public server is started. Profile, downloads, local libraries, and logs stay under this project. `runs/` and `.cache/` are already ignored.

## Development-only runtime provenance

Three missing libraries were downloaded from the official AlmaLinux repository as exact RPMs, verified with `rpm -K` (digests and signatures OK), and extracted with `rpm2cpio` into `.cache/browser/root`; no host package was installed. Source RPM names and LGPLv2+ license files are retained in RPM metadata/extracted paths. These files are QA-only and must not be included as product runtime dependencies.

| Package | Official source | SHA-256 |
| --- | --- | --- |
| atk 2.28.1-1.el8 x86_64, LGPLv2+ | https://repo.almalinux.org/almalinux/8/AppStream/x86_64/os/Packages/atk-2.28.1-1.el8.x86_64.rpm | `882e6d686af8a7d3bd5080e43ba2a5cfab625b3384dcfcf25aa3971c4902ebf9` |
| at-spi2-atk 2.26.2-1.el8 x86_64, LGPLv2+ | https://repo.almalinux.org/almalinux/8/AppStream/x86_64/os/Packages/at-spi2-atk-2.26.2-1.el8.x86_64.rpm | `ea0a4c413f9c23de510256d2c99ac870438bf8b95e6ba155ab9a134e672fdb85` |
| at-spi2-core 2.28.0-1.el8 x86_64, LGPLv2+ | https://repo.almalinux.org/almalinux/8/AppStream/x86_64/os/Packages/at-spi2-core-2.28.0-1.el8.x86_64.rpm | `3f34083b191a471c62353d8a9e9cd262e16d8b624a2f4d7414a5f0326f4461f6` |

Chromium’s sandbox stayed enabled. No host security settings, shared browser cache, toolchain, or sibling project were changed.
