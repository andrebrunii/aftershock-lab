# Verification record

Local preparation: **17 October 2026**, Linux, Python 3.12.14.

| Check | Observed result |
| --- | --- |
| Unit and SQLite integration suite | 31 tests passed |
| Synthetic demo | 4 scenarios × 5 candidate actions = 20 response replays |
| Handwritten proposal contract cases | 8 expected outcomes matched |
| Rollback with unrelated operator edit | Rule restored, newer banner preserved |
| Rollback with same-cell edit | Refused without partially changing state |
| ABA revision and multi-cell conflict tests | Passed |
| Two SQLite connections with an intervening write | Stale plan rejected |
| Negative-control sensitivity sweep | Eligibility flips between 18/918 and 19/919 legitimate requests denied |
| Bandit 1.9.4 scan | No reported findings; medium/high gate passed |
| HTML JavaScript interactions | Passed in jsdom: selection, counts, budget, abstention cases and rollback modes |
| Browser visual audit | Not completed; browser binary download was unavailable |

Raw evidence is in `test-results.txt`, `bandit-results.json`, `ui-checks.json`, `../examples/results.json` and `../examples/sensitivity.csv`. Reproduce the sensitivity CSV with `python -m aftershock.sensitivity`.

The eight proposal cases are handwritten contract tests. They are not eight attacks against an actual LLM and must not be reported as an LLM defense success rate. The local model adapter was tested with mocked transport and responses only.

## Not established by these checks

- No live Ollama/model inference was run during preparation.
- No real attacker traffic, AWS WAF, cloud infrastructure, EDR, Splunk or production system was used.
- No measured latency, downtime, revenue, prevention rate or field false-positive rate is claimed.
- Windows and GitHub Actions execution are configured but must be verified after publication.
- jsdom checks DOM behavior; they are not a full browser rendering, accessibility or responsive-layout audit.
- A clean static scan is not proof that the application is free of vulnerabilities.

The checked-in report is a snapshot generated from the implementation. After changing scenarios or policy, regenerate it and keep source/results consistent. Do not present local or configured checks as a successful remote pipeline run.
