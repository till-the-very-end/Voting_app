// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title E-Voting smart contract (Sepolia testnet)
contract EVoting {
    struct Candidate {
        string name;
        uint256 voteCount;
    }

    address public admin;                       // deployer = election admin
    bool public votingOpen;
    Candidate[] private candidates;
    mapping(address => bool) public isRegistered;
    mapping(address => bool) public hasVoted;

    event VoterRegistered(address indexed voter);
    event VoteCast(address indexed voter, uint256 indexed candidateId);
    event VotingStatus(bool open);

    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin");
        _;
    }

    constructor(string[] memory names) {
        require(names.length >= 2, "Need 2+ candidates");
        admin = msg.sender;
        for (uint256 i = 0; i < names.length; i++) {
            candidates.push(Candidate(names[i], 0));
        }
    }

    function registerVoter(address voter) external onlyAdmin {
        require(!isRegistered[voter], "Already registered");
        isRegistered[voter] = true;
        emit VoterRegistered(voter);
    }

    function startVoting() external onlyAdmin {
        votingOpen = true;
        emit VotingStatus(true);
    }

    function endVoting() external onlyAdmin {
        votingOpen = false;
        emit VotingStatus(false);
    }

    function vote(uint256 candidateId) external {
        require(votingOpen, "Voting is not open");
        require(isRegistered[msg.sender], "Not registered");
        require(!hasVoted[msg.sender], "Already voted");
        require(candidateId < candidates.length, "Invalid candidate");
        hasVoted[msg.sender] = true;
        candidates[candidateId].voteCount += 1;
        emit VoteCast(msg.sender, candidateId);
    }

    function candidatesCount() external view returns (uint256) {
        return candidates.length;
    }

    function getCandidates() external view returns (string[] memory names, uint256[] memory counts) {
        names = new string[](candidates.length);
        counts = new uint256[](candidates.length);
        for (uint256 i = 0; i < candidates.length; i++) {
            names[i] = candidates[i].name;
            counts[i] = candidates[i].voteCount;
        }
    }
}
