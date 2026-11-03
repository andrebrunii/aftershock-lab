"""Deterministic intervention replay and policy checks over a stated toy model."""
from copy import deepcopy
import hashlib
import json

DEFAULT_POLICY = {"min_containment_pct": 90, "max_collateral_pct": 2,
                  "max_unknown_denied": 0, "min_labeled_coverage_pct": 95}


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def digest(obj):
    return hashlib.sha256(canonical(obj).encode()).hexdigest()


def parse_proposal(value, case):
    if not isinstance(value, dict) or set(value) != {"candidate_id", "evidence_ids", "explanation"}:
        raise ValueError("Proposal must contain only candidate_id, evidence_ids and explanation")
    if value["candidate_id"] not in [c["id"] for c in case["candidates"]]:
        raise ValueError("Unknown action; arbitrary tools and commands are not supported")
    ids = value["evidence_ids"]
    if not isinstance(ids, list) or not 1 <= len(ids) <= 10 or any(not isinstance(i, str) for i in ids):
        raise ValueError("At least one bounded evidence reference is required")
    if len(ids) != len(set(ids)) or not set(ids) <= {x["id"] for x in case["observations"]}:
        raise ValueError("Duplicate or unknown evidence reference")
    if not isinstance(value["explanation"], str) or not 1 <= len(value["explanation"]) <= 1500:
        raise ValueError("Explanation must contain 1 to 1500 characters")
    return deepcopy(value)


def proposal(candidate_id):
    return {"candidate_id": candidate_id, "evidence_ids": ["E1", "E2"],
            "explanation": "Deterministic fixture proposal. Evaluate independently before approving."}


def validate_policy(policy):
    if not isinstance(policy, dict) or set(policy) != set(DEFAULT_POLICY):
        raise ValueError("Unexpected policy fields")
    for key, value in policy.items():
        if type(value) is not int or value < 0 or (key.endswith("pct") and value > 100):
            raise ValueError("Policy bounds must be nonnegative integers; percentages cannot exceed 100")


def candidate(case, candidate_id):
    return next(c for c in case["candidates"] if c["id"] == candidate_id)


def service_available(service, state, dependencies, visiting=None):
    visiting = set() if visiting is None else visiting
    if service not in dependencies or service in visiting or f"service:{service}" not in state:
        raise ValueError("Missing or cyclic service dependency; refuse incomplete simulation")
    # Validate all dependency branches even if this service is unavailable.
    children = [service_available(d, state, dependencies, visiting | {service}) for d in dependencies[service]]
    return state[f"service:{service}"] and all(children)


def allowed(request, state, dependencies):
    if not service_available(request["service"], state, dependencies):
        return False
    if request["principal"] == "batch" and not state["identity:batch"]:
        return False
    if state["waf:enabled"]:
        if state.get(f"block:{request['ip']}", False):
            return False
        if state["rule:sensitive"] and request["path"] in {"/.env", "/.git/config"}:
            return False
        if state["rule:signature"] and request["path"] == "/hooks/payment" and not request["signature"]:
            return False
    return True


def replay(case, state, patch):
    if not set(patch) <= set(state):
        raise ValueError("Patch touches an unknown resource")
    after = {**state, **patch}
    totals = {label: 0 for label in ("benign", "attack", "unknown")}
    denied = {label: 0 for label in totals}
    witnesses = {label: [] for label in totals}
    for req in case["requests"]:
        if req["label"] not in totals:
            raise ValueError("Unknown evaluator label")
        before_ok = allowed(req, state, case["dependencies"])
        after_ok = allowed(req, after, case["dependencies"])
        if before_ok:
            totals[req["label"]] += 1
            if not after_ok:
                denied[req["label"]] += 1
                if len(witnesses[req["label"]]) < 4:
                    witnesses[req["label"]].append({k: req[k] for k in ("id", "service", "path", "ip", "principal")})
    labeled = sum(r["label"] != "unknown" for r in case["requests"])
    return {"baseline_allowed": totals, "newly_denied": denied,
            "containment_pct": 100 * denied["attack"] / totals["attack"] if totals["attack"] else None,
            "collateral_pct": 100 * denied["benign"] / totals["benign"] if totals["benign"] else None,
            "labeled_coverage_pct": 100 * labeled / len(case["requests"]) if case["requests"] else 0,
            "witnesses": witnesses}


def evaluate(case, state, candidate_id, policy=None):
    policy = deepcopy(DEFAULT_POLICY if policy is None else policy)
    validate_policy(policy)
    action = candidate(case, candidate_id)
    result = replay(case, state, action["patch"])
    checks = [
        ("CONTROL_INTEGRITY", action["patch"].get("waf:enabled", True) is not False, "The proposer cannot disable WAF protection."),
        ("EVIDENCE_COVERAGE", result["labeled_coverage_pct"] >= policy["min_labeled_coverage_pct"], "Labeled coverage must meet the selected policy floor."),
        ("ATTACK_SAMPLE", result["baseline_allowed"]["attack"] >= 1, "Need at least one baseline-allowed attack example."),
        ("BENIGN_SAMPLE", result["baseline_allowed"]["benign"] >= 50, "Need at least 50 baseline-allowed benign examples."),
        ("CONTAINMENT", result["containment_pct"] is not None and result["containment_pct"] >= policy["min_containment_pct"], "Containment must reach the selected floor."),
        ("COLLATERAL", result["collateral_pct"] is not None and result["collateral_pct"] <= policy["max_collateral_pct"], "Legitimate request loss must remain within budget."),
        ("UNKNOWN_IMPACT", result["newly_denied"]["unknown"] <= policy["max_unknown_denied"], "Do not hide uncertain traffic inside the benign denominator."),
    ]
    return {**result, "candidate_id": candidate_id, "title": action["title"], "patch": action["patch"],
            "checks": [{"code": code, "passed": passed, "description": desc} for code, passed, desc in checks],
            "eligible": all(passed for _, passed, _ in checks)}


def make_plan(case, snapshot, proposed, policy=None):
    proposed = parse_proposal(proposed, case)
    state = {key: item["value"] for key, item in snapshot.items()}
    policy = deepcopy(DEFAULT_POLICY if policy is None else policy)
    result = evaluate(case, state, proposed["candidate_id"], policy)
    body = {"version": 1, "scenario_id": case["id"], "scenario_digest": digest(case),
            "snapshot_digest": digest(snapshot), "proposal": proposed, "policy": policy, "evaluation": result}
    return {**body, "plan_digest": digest(body)}
