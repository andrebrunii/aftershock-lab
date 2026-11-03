# Architecture, invariants and trust boundaries

## Trusted versus untrusted

Trusted in this lab: Python code, action catalog, scenario topology, evaluator labels, policy configuration, local database and its owner. Untrusted: optional LLM response and log text shown to it. The model receives incident observations, candidate identifiers and the untrusted log field; it does not receive request-level labels.

`parse_proposal` permits exactly three fields: `candidate_id`, `evidence_ids`, `explanation`. It rejects extra fields, unknown actions, invented evidence references and oversized explanations. Explanations remain text. The model cannot submit shell commands, patches, policy overrides or evaluation scores. A valid reference does not prove semantic support: analysts still review the explanation.

The default handwritten fixtures test this **contract**, not whether a model resists prompt injection. The optional Ollama adapter sends only to fixed loopback address `127.0.0.1`, has no tool interface and does not apply proposals. Running that service under an untrusted same-user process is outside the model boundary.

## Replay model

Each request has service, exact path, source IP, synthetic principal, signature-valid flag, and evaluator label (`benign`, `attack`, `unknown`). Service dependencies form a directed acyclic graph. Every required service must be available. A missing dependency or cycle aborts simulation.

With WAF enabled, the selected source IP can be denied; the sensitive-path control denies `/.env` and `/.git/config`; the signature control denies invalid callbacks at `/hooks/payment`. Disabling the batch identity denies requests using that principal. These are synthetic controls, not implementations of AWS WAF or a cryptographic signature verifier.

For the same fixed workload, evaluate baseline state and the state after one patch. Count **newly denied** requests: requests allowed in baseline and denied after the patch. Already-denied requests do not inflate containment or collateral.

Let A and B be the baseline-allowed attack and benign counts, and dA and dB their newly-denied counts:

`containment = 100 × dA/A`; `collateral = 100 × dB/B`.

An empty denominator yields no score and fails the corresponding gate. Unknown requests remain a separate count. Labeled coverage is the fraction of all fixture requests whose label is not unknown.

Default eligibility requires: WAF protection is not disabled by the patch; at least 95% labeled coverage; at least one baseline-allowed attack and 50 baseline-allowed benign examples; at least 90% containment; no more than 2% collateral; no newly denied unknown requests. These are educational policy choices, not recommended operational thresholds.

The graph and request outcomes are deterministic. This is an intervention replay in a toy model, not causal identification from observational data and not an estimate of what an adaptive adversary would do next.

## Plan binding and commit

A plan records proposal, policy, scenario digest, complete snapshot digest and recomputed evaluation. Its digest binds that content. The operator reviews it and explicitly supplies the digest to apply.

Under `BEGIN IMMEDIATE`, apply reloads the current cells and revisions, reconstructs the whole plan, compares it with the reviewed plan, checks eligibility and writes the patch and audit record in one SQLite transaction. Any intervening snapshot revision change invalidates the plan. This is deliberately conservative, including changes to unrelated keys between review and apply.

The digest is not a secret, signature or authentication token. Someone who owns the files can create and approve plans. The implementation does not separate approver and executor identities. Do not describe it as production RBAC, cryptographic authorization, a distributed lock or a sandbox for hostile Python code.

## Compensation and the ABA case

The transaction stores only cells whose value changed, with before value, after value and applied revision. Rollback first verifies **all** affected cells still match the recorded after value and revision. If one fails, no cell is changed. If all pass, it restores before values and advances revisions; it does not rewind revision numbers.

Unrelated changes survive because rollback never restores a complete snapshot. A same-value write increments revision and causes a conflict. Changing `true → false → true` also causes a conflict: matching values alone would miss this ABA pattern.

Repeated rollback of an already compensated transaction returns `already_rolled_back`. The database prevents partial changes and serializes writers. This local behavior does not solve concurrent changes in remote cloud APIs or distributed transactions.

## Evidence integrity

Audit records contain sequence, previous hash, event and current hash. Verification detects altered records relative to the supplied chain. Truncation requires a previously trusted `expected_head`. An attacker with write access can rewrite the chain and head together; therefore hashes alone provide no authenticity, external timestamp or immutability. Rejected operations return errors but are not appended to the transactional journal in this version.

## Rollback is not recovery

Undoing containment may reopen an attack path. The lab's rollback is an explicit operator command, not an automatic claim that the incident is resolved. It restores configuration cells, not leaked data, rotated credentials, money transferred, external notifications or real-world trust. An operational implementation would need an independent recovery decision, revalidation, service-owner approval and action-specific compensation semantics.

## Separation from Git

Git reverts source changes. AFTERSHOCK compensates local simulated runtime state. Reverting a commit does not undo a database transaction or recover an exposed secret. Conversely, rolling back the simulated rule does not change source history.
