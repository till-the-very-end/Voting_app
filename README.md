# E-Voting dApp (Solidity + Remix + MetaMask + Sepolia)

## Project Aim
Create a dApp (de-centralized app) for an e-voting system.

## Objectives
- To illustrate the concepts of a blockchain dApp.
- To write, deploy and interact with a smart contract on a public Ethereum testnet (Sepolia) using Remix IDE and MetaMask.

## Theory

### Concepts used
| Concept | Where |
|---|---|
| Smart contract | `contracts/EVoting.sol` holds all voting rules |
| Decentralized ledger | Votes are stored on Sepolia, replicated on every Ethereum node |
| Public/private key, digital signature | MetaMask account signs every transaction |
| Wallet address = identity | `msg.sender` identifies admin and voters |
| Transactions and gas | Every write (register, vote) is a transaction paid in Sepolia ETH |
| Consensus (Proof of Stake on Ethereum) | Validators confirm blocks containing our transactions |
| Immutability | Once a vote is mined it cannot be edited or deleted |
| Events | `VoterRegistered`, `VoteCast`, `VotingStatus` give an audit trail |
| Access control | `onlyAdmin` modifier |
| Hashing / Merkle tree / block linking | Used internally by Ethereum; implemented by hand in `simulation/` |
| dApp architecture | Frontend (Streamlit + ethers.js + web3.py) -> MetaMask -> Contract |

### Algorithm
1. Admin deploys `EVoting` with candidate names; deployer becomes admin.
2. Admin calls `registerVoter(address)` for each eligible voter.
3. Admin calls `startVoting()`.
4. Voter calls `vote(candidateId)`. The contract requires: voting open, sender registered, sender has not voted, candidate id valid. Then it sets `hasVoted[sender] = true` and increments the count.
5. Admin calls `endVoting()`.
6. Anyone reads `getCandidates()` (free, no gas) to see the result.

### Block diagram
```
 Admin / Voter
      |
 [ Streamlit UI (app.py) ]
   |  read (web3.py, RPC)        |  write (ethers.js)
   |                             v
   |                       [ MetaMask ] -- signs tx with private key
   |                             |
   v                             v
 [ Sepolia testnet nodes ]  --  EVoting.sol (Remix-deployed)
      blocks -> validators confirm -> state stored on-chain
```

### Modules
- `contracts/EVoting.sol` - smart contract.
- `abi.json` - contract interface used by the frontend.
- `app.py` - Streamlit dApp: live results, voter check, MetaMask actions.
- `simulation/` - optional pure-Python chain (hash, Merkle, PoW) for extra theory marks.

## Step 1: Setup MetaMask and get Sepolia ETH
1. Install the MetaMask browser extension and create a wallet (save the seed phrase safely).
2. Open MetaMask, enable **Show test networks**, switch to **Sepolia**.
3. Create a second account (Account 2) to act as a voter.
4. Get free test ETH from a Sepolia faucet (e.g. Google Cloud Web3 faucet, Alchemy faucet, or the PoW faucet sepolia-faucet.pk910.de). Send some to both accounts.

## Step 2: Deploy from Remix
1. Open https://remix.ethereum.org.
2. Create `EVoting.sol` in the `contracts` folder and paste the code from this project.
3. **Solidity Compiler** tab: choose compiler 0.8.20 or higher, click **Compile**.
4. **Deploy & Run** tab: Environment = **Injected Provider - MetaMask** (confirm it shows Sepolia, Network 11155111).
5. Next to **Deploy**, enter candidates as `["Alice","Bob","Charlie"]`.
6. Click **Deploy** and confirm in MetaMask.
7. Copy the contract address under **Deployed Contracts** (and screenshot the Etherscan page for the report).
8. Test in Remix: `registerVoter(<Account 2 address>)`, `startVoting()`, switch MetaMask to Account 2, call `vote(0)`, then `getCandidates()`.

## Step 3: Run the frontend locally
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```
Paste the contract address in the sidebar. Use the same browser that has MetaMask installed.

## Step 4: Deploy on Streamlit Community Cloud
1. Push the project to a public GitHub repo (`app.py`, `abi.json`, `requirements.txt` at the root).
2. Go to https://share.streamlit.io, sign in with GitHub, **Create app**, pick repo, branch `main`, main file `app.py`, **Deploy**.
3. Open the `.streamlit.app` URL, paste the contract address in the sidebar, and use MetaMask from your browser.
Note: Streamlit runs on a server, so it cannot hold your private key. MetaMask in the user's browser signs everything, which is how real dApps work.

## Output (Screenshots)
Add: Remix compile, Remix deploy, MetaMask confirmation, Etherscan contract page, Streamlit results page, a rejected double vote.

## Troubleshooting
- "MetaMask not found" inside the app: use a desktop browser with the extension, not an in-app browser.
- Transaction fails with "Not registered" / "Voting is not open" / "Already voted": these are the contract rules working.
- Results look old: click Refresh after the transaction is confirmed.

## Conclusion
Thus, successfully implemented a dApp (de-centralized app) for e-voting system.
