import copy, time
import streamlit as st
from wallet import Wallet
from contract import payload, build_state
from chain import Blockchain

st.set_page_config(page_title="E-Voting dApp", layout="centered")
NODES = ["Node A", "Node B", "Node C"]
CANDIDATES = ["Alice", "Bob", "Charlie"]


def init():
    admin = Wallet()
    base = Blockchain(CANDIDATES, admin.pub, difficulty=3)
    st.session_state.admin = admin
    st.session_state.wallets = {}
    st.session_state.nodes = {n: copy.deepcopy(base) for n in NODES}


if "nodes" not in st.session_state:
    init()
S = st.session_state


def broadcast(tx):
    results = [S.nodes[n].add_tx(tx) for n in NODES]
    return results[0]


st.title("E-Voting dApp")
st.caption("Blockchain mini project - 3 simulated nodes, Proof of Work, "
           "digital signatures, smart contract")
if st.sidebar.button("Reset everything"):
    init()
    st.rerun()
st.sidebar.write("Candidates:", ", ".join(CANDIDATES))
st.sidebar.write("Admin public key:")
st.sidebar.code(S.admin.pub[:24] + "...")

tabs = st.tabs(["1. Wallets", "2. Register", "3. Vote", "4. Mine",
                "5. Explorer", "6. Results", "7. Tamper"])

with tabs[0]:
    st.subheader("Create voter wallet")
    st.write("A wallet is a public/private key pair. The public key is the voter's identity.")
    name = st.text_input("Voter name")
    if st.button("Generate keys") and name:
        S.wallets[name] = Wallet()
    for n, w in S.wallets.items():
        st.write(f"**{n}** - public key: `{w.pub[:32]}...`")

with tabs[1]:
    st.subheader("Register voter (admin only)")
    if not S.wallets:
        st.info("Create a wallet first.")
    else:
        v = st.selectbox("Voter", list(S.wallets), key="reg")
        if st.button("Sign and broadcast REGISTER"):
            tx = {"type": "REGISTER", "voter": S.wallets[v].pub, "ts": time.time()}
            tx["sig"] = S.admin.sign(payload(tx))
            ok, msg = broadcast(tx)
            (st.success if ok else st.error)(msg)

with tabs[2]:
    st.subheader("Cast vote")
    if not S.wallets:
        st.info("Create a wallet first.")
    else:
        v = st.selectbox("Voter", list(S.wallets), key="vote")
        c = st.radio("Candidate", CANDIDATES)
        if st.button("Sign and broadcast VOTE"):
            tx = {"type": "VOTE", "voter": S.wallets[v].pub, "candidate": c, "ts": time.time()}
            tx["sig"] = S.wallets[v].sign(payload(tx))
            ok, msg = broadcast(tx)
            (st.success if ok else st.error)(msg)
    st.write("Pending transactions (mempool):", len(S.nodes["Node A"].pending))

with tabs[3]:
    st.subheader("Mine a block (Proof of Work)")
    miner = st.selectbox("Miner node", NODES)
    st.write("Difficulty:", S.nodes[miner].difficulty, "| Pending:", len(S.nodes[miner].pending))
    if st.button("Mine"):
        t = time.time()
        b = S.nodes[miner].mine_pending()
        if b is None:
            st.warning("No pending transactions.")
        else:
            for n in NODES:
                if n != miner:
                    S.nodes[n].resolve([S.nodes[miner]])
                    S.nodes[n].pending = []
            st.success(f"Block {b.index} mined in {time.time()-t:.2f}s, nonce = {b.nonce}")
            st.code(b.hash)

with tabs[4]:
    st.subheader("Block explorer")
    node = st.selectbox("View ledger of", NODES, key="exp")
    ok, msg = S.nodes[node].is_valid()
    (st.success if ok else st.error)(f"Chain valid: {ok} ({msg})")
    for b in S.nodes[node].chain:
        with st.expander(f"Block {b.index}  |  {b.hash[:16]}...  |  {len(b.txs)} tx"):
            st.write("Previous hash:", b.prev_hash[:32] + "...")
            st.write("Merkle root:", b.merkle[:32] + "...")
            st.write("Nonce:", b.nonce)
            st.json(b.txs)

with tabs[5]:
    st.subheader("Election result")
    node = st.selectbox("Count from", NODES, key="res")
    state, ok, _ = build_state(S.nodes[node].chain)
    st.bar_chart(state.tally)
    st.write("Registered:", len(state.registered), "| Voted:", len(state.voted))
    st.write("Votes are counted by replaying the chain, not from a stored counter.")

with tabs[6]:
    st.subheader("Tamper test and consensus")
    node = st.selectbox("Attack node", NODES, key="tam")
    chain = S.nodes[node].chain
    idx = st.number_input("Block index", 1, max(1, len(chain) - 1), 1)
    fake = st.selectbox("Change vote to", CANDIDATES)
    if st.button("Tamper"):
        done = False
        if idx < len(chain):
            for tx in chain[idx].txs:
                if tx["type"] == "VOTE":
                    tx["candidate"] = fake
                    done = True
        st.warning("Vote changed in this node's copy." if done else "No VOTE tx in that block.")
    for n in NODES:
        ok, msg = S.nodes[n].is_valid()
        st.write(f"{n}: {'VALID' if ok else 'INVALID'} - {msg}")
    if st.button("Run consensus (longest valid chain)"):
        for n in NODES:
            S.nodes[n].resolve([S.nodes[m] for m in NODES if m != n])
        st.rerun()
