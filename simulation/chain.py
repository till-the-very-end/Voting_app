"""Core blockchain: hashing, Merkle tree, blocks, Proof of Work, validation, consensus."""
import copy, hashlib, json, time
from contract import apply, build_state


def sha256(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def tx_hash(tx: dict) -> str:
    return sha256(json.dumps(tx, sort_keys=True))


def merkle_root(hashes):
    if not hashes:
        return sha256("")
    level = list(hashes)
    while len(level) > 1:
        if len(level) % 2:
            level.append(level[-1])          # duplicate last if odd
        level = [sha256(level[i] + level[i + 1]) for i in range(0, len(level), 2)]
    return level[0]


class Block:
    def __init__(self, index, txs, prev_hash, timestamp=None):
        self.index, self.txs, self.prev_hash = index, txs, prev_hash
        self.timestamp = time.time() if timestamp is None else timestamp
        self.nonce = 0
        self.merkle = merkle_root([tx_hash(t) for t in txs])
        self.hash = self.calc_hash()

    def calc_hash(self):
        return sha256(f"{self.index}{self.timestamp}{self.prev_hash}{self.merkle}{self.nonce}")

    def mine(self, difficulty):              # Proof of Work
        while not self.hash.startswith("0" * difficulty):
            self.nonce += 1
            self.hash = self.calc_hash()


def valid_chain(chain, difficulty):
    for i, b in enumerate(chain):
        if b.merkle != merkle_root([tx_hash(t) for t in b.txs]):
            return False, f"Block {b.index}: transactions do not match Merkle root"
        if b.hash != b.calc_hash():
            return False, f"Block {b.index}: hash mismatch"
        if not b.hash.startswith("0" * difficulty):
            return False, f"Block {b.index}: Proof of Work invalid"
        if i > 0 and b.prev_hash != chain[i - 1].hash:
            return False, f"Block {b.index}: broken link to previous block"
    _, ok, msg = build_state(chain)           # re-run smart contract on all txs
    return ok, msg


class Blockchain:
    def __init__(self, candidates, admin_pub, difficulty=3):
        self.difficulty, self.pending = difficulty, []
        g = Block(0, [{"type": "GENESIS", "candidates": candidates,
                       "admin": admin_pub, "ts": 0}], "0" * 64, timestamp=0)
        g.mine(difficulty)
        self.chain = [g]

    def add_tx(self, tx):
        state, _, _ = build_state(self.chain, self.pending)
        ok, msg = apply(state, tx)
        if ok:
            self.pending.append(tx)
        return ok, msg

    def mine_pending(self):
        if not self.pending:
            return None
        b = Block(len(self.chain), self.pending, self.chain[-1].hash)
        b.mine(self.difficulty)
        self.chain.append(b)
        self.pending = []
        return b

    def is_valid(self):
        return valid_chain(self.chain, self.difficulty)

    def resolve(self, peers):
        """Consensus: adopt the longest VALID chain among peers."""
        best = self.chain if self.is_valid()[0] else []
        for p in peers:
            if p.is_valid()[0] and len(p.chain) > len(best):
                best = p.chain
        if best is not self.chain and best:
            self.chain = copy.deepcopy(best)
            self.pending = []
            return True
        return False
