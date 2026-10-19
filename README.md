# E-Voting dApp — Deployed Blockchain Voting System

## 1. Project Overview

The **E-Voting dApp (Decentralized Application)** is a blockchain-based electronic voting system developed using Solidity, Remix IDE, MetaMask, and the Ethereum Sepolia test network.

The project demonstrates how blockchain technology can be used to manage a voting process through smart contracts. It provides voter registration, controlled voting, vote counting, and result retrieval, with voting records maintained on the blockchain.

**Project Status:** Deployed and accessible online.

**Live Application:** https://votingapp-zf5kmhyqhyfyq8ggwpfkbr.streamlit.app/

## 2. Project Aim

To develop and demonstrate a decentralized electronic voting application using smart contracts deployed on the Ethereum Sepolia testnet.

## 3. Objectives

- Demonstrate the practical implementation of a blockchain-based decentralized application.
- Develop voting rules using Solidity smart contracts.
- Deploy and interact with a smart contract on the Sepolia test network using Remix IDE.
- Integrate MetaMask for wallet connectivity and transaction signing.
- Implement voter registration, voting, and candidate vote counting.
- Demonstrate blockchain concepts such as transparency, immutability, transaction validation, and access control.

## 4. Technologies Used

| Technology | Purpose |
|---|---|
| Solidity | Implements the voting smart contract and its rules |
| Remix IDE | Compiles, deploys, and tests the smart contract |
| Ethereum Sepolia | Public Ethereum test network used for deployment |
| MetaMask | Connects user wallets and signs blockchain transactions |
| Streamlit | Provides the web-based user interface |
| Python / web3.py | Supports blockchain interaction and reading contract data |
| ethers.js | Supports wallet-based blockchain transactions |
| JSON ABI | Defines the interface used to communicate with the smart contract |

## 5. System Architecture

The application consists of a frontend, a blockchain wallet, and a deployed smart contract.

**System workflow:**

1. The administrator deploys the smart contract and defines the candidates.
2. The administrator registers eligible voters.
3. The administrator starts the voting process.
4. Registered voters connect their wallets and cast their votes.
5. The smart contract validates each voting transaction.
6. The blockchain records successful transactions and updates the vote counts.
7. The application retrieves and displays candidate results.

### Architecture Diagram

```text
       Administrator / Voter
                |
                v
       Streamlit Web Interface
                |
          +-----+------+
          |            |
     Read Contract   Write Actions
     (web3.py/RPC)   (ethers.js)
          |            |
          |         MetaMask
          |      Transaction Signing
          |            |
          +------+-----+
                 |
                 v
        Ethereum Sepolia Testnet
                 |
                 v
          EVoting Smart Contract
          (Deployed using Remix)
                 |
                 v
       Candidate Counts and Results
```

## 6. Smart Contract Functionality

The `EVoting.sol` smart contract contains the core voting logic.

### Main functions

- **Candidate initialization:** Stores the candidates when the contract is deployed.
- **Voter registration:** Allows the administrator to register eligible voter addresses.
- **Start voting:** Opens the voting process.
- **Cast vote:** Allows a registered voter to vote for a valid candidate.
- **End voting:** Allows the administrator to close the voting process.
- **Retrieve candidates:** Reads candidate information and vote counts.
- **Access control:** Restricts administrative operations to the designated administrator.

### Voting validation

Before accepting a vote, the smart contract checks that:

- Voting is open.
- The voter is registered.
- The voter has not already voted.
- The selected candidate ID is valid.

If a condition is not satisfied, the transaction is rejected by the smart contract.

## 7. Blockchain Concepts Demonstrated

**Decentralization:** The voting contract operates on the Ethereum test network rather than relying solely on a centralized application server.

**Wallet-based identity:** Ethereum wallet addresses identify the administrator and registered voters.

**Digital signatures:** MetaMask signs transactions using the connected wallet.

**Gas fees:** Blockchain write operations require Sepolia test ETH.

**Immutability:** Successfully mined blockchain transactions cannot simply be edited or deleted.

**Events and auditability:** Smart contract events can provide a record of voter registration, voting activity, and voting status.

**Access control:** The administrator-only modifier protects restricted functions.

**Consensus:** Ethereum validators process and confirm transactions through Ethereum's Proof of Stake consensus mechanism.

## 8. Deployment and Implementation

The project has been deployed using the following technologies:

- **Smart contract deployment:** Solidity contract compiled and deployed through Remix IDE.
- **Blockchain network:** Ethereum Sepolia testnet.
- **Wallet integration:** MetaMask for connecting accounts and signing transactions.
- **Web application:** Streamlit application published online.
- **Blockchain interaction:** Contract interface and blockchain communication through the configured application components.

The deployed application can be accessed here:

**Live Project:** https://votingapp-zf5kmhyqhyfyq8ggwpfkbr.streamlit.app/

The application demonstrates the interaction between a web interface, a blockchain wallet, and a deployed smart contract.

## 9. Testing and Validation

The following scenarios are relevant to validating the voting system:

| Test scenario | Expected behavior |
|---|---|
| Register an eligible voter | The administrator can register the voter |
| Start voting | Voting becomes active |
| Cast a valid vote | The candidate's vote count increases |
| Vote without registration | The contract rejects the vote |
| Vote more than once | The contract rejects the second vote |
| Select an invalid candidate ID | The contract rejects the transaction |
| Vote after voting closes | The contract rejects the vote |
| Retrieve candidate results | The application reads the available candidate counts |

These tests demonstrate the validation rules enforced by the smart contract. Actual test results and screenshots can be added to document the completed test cases.

## 10. Applications and Limitations

### Potential applications

- Academic and blockchain technology demonstrations.
- Small-scale organizational voting prototypes.
- Demonstrations of smart contract-based election workflows.
- Learning about wallet integration and blockchain transactions.

### Limitations

- Sepolia is a test network and uses test ETH, not real funds.
- Wallet addresses do not independently verify a person's real-world identity.
- Public blockchain transactions can expose voting activity and related wallet addresses.
- The application is an educational prototype and has not been established as a secure, production-ready election system.
- Production elections would require additional security audits, privacy protections, identity verification, and measures against coercion and other election-specific risks.

## 11. Conclusion

The E-Voting dApp demonstrates the implementation and deployment of a blockchain-based voting system using Solidity, Remix IDE, MetaMask, Ethereum Sepolia, and Streamlit.

The project illustrates how smart contracts can enforce voting rules, validate transactions, prevent duplicate voting by registered wallet addresses, and maintain candidate vote counts on a blockchain.

The deployed application provides a practical demonstration of decentralized application architecture and the integration of a web interface with blockchain technology.

## 12. Live Demo

**Explore the deployed E-Voting dApp:**

https://votingapp-zf5kmhyqhyfyq8ggwpfkbr.streamlit.app/


