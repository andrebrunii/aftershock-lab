"""Commands mutate only the explicitly selected local simulation database."""
import argparse
import json
from pathlib import Path
import sqlite3
import sys
from .demo import write_demo
from .engine import make_plan, proposal
from .ollama import propose_local
from .scenarios import SPECS, scenario
from .store import Store, verify_journal


def save(path, value):
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="AFTERSHOCK — rehearse response, measure collateral, challenge rollback")
    sub = parser.add_subparsers(dest="command", required=True)
    demo = sub.add_parser("demo")
    demo.add_argument("--out", default="output")
    for name in ("init", "plan", "apply", "edit", "rollback", "audit"):
        command = sub.add_parser(name)
        command.add_argument("--db", default="output/lab.db")
        if name in ("init", "plan"):
            command.add_argument("--scenario", choices=list(SPECS), default="shared-nat")
        if name == "plan":
            command.add_argument("--candidate", default="narrow_control")
            command.add_argument("--proposal", help="Optional JSON proposal from a model or reviewer")
            command.add_argument("--out", default="output/plan.json")
        if name == "apply":
            command.add_argument("--plan", default="output/plan.json")
            command.add_argument("--approve", required=True, help="Exact digest reviewed by the local operator")
        if name == "edit":
            command.add_argument("--key", required=True)
            command.add_argument("--value", required=True, help="A JSON scalar, e.g. true or a quoted string")
        if name == "rollback":
            command.add_argument("--transaction", required=True)
        if name == "audit":
            command.add_argument("--expected-head")
    llm = sub.add_parser("propose")
    llm.add_argument("--scenario", choices=list(SPECS), default="shared-nat")
    llm.add_argument("--model", required=True)
    llm.add_argument("--poisoned", action="store_true")
    llm.add_argument("--port", type=int, default=11434)
    llm.add_argument("--out", default="output/model-run.json")
    args = parser.parse_args()
    store = None
    try:
        if args.command == "demo":
            data = write_demo(args.out)
            print(f"4 synthetic scenarios | 20 action replays | {sum(x['matched'] for x in data['proposal_fixtures'])}/8 proposal fixtures matched")
            print("Rollback: unrelated edit preserved; same-cell conflict refused.")
            print(f"Open: {(Path(args.out) / 'index.html').resolve()}")
            print("No live model, real attack, cloud mutation or network request was executed.")
            return 0
        if args.command == "propose":
            record = propose_local(scenario(args.scenario), args.model, args.poisoned, args.port)
            save(args.out, record)
            if record["schema_valid"]:
                save(str(Path(args.out).with_suffix(".proposal.json")), record["proposal"])
            print(f"Recorded local model output. Schema valid: {record['schema_valid']}. Nothing applied.")
            return 0 if record["schema_valid"] else 2
        db_path = Path(args.db)
        if args.command != "init" and not db_path.is_file():
            raise ValueError("Initialize the local simulation database first")
        db_path.parent.mkdir(parents=True, exist_ok=True)
        store = Store(db_path)
        if args.command == "init":
            store.initialize(scenario(args.scenario)["initial_state"])
            print(f"Initialized local simulation: {db_path}")
        elif args.command == "plan":
            case = scenario(args.scenario)
            proposed = json.loads(Path(args.proposal).read_text(encoding="utf-8")) if args.proposal else proposal(args.candidate)
            plan = make_plan(case, store.snapshot(), proposed)
            save(args.out, plan)
            print(json.dumps({"eligible": plan["evaluation"]["eligible"], "plan_digest": plan["plan_digest"],
                              "checks": plan["evaluation"]["checks"]}, indent=2))
            return 0 if plan["evaluation"]["eligible"] else 3
        elif args.command == "apply":
            plan = json.loads(Path(args.plan).read_text(encoding="utf-8"))
            tx_id = store.apply(scenario(plan["scenario_id"]), plan, args.approve)
            print(f"SIMULATION APPLIED. Transaction: {tx_id}")
        elif args.command == "edit":
            store.edit(args.key, json.loads(args.value))
            print("Local operator edit recorded.")
        elif args.command == "rollback":
            print(json.dumps(store.rollback(args.transaction), indent=2))
        elif args.command == "audit":
            journal = store.journal()
            valid = verify_journal(journal, args.expected_head)
            print(json.dumps({"consistent": valid, "head": journal[-1]["hash"] if journal else None, "events": len(journal),
                              "note": "Hashes detect changes relative to a trusted anchor; they do not authenticate the operator."}, indent=2))
            return 0 if valid else 3
        return 0
    except (ValueError, KeyError, TypeError, StopIteration, OSError, sqlite3.Error) as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 2
    finally:
        if store:
            store.close()


if __name__ == "__main__":
    raise SystemExit(main())
