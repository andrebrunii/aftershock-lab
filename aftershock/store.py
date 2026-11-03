"""SQLite transactions for simulated state; approval binding and scoped compensation."""
import json
import sqlite3
from .engine import canonical, digest, make_plan


class Conflict(ValueError):
    """Re-review is required; no partial write is allowed."""


class Store:
    def __init__(self, path=":memory:"):
        self.db = sqlite3.connect(str(path), isolation_level=None, timeout=5)
        self.db.executescript("""
            CREATE TABLE IF NOT EXISTS cells (name TEXT PRIMARY KEY, value TEXT NOT NULL, rev INTEGER NOT NULL);
            CREATE TABLE IF NOT EXISTS transactions (id TEXT PRIMARY KEY, patch TEXT NOT NULL, status TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS audit (seq INTEGER PRIMARY KEY, record TEXT NOT NULL, previous TEXT NOT NULL, hash TEXT NOT NULL);
        """)

    def close(self):
        self.db.close()

    def snapshot(self):
        return {key: {"value": json.loads(value), "revision": rev}
                for key, value, rev in self.db.execute("SELECT name,value,rev FROM cells ORDER BY name")}

    def initialize(self, state):
        self.db.execute("BEGIN IMMEDIATE")
        try:
            if self.snapshot():
                raise ValueError("Database already initialized; choose a new path")
            self.db.executemany("INSERT INTO cells VALUES (?,?,0)", [(k, canonical(v)) for k, v in state.items()])
            self._audit({"kind": "initialize", "state_digest": digest(state)})
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise

    def _audit(self, record):
        previous = self.db.execute("SELECT hash FROM audit ORDER BY seq DESC LIMIT 1").fetchone()
        previous = previous[0] if previous else "0" * 64
        seq = self.db.execute("SELECT count(*) FROM audit").fetchone()[0] + 1
        entry_hash = digest({"seq": seq, "previous": previous, "record": record})
        self.db.execute("INSERT INTO audit VALUES (?,?,?,?)", (seq, canonical(record), previous, entry_hash))

    def apply(self, case, plan, approval):
        self.db.execute("BEGIN IMMEDIATE")
        try:
            if approval != plan.get("plan_digest"):
                raise Conflict("Approval does not match this exact plan")
            snapshot = self.snapshot()
            rebuilt = make_plan(case, snapshot, plan["proposal"], plan["policy"])
            if rebuilt != plan:
                raise Conflict("Plan changed or snapshot is stale; preview and approve again")
            if not rebuilt["evaluation"]["eligible"]:
                raise Conflict("Policy denied this action; approval cannot override the gate")
            patch = {}
            for key, value in rebuilt["evaluation"]["patch"].items():
                old = snapshot[key]
                if old["value"] != value:
                    patch[key] = {"before": old["value"], "after": value, "applied_revision": old["revision"] + 1}
                    self.db.execute("UPDATE cells SET value=?,rev=rev+1 WHERE name=?", (canonical(value), key))
            tx_id = plan["plan_digest"]
            self.db.execute("INSERT INTO transactions VALUES (?,?,?)", (tx_id, canonical(patch), "applied"))
            self._audit({"kind": "apply", "transaction": tx_id, "patch": patch, "plan_digest": tx_id})
            self.db.commit()
            return tx_id
        except Exception:
            self.db.rollback()
            raise

    def edit(self, key, value):
        """Lab-only operator edit used to reproduce concurrent changes."""
        self.db.execute("BEGIN IMMEDIATE")
        try:
            current = self.snapshot()
            if key not in current or type(value) is not type(current[key]["value"]):
                raise ValueError("Unknown cell or invalid value type")
            self.db.execute("UPDATE cells SET value=?,rev=rev+1 WHERE name=?", (canonical(value), key))
            self._audit({"kind": "operator_edit", "cell": key, "value": value})
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise

    def rollback(self, tx_id):
        self.db.execute("BEGIN IMMEDIATE")
        try:
            row = self.db.execute("SELECT patch,status FROM transactions WHERE id=?", (tx_id,)).fetchone()
            if not row:
                raise ValueError("Unknown transaction")
            if row[1] == "rolled_back":
                self.db.rollback()
                return {"status": "already_rolled_back", "restored_cells": []}
            patch = json.loads(row[0])
            snapshot = self.snapshot()
            for key, change in patch.items():
                if snapshot.get(key) != {"value": change["after"], "revision": change["applied_revision"]}:
                    raise Conflict(f"Rollback conflict on {key}; preserve the newer edit and investigate")
            for key, change in patch.items():
                self.db.execute("UPDATE cells SET value=?,rev=rev+1 WHERE name=?", (canonical(change["before"]), key))
            self.db.execute("UPDATE transactions SET status='rolled_back' WHERE id=?", (tx_id,))
            self._audit({"kind": "rollback", "transaction": tx_id, "restored_cells": sorted(patch)})
            self.db.commit()
            return {"status": "rolled_back", "restored_cells": sorted(patch)}
        except Exception:
            self.db.rollback()
            raise

    def journal(self):
        return [{"seq": seq, "record": json.loads(record), "previous": previous, "hash": h}
                for seq, record, previous, h in self.db.execute("SELECT seq,record,previous,hash FROM audit ORDER BY seq")]


def verify_journal(records, expected_head=None):
    previous = "0" * 64
    for index, entry in enumerate(records, 1):
        body = {"seq": index, "previous": previous, "record": entry["record"]}
        if entry["seq"] != index or entry["previous"] != previous or entry["hash"] != digest(body):
            return False
        previous = entry["hash"]
    return expected_head is None or previous == expected_head
