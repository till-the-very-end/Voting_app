"""Smart contract: the voting rules every node enforces on every transaction."""
import json
from wallet import verify


def payload(tx):
    """The exact data that gets signed."""
    keys = ("type", "voter", "candidate", "ts")
    return json.dumps({k: tx[k] for k in keys if k in tx}, sort_keys=True)


class State:
    def __init__(self):
        self.candidates, self.admin = [], None
        self.registered, self.voted, self.tally = set(), set(), {}


def apply(state: State, tx: dict):
    """Validate one transaction against the current state and update it."""
    t = tx.get("type")
    if t == "GENESIS":
        state.candidates, state.admin = tx["candidates"], tx["admin"]
        state.tally = {c: 0 for c in tx["candidates"]}
        return True, "ok"
    if t == "REGISTER":
        if not verify(state.admin, payload(tx), tx.get("sig", "")):
            return False, "Not signed by election admin"
        if tx["voter"] in state.registered:
            return False, "Voter already registered"
        state.registered.add(tx["voter"])
        return True, "Voter registered"
    if t == "VOTE":
        if not verify(tx["voter"], payload(tx), tx.get("sig", "")):
            return False, "Invalid signature"
        if tx["voter"] not in state.registered:
            return False, "Voter is not registered"
        if tx["voter"] in state.voted:
            return False, "Double voting rejected"
        if tx["candidate"] not in state.candidates:
            return False, "Unknown candidate"
        state.voted.add(tx["voter"])
        state.tally[tx["candidate"]] += 1
        return True, "Vote accepted"
    return False, "Unknown transaction type"


def build_state(chain, extra=()):
    """Replay the whole ledger (+ pending txs) to get the current state."""
    st = State()
    for b in chain:
        for tx in b.txs:
            ok, msg = apply(st, tx)
            if not ok:
                return st, False, f"Block {b.index}: {msg}"
    for tx in extra:
        apply(st, tx)
    return st, True, "ok"
