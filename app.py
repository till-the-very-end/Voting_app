import json, os
import streamlit as st
import streamlit.components.v1 as components
from web3 import Web3

st.set_page_config(page_title="E-Voting dApp", layout="centered")
ABI = json.load(open(os.path.join(os.path.dirname(__file__), "abi.json")))
DEFAULT_RPC = "https://ethereum-sepolia-rpc.publicnode.com"

st.title("E-Voting dApp")
st.caption("Solidity smart contract on Sepolia testnet | MetaMask | Remix IDE")

addr = st.sidebar.text_input("Contract address (from Remix)")
rpc = st.sidebar.text_input("Sepolia RPC URL", DEFAULT_RPC)
st.sidebar.write("Network: Sepolia (chain id 11155111)")

if not Web3.is_address(addr):
    st.info("Deploy EVoting.sol from Remix, then paste the contract address in the sidebar.")
    st.stop()
addr = Web3.to_checksum_address(addr)

try:
    w3 = Web3(Web3.HTTPProvider(rpc))
    if w3.eth.chain_id != 11155111:
        st.error("RPC is not Sepolia.")
        st.stop()
    code = w3.eth.get_code(addr)
    if not code or code == b'\x00' or code == b'':
        st.error(
            f"❌ No smart contract code found at address `{addr}` on Sepolia testnet.\n\n"
            "**Common causes:**\n"
            "1. **Remix VM used instead of Sepolia:** Address `0x5B38...` is a Remix local test account address. In Remix under *Deploy & Run*, change **Environment** from *Remix VM* to **Injected Provider - MetaMask**.\n"
            "2. **Wrong Address Copied:** Copy the contract address from *Deployed Contracts* section at the bottom left of Remix after deploying.\n"
            "3. **Not Deployed Yet:** Make sure the deployment transaction finished in MetaMask."
        )
        st.stop()
    c = w3.eth.contract(address=addr, abi=ABI)
    admin = c.functions.admin().call()
    is_open = c.functions.votingOpen().call()
    names, counts = c.functions.getCandidates().call()
except Exception as e:
    st.error(f"Could not read contract. Check address/network. ({e})")
    st.stop()

st.subheader("Election status")
st.write("Admin:", admin)
st.write("Voting is", "OPEN" if is_open else "CLOSED")
st.write(f"[View contract on Etherscan](https://sepolia.etherscan.io/address/{addr})")

st.subheader("Live results (read from blockchain)")
st.bar_chart(dict(zip(names, counts)))
st.write("Total votes:", sum(counts))
if st.button("Refresh"):
    st.rerun()

st.subheader("Check a voter")
v = st.text_input("Voter address")
if Web3.is_address(v):
    v = Web3.to_checksum_address(v)
    st.write("Registered:", c.functions.isRegistered(v).call(),
             "| Voted:", c.functions.hasVoted(v).call())

st.subheader("Actions (signed in MetaMask)")
st.caption("Admin account: register voters, start/end voting. Voter account: vote.")

HTML = """
<style>
 body{font-family:sans-serif;font-size:14px} button{margin:3px;padding:5px 9px}
 input,select{padding:4px;margin:3px} #log{margin-top:8px;color:#333;word-break:break-all}
</style>
<button onclick="connect()">Connect MetaMask</button><br>
<b>Admin:</b><br>
<input id="voter" size="44" placeholder="voter address 0x...">
<button onclick="send('registerVoter', document.getElementById('voter').value)">Register voter</button><br>
<button onclick="send('startVoting')">Start voting</button>
<button onclick="send('endVoting')">End voting</button><br>
<b>Voter:</b><br>
<select id="cand"></select>
<button onclick="send('vote', document.getElementById('cand').value)">Cast vote</button>
<div id="log"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/ethers/6.7.0/ethers.umd.min.js"></script>
<script>
const ADDR="__ADDR__", ABI=__ABI__, NAMES=__NAMES__;
const eth = window.ethereum || window.parent.ethereum;
let c=null;
NAMES.forEach((n,i)=>{document.getElementById('cand').add(new Option(n,i));});
const log=(m)=>{document.getElementById('log').innerHTML=m;};
async function connect(){
  if(!eth){log("MetaMask not found. Install the extension.");return false;}
  await eth.request({method:'eth_requestAccounts'});
  try{await eth.request({method:'wallet_switchEthereumChain',params:[{chainId:'0xaa36a7'}]});}
  catch(e){log("Please switch MetaMask to Sepolia.");return false;}
  const signer=await (new ethers.BrowserProvider(eth)).getSigner();
  c=new ethers.Contract(ADDR,ABI,signer);
  log("Connected: "+await signer.getAddress());
  return true;
}
async function send(fn,...args){
  try{
    if(!c && !(await connect())) return;
    const tx=await c[fn](...args);
    log("Tx sent: <a target='_blank' href='https://sepolia.etherscan.io/tx/"+tx.hash+"'>"+tx.hash+"</a> waiting...");
    await tx.wait();
    log("Confirmed. Click Refresh above. <a target='_blank' href='https://sepolia.etherscan.io/tx/"+tx.hash+"'>View tx</a>");
  }catch(e){log("Error: "+(e.reason||e.shortMessage||e.message));}
}
</script>
"""
html = (HTML.replace("__ADDR__", addr).replace("__ABI__", json.dumps(ABI))
            .replace("__NAMES__", json.dumps(list(names))))
components.html(html, height=330)
