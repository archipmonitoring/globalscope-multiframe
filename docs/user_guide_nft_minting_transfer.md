# User Guide: NFT Minting and Transfer

*Документація також доступна українською мовою: [user_guide_nft_minting_transfer_uk.md](user_guide_nft_minting_transfer_uk.md)*

## Overview
This guide explains how to use the NFT minting and transfer features in GlobalScope MultiFrame to tokenize chip designs, protect intellectual property, and ensure authenticity verification. The system uses blockchain technology to create unique digital assets that represent your chip designs.

## Prerequisites
- Completed [Platform Overview and Architecture](user_guide_platform_overview.md)
- Basic understanding of blockchain and NFT concepts
- Familiarity with [IP Block Generation](user_guide_ip_block_generation.md)
- Access to appropriate project resources and permissions
- Availability of a cryptographic wallet for blockchain transactions

## Understanding NFTs in GlobalScope MultiFrame

### What are NFTs for Chip Designs?
NFTs (Non-Fungible Tokens) in the context of GlobalScope MultiFrame are unique digital assets that represent ownership rights to specific chip designs or IP blocks. They enable:
- **Authenticity Verification**: Cryptographic proof of design originality
- **Intellectual Property Protection**: Immutable record of ownership rights on the blockchain
- **Asset Trading**: Ability to buy, sell, and license designs
- **Ownership Tracking**: Complete history of ownership and rights transfers
- **Decentralized Verification**: Independent authenticity verification without intermediaries

### NFT Features in GlobalScope MultiFrame
The NFT system offers several key capabilities:
- **NFT Creation**: Minting tokens for your chip designs
- **Rights Transfer**: Secure transfer of NFT ownership
- **Design Metadata**: Built-in storage of technical design information
- **Licensing**: Ability to create licensing agreements through smart contracts
- **Marketplace Integration**: Seamless integration with [IP Block Trading](user_guide_ip_block_trading.md)

## Creating NFTs

### 1. Preparing Design for Tokenization
Prepare your chip design for NFT creation:
1. Navigate to the "Marketplace" module from the main navigation
2. Select the project or IP block you want to tokenize
3. Ensure the design is complete and tested
4. Prepare metadata: description, technical specifications, images
5. Define licensing terms (if needed)

### 2. Minting NFTs
Create an NFT for your design:
1. In the project editor, click "Create NFT"
2. Review metadata and technical information
3. Select the blockchain for NFT deployment (Ethereum, Polygon, or other)
4. Specify metadata URI (IPFS or other decentralized storage)
5. Click "Create NFT" and confirm the transaction in your wallet
6. Wait for blockchain confirmation (typically 1-5 minutes)

### 3. Verifying Created NFT
Verify successful NFT creation:
1. Navigate to the "My NFTs" section in your profile
2. Find the newly created NFT in the list
3. Check the token ID and contract address
4. Ensure all metadata is correctly stored
5. Save NFT information for future operations

## Transferring NFTs

### 1. Preparing for Transfer
Prepare to transfer an NFT to another user:
1. Navigate to the "My NFTs" section in your profile
2. Select the NFT you want to transfer
3. Review ownership details and metadata
4. Obtain the recipient's wallet address
5. Define transfer terms (free, for reward, licensing)

### 2. Executing Transfer
Execute the NFT transfer:
1. In the NFT details, click "Transfer"
2. Enter the recipient's wallet address
3. Specify transfer terms (if needed)
4. Confirm the transaction in your wallet
5. Wait for blockchain confirmation
6. Ensure the transfer is successfully completed

### 3. Confirming Transfer
Confirm successful transfer:
1. Check the NFT status in your list (should be gone)
2. Ensure the recipient has received the NFT (they can check in their profile)
3. Save the transaction hash for future reference
4. Update internal ownership records (if needed)

## NFT Management

### 1. NFT Catalog
Organizing your NFT collection:
- **Categorization**: Grouping NFTs by design types
- **Search and Filtering**: Quick search by IDs, dates, types
- **Statuses**: Tracking statuses (active, transferred, for sale)
- **Metadata**: Viewing and updating metadata (per smart contract support)
- **History**: Complete history of transfers and transactions

### 2. Licensing and Royalties
Managing licensing rights:
- **Licensing Agreements**: Creating and managing licenses through smart contracts
- **Royalties**: Automatic royalty payments on subsequent sales
- **Usage Restrictions**: Setting restrictions on IP usage
- **Term Management**: Managing license term expiration
- **Reporting**: Tracking licensed IP usage

### 3. Marketplace Integration
Using NFTs on the marketplace:
- **Listing for Sale**: Offering NFTs for buying and selling
- **Auctions**: Participating in chip design auctions
- **Offers**: Creating offers for specific buyers
- **Sales Statistics**: Tracking sales performance
- **Reputation**: Building reputation as an IP seller

## Best Practices

### NFT Creation
1. Ensure the design is fully complete before tokenization
2. Use decentralized storage (e.g., IPFS) for metadata
3. Document all technical design specifications
4. Set clear licensing terms
5. Keep backup copies of metadata and contracts

### NFT Transfer
1. Double-check the recipient's wallet address
2. Use test transactions to verify the process
3. Document all transfers for internal accounting
4. Notify the recipient of the transfer through the platform
5. Keep transaction hashes for legal purposes

### Security and Privacy
1. Never disclose wallet private keys
2. Use wallets with hardware security support
3. Verify contract addresses before confirming transactions
4. Use test networks for experimentation
5. Regularly update wallet software

## Troubleshooting

### Common Issues and Solutions

#### Issue: Transaction not confirming
- **Cause**: Insufficient gas or network issues
- **Solution**: Increase gas limit or try later when the network is less congested

#### Issue: NFT not appearing in profile
- **Cause**: Blockchain indexing delay or metadata issues
- **Solution**: Wait a few minutes or check metadata URI

#### Issue: Error during NFT transfer
- **Cause**: Incorrect recipient address or lack of ownership rights
- **Solution**: Verify the address and ensure you own the NFT

#### Issue: NFT metadata unavailable
- **Cause**: Decentralized storage issues or incorrect URI
- **Solution**: Check URI availability and consider migrating metadata

#### Issue: High transaction fees
- **Cause**: High blockchain activity levels
- **Solution**: Try executing the transaction at a different time or use a different blockchain

## Related Features
- [Platform Overview and Architecture](user_guide_platform_overview.md)
- [IP Block Generation](user_guide_ip_block_generation.md)
- [IP Block Trading](user_guide_ip_block_trading.md)
- [Partner Program](user_guide_partner_program.md)
- [Quantum Security](user_guide_quantum_security.md)

## API Reference
For programmatic NFT management, refer to the following API endpoints:
- `POST /api/v1/web3/nft/mint` - Create (mint) NFT
- `POST /api/v1/web3/nft/transfer` - Transfer NFT to another user
- `GET /api/v1/web3/nft/{nft_id}` - Get NFT information
- `GET /api/v1/web3/nft/{nft_id}/metadata` - Get NFT metadata
- `GET /api/v1/web3/nft/{nft_id}/history` - Get NFT transfer history

For detailed API documentation, see [API Documentation](api_documentation.md).