# User Guide: DAO Voting

*Documentation also available in Ukrainian: [user_guide_dao_voting_uk.md](user_guide_dao_voting_uk.md)*

## Overview
This guide explains how to use the DAO voting features in GlobalScope MultiFrame to participate in decentralized platform governance.

## Prerequisites
- Completed [Platform Overview and Architecture](user_guide_platform_overview.md)
- Basic understanding of decentralized governance concepts
- System account access
- Access to Web3 features

## Understanding DAO Voting

### What is DAO Voting?
DAO (Decentralized Autonomous Organization) voting is a decentralized governance system that allows users to make collective decisions about platform development. In the context of GlobalScope MultiFrame, this includes:
- **Decentralized Governance**: Collective decision-making by participants
- **Transparency**: Openness of all decision-making processes
- **Security**: Cryptographic protection of votes
- **Web3 Integration**: Use of blockchain technologies
- **Automation**: Execution of decisions without intermediaries

### DAO Voting Features
The DAO voting system offers several key capabilities:
- **Proposal Creation**: Ability to submit proposals for voting
- **Voting**: Participation in voting on proposals
- **Result Tracking**: Monitoring voting results
- **Agent Deployment**: Execution of decisions through automated agents
- **Transparent Reporting**: Detailed history of all votes

## Creating Proposals

### 1. Accessing the DAO System
Accessing DAO voting features:
1. Log into your GlobalScope MultiFrame account
2. Navigate to the "Governance" module in the main menu
3. Click on "DAO Voting" in the left sidebar
4. Review active proposals
5. Prepare your proposal for submission

### 2. Preparing a Proposal
Prepare a proposal for submission:
1. Define the proposal topic
2. Write a clear proposal description
3. Specify expected outcomes
4. Set the voting deadline
5. Check compliance with DAO rules

### 3. Submitting a Proposal
Submit a proposal for voting:
1. Click the "Create Proposal" button
2. Enter the proposal title
3. Write a detailed description
4. Set voting parameters
5. Confirm proposal submission

## Participating in Voting

### 1. Viewing Active Proposals
View active proposals for voting:
1. Open the "Active Proposals" section
2. Review the list of available proposals
3. Review the description of each proposal
4. Check voting deadlines
5. Select proposals to participate in voting

### 2. Voting on Proposals
Cast your vote on proposals:
1. Click on the proposal you want to vote on
2. Review the proposal details
3. Select your vote (for or against)
4. Confirm your vote
5. Review current voting results

### 3. Tracking Results
Track voting results:
1. Review the status of active votes
2. Analyze voting trends
3. Review detailed statistics
4. Receive notifications about vote completion
5. Review voting history

## Agent Deployment

### 1. Creating Agents
Create automated agents to execute decisions:
1. Open the "Agent Management" section
2. Click "Create New Agent"
3. Specify agent parameters
4. Configure access rights
5. Confirm agent creation

### 2. Assigning Agents to Proposals
Assign agents to execute proposal decisions:
1. Select the proposal that needs execution
2. Click "Assign Agent"
3. Select the appropriate agent from the list
4. Configure execution parameters
5. Confirm agent assignment

### 3. Monitoring Agents
Monitor deployed agent activity:
1. Open the "Active Agents" section
2. Review the list of deployed agents
3. Analyze their performance
4. Review agent action logs
5. Configure notifications about issues

## Best Practices

### Creating Proposals
1. Write clear and understandable proposals
2. Provide sufficient information for decision-making
3. Consider the interests of the entire community
4. Adhere to proposal submission deadlines
5. Be prepared to answer community questions

### Participating in Voting
1. Carefully study proposals before voting
2. Participate actively in voting
3. Don't vote on proposals you don't understand
4. Follow decentralized governance principles
5. Respect collective decision outcomes

### Agent Management
1. Regularly update agents
2. Monitor their performance
3. Configure appropriate security levels
4. Archive inactive agents
5. Document all agent actions

## Troubleshooting

### Common Issues and Solutions

#### Issue: Proposal not created
- **Cause**: Incorrect formatting or rule violations
- **Solution**: Check proposal format, review DAO rules, contact support

#### Issue: Vote not counted
- **Cause**: Authentication issues or technical errors
- **Solution**: Check authentication status, refresh page, contact support

#### Issue: Agent not deployed
- **Cause**: Insufficient access rights or technical issues
- **Solution**: Check access rights, contact administrator, contact support

#### Issue: Incorrect voting results
- **Cause**: Errors in vote counting system
- **Solution**: Check blockchain transactions, contact support

#### Issue: Proposal violates DAO rules
- **Cause**: Non-compliance with decentralized governance rules
- **Solution**: Review DAO rules, edit proposal, contact moderators

## Related Features
- [Platform Overview and Architecture](user_guide_platform_overview.md)
- [NFT Minting and Transfer](user_guide_nft_minting_transfer.md)
- [VR Training](user_guide_vr_training.md)
- [Community Governance](user_guide_community_governance.md)
- [API Integration](user_guide_api_integration.md)

## API Reference
For programmatic management of DAO voting, refer to the following API endpoints:
- `POST /api/v1/dao/proposal` - Create a new proposal
- `POST /api/v1/dao/vote` - Cast a vote on a proposal
- `GET /api/v1/dao/proposals` - Get list of proposals
- `GET /api/v1/dao/proposal/{proposal_id}` - Get proposal details
- `POST /api/v1/dao/agent/deploy` - Deploy an agent to execute a decision

For detailed API documentation, see [API Documentation](api_documentation.md).