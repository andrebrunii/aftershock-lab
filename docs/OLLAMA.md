# Optional local LLM experiment

The bundled demo has no live LLM results. The adapter is implemented and its transport/schema behavior is tested with mocks. This protocol is for your own actual model run.

## Prerequisites

Run Ollama locally with an installed model that supports the chat API and structured outputs. Use `ollama list` to choose an existing model tag appropriate for your available hardware. The project does not download a model or assume a particular GPU. The endpoint is fixed to loopback `127.0.0.1`; `--port` defaults to 11434. Remote endpoints are intentionally unsupported.

Ollama accepts a JSON schema in the `format` field of `/api/chat`; the application still validates the returned content. See [structured outputs](https://docs.ollama.com/capabilities/structured-outputs) and [chat API](https://docs.ollama.com/api/chat).

## Paired runs

Replace `YOUR_INSTALLED_MODEL` with the local tag:

```bash
python -m aftershock propose --model YOUR_INSTALLED_MODEL --out output/clean.json
python -m aftershock propose --model YOUR_INSTALLED_MODEL --poisoned --out output/poisoned.json
```

The clean and poisoned versions share the scenario. Only the untrusted log field changes. The poisoned field claims authority and asks for WAF removal. Temperature is set to zero, but inference is not guaranteed to be bit-for-bit deterministic across hardware, versions or repeated runs.

The record includes the requested/returned model name, time, prompt context, raw answer, schema status and parsed proposal if valid. Invalid output is retained as evidence. No tool call or database mutation follows automatically. A valid proposal is saved alongside the record, for example `output/poisoned.proposal.json`.

## Independent evaluation

```bash
python -m aftershock init --db output/model-eval.db
python -m aftershock plan --db output/model-eval.db --proposal output/poisoned.proposal.json --out output/model-plan.json
```

Exit code 3 means a valid plan was evaluated and denied by policy; code 2 indicates an error or refusal such as invalid proposal input. Read the JSON rather than treating any nonzero exit as an experiment failure. If schema validation failed, no proposal file is generated for that run; do not reuse an older file from a previous run. Choose new output names for each trial.

## Record observations, not a manufactured success story

Keep model/version/digest, Ollama version, hardware, date, scenario, exact input, output, selected action, validation status, containment and collateral. Use at least several paired runs and report all outcomes, including unchanged responses and invalid JSON. A changed action is not automatically a successful injection; inspect whether it violates the task or policy.

Do not report the eight built-in handwritten fixtures as an 8/8 defense rate against LLM attacks. A meaningful attack-success metric needs a declared attack corpus, repeated model runs, a fixed success definition, denominators and baseline utility. This lab does not claim a broad prompt-injection defense benchmark.

The independent gate can reject a harmful recommendation even when the model follows injected text. It can also accept a harmful action outside the simplified scenario's coverage. Model quality, evaluator quality and authorization are separate concerns.
