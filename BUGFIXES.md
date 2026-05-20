# Bugfix Log

This file tracks bugs found and fixed before GitHub uploads. Keep entries short, factual and testable.

## Entry Format

```text
Date:
Area:
Severity:
Bug:
Root cause:
Fix:
Verification:
Files changed:
Remaining risk:
```


## 2026-05-20 20:05

Date: 2026-05-20 20:05

Area: Stabilization, scan diagnostics, GitHub packaging, regression testing

Severity: High

Bug: Scanner engine/fallback state was not visible enough in the UI, making it hard to distinguish process scanning from thread fallback during slow scans. The GitHub upload folder also still contained runtime result/error data that should not be published.

Root cause: Engine metadata existed in small runtime files, but it was not surfaced in a compact always-available panel. The upload folder had accumulated local runtime artifacts during earlier debugging.

Fix: Added a lightweight scan-engine diagnostics panel with engine, worker count, candidates/s, RAM-cache, CPU and process-RAM fields, added `run_regression_tests.py`, copied the current bot into the upload folder, updated GitHub documentation, and removed runtime/errorlog artifacts from the public upload folder.

Verification: `python -m py_compile bot.py` passed. `python run_regression_tests.py` passed. Synthetic benchmark showed increasing throughput from 1 to 16 workers. Local Streamlit smoke test returned HTTP 200.

Files changed: `./bot.py`, `./run_regression_tests.py`, `./README.md`, `./FILES_TO_UPLOAD.txt`, `./.gitignore`, `./Updates.txt`, `./bugfixes/BUGFIXES.md`

Remaining risk: No long multi-hour live KuCoin scan or real-money order was executed in this pass. Those must remain separate controlled validation steps.

## 2026-05-20 17:05

Date: 2026-05-20 17:05

Area: UI translations, order book labels, background scanner initialization

Severity: High

Bug: Recent screenshots still showed mixed Swedish/English text in the English UI, including the worker-reservation note, RAM CSV flush label and order-book table headers. A background scan could also report a critical `num_workers` initialization error before the worker count had been assigned.

Root cause: Some runtime strings were built outside the translation layer. The scan engine also used `num_workers` in RAM/diagnostic metadata before assigning it.

Fix: Added an explicit English branch for the worker-reservation note, localized the RAM CSV flush label and order-book table columns, refreshed order-book column labels when the language changes, and moved worker-count initialization before RAM/shared-memory diagnostics.

Verification: `python -m py_compile` passed for the production bot. Static searches found no remaining `backgruond`, `Preset profilee`, stale worker-note translation call or `numworkers` typo.

Files changed: `./bot.py`, `./bugfixes/BUGFIXES.md`

Remaining risk: Screenshots already committed to `./screenshots` are static captures. Any old translation text inside those images remains visible until the screenshots are re-captured from the corrected UI.
