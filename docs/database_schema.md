# GlobalScope MultiFrame 11.0 Database Schema Documentation

## Overview
This document provides comprehensive documentation of the database schema for GlobalScope MultiFrame 11.0. The system uses Redis as its primary data store with a key-value structure organized by entity types.

## Database Technology
- **Primary Store**: Redis 7.0
- **Data Model**: Key-Value with JSON serialization
- **Connection**: redis://localhost:6379 (default)

## Schema Structure

### Key Naming Convention
All keys follow the pattern: `{entity_type}:{identifier}`

### Entity Types

#### 1. Users
**Key Pattern**: `user:{user_id}`

**Fields**:
- `user_id` (string): Unique user identifier
- `username` (string): User's display name
- `email` (string): User's email address
- `role` (string): User role (admin, designer, engineer)
- `created_at` (ISO timestamp): Account creation timestamp

**Example**:
```json
{
  "user_id": "user_1",
  "username": "HoloMisha",
  "email": "holo@misha.com",
  "role": "admin",
  "created_at": "2025-09-29T10:30:00"
}
```

#### 2. Chip Drivers
**Key Pattern**: `driver:{driver_id}`

**Fields**:
- `driver_id` (string): Unique driver identifier
- `user_id` (string): ID of the user who created the driver
- `chip_id` (string): Associated chip identifier
- `chip_data` (object): Chip specifications
  - `type` (string): Chip type (quantum_processor, neural_processor, crypto_processor)
  - `cores` (integer): Number of cores
  - `frequency` (string): Processing frequency
  - `architecture` (string): Chip architecture
- `status` (string): Driver status (generated, optimized)
- `version` (string): Driver version
- `timestamp` (ISO timestamp): Creation/modification timestamp

**Example**:
```json
{
  "driver_id": "driver_1",
  "user_id": "user_1",
  "chip_id": "chip_quantum_1",
  "chip_data": {
    "type": "quantum_processor",
    "cores": 128,
    "frequency": "4.5GHz",
    "architecture": "QubitCore"
  },
  "status": "optimized",
  "version": "2.1.0",
  "timestamp": "2025-09-29T10:30:00"
}
```

#### 3. Collaborations
**Key Pattern**: `collab:{collab_id}`

**Fields**:
- `collab_id` (string): Unique collaboration identifier
- `user_id` (string): ID of the collaboration creator
- `chip_id` (string): Associated chip identifier
- `chip_data` (object): Chip specifications (same structure as drivers)
- `collaborators` (array of strings): List of collaborator user IDs
- `status` (string): Collaboration status (active, completed)
- `timestamp` (ISO timestamp): Creation timestamp

**Example**:
```json
{
  "collab_id": "collab_1",
  "user_id": "user_1",
  "chip_id": "chip_quantum_1",
  "chip_data": {
    "type": "quantum_processor",
    "cores": 128,
    "frequency": "4.5GHz",
    "architecture": "QubitCore"
  },
  "collaborators": ["user_2", "user_3"],
  "status": "active",
  "timestamp": "2025-09-29T10:30:00"
}
```

#### 4. Chip Processes
**Key Pattern**: `process:{process_id}`

**Fields**:
- `process_id` (string): Unique process identifier
- `user_id` (string): ID of the user who initiated the process
- `chip_data` (object): Chip specifications (same structure as drivers)
- `status` (string): Process status (running, completed)
- `timestamp` (ISO timestamp): Creation timestamp

**Example**:
```json
{
  "process_id": "process_1",
  "user_id": "user_1",
  "chip_data": {
    "type": "quantum_processor",
    "cores": 128,
    "frequency": "4.5GHz",
    "architecture": "QubitCore"
  },
  "status": "completed",
  "timestamp": "2025-09-29T10:30:00"
}
```

#### 5. NFTs
**Key Pattern**: `nft:{nft_id}`

**Fields**:
- `nft_id` (string): Unique NFT identifier
- `user_id` (string): ID of the NFT owner
- `chip_id` (string): Associated chip identifier
- `metadata_uri` (string): IPFS URI for NFT metadata
- `owner` (string): Blockchain address of the owner

**Example**:
```json
{
  "nft_id": "nft_user_1_chip_quantum_1",
  "user_id": "user_1",
  "chip_id": "chip_quantum_1",
  "metadata_uri": "ipfs://metadata/nft_user_1_chip_quantum_1",
  "owner": "0x1234567890123456789012345678901234567890"
}
```

#### 6. Quests
**Key Pattern**: `quest:{quest_id}`

**Fields**:
- `quest_id` (string): Unique quest identifier
- `user_id` (string): ID of the user undertaking the quest
- `title` (string): Quest title
- `description` (string): Quest description
- `status` (string): Quest status (active, completed)
- `reward` (string): Reward for completing the quest
- `timestamp` (ISO timestamp): Creation timestamp

**Example**:
```json
{
  "quest_id": "quest_1",
  "user_id": "user_1",
  "title": "Quantum Chip Design",
  "description": "Design a quantum processor with 128 cores",
  "status": "completed",
  "reward": "nft_quantum_designer",
  "timestamp": "2025-09-29T10:30:00"
}
```

#### 7. System Configuration
**Key Pattern**: `config:system`

**Fields**:
- `system` (object): System-level configuration
  - `version` (string): System version
  - `mode` (string): System mode (production, development)
  - `maintenance` (boolean): Maintenance mode status
- `subscription_price` (integer): Default subscription price
- `supported_fabs` (array of strings): List of supported fabrication partners
- `supported_protocols` (array of strings): List of supported communication protocols

**Example**:
```json
{
  "system": {
    "version": "11.0.0",
    "mode": "production",
    "maintenance": false
  },
  "subscription_price": 10,
  "supported_fabs": ["TSMC", "Intel", "Samsung"],
  "supported_protocols": ["MQTT", "OPC_UA"]
}
```

#### 8. Analytics
**Key Pattern**: `analytics:metrics`

**Fields**:
- `chip_metrics` (object): Performance metrics for chips
  - `{chip_id}` (object): Metrics for a specific chip
    - `performance` (float): Performance percentage
    - `efficiency` (float): Efficiency percentage
    - `temperature` (float): Temperature in Celsius
    - `last_updated` (ISO timestamp): Last update timestamp

**Example**:
```json
{
  "chip_metrics": {
    "chip_quantum_1": {
      "performance": 95.5,
      "efficiency": 87.2,
      "temperature": 45.3,
      "last_updated": "2025-09-29T10:30:00"
    }
  }
}
```

### Counters
**Keys**: Simple integer values used for generating unique IDs

- `driver_counter`: Current driver ID counter
- `collab_counter`: Current collaboration ID counter
- `process_counter`: Current process ID counter
- `quest_counter`: Current quest ID counter
- `nft_counter`: Current NFT ID counter

## Relationships

### User Relationships
- Users can create multiple drivers, collaborations, processes, and quests
- Users can participate in collaborations as collaborators
- Users can own multiple NFTs

### Chip Relationships
- Chips are associated with drivers, collaborations, processes, and NFTs
- Chip metrics are stored in the analytics data

## Data Access Patterns

### Read Operations
1. Get user by ID: `GET user:{user_id}`
2. Get all users: `KEYS user:*`
3. Get driver by ID: `GET driver:{driver_id}`
4. Get all drivers: `KEYS driver:*`
5. Get collaboration by ID: `GET collab:{collab_id}`
6. Get all collaborations: `KEYS collab:*`
7. Get process by ID: `GET process:{process_id}`
8. Get all processes: `KEYS process:*`
9. Get NFT by ID: `GET nft:{nft_id}`
10. Get all NFTs: `KEYS nft:*`
11. Get quest by ID: `GET quest:{quest_id}`
12. Get all quests: `KEYS quest:*`
13. Get system configuration: `GET config:system`
14. Get analytics data: `GET analytics:metrics`

### Write Operations
1. Create/update user: `SET user:{user_id} {user_data}`
2. Create/update driver: `SET driver:{driver_id} {driver_data}`
3. Create/update collaboration: `SET collab:{collab_id} {collab_data}`
4. Create/update process: `SET process:{process_id} {process_data}`
5. Create/update NFT: `SET nft:{nft_id} {nft_data}`
6. Create/update quest: `SET quest:{quest_id} {quest_data}`
7. Update system configuration: `SET config:system {config_data}`
8. Update analytics data: `SET analytics:metrics {analytics_data}`
9. Update counters: `SET {counter_name} {value}`

## Indexing Strategy
Redis keys serve as the primary index. Additional indexing is achieved through:
1. Key naming conventions for grouping related data
2. Counter mechanisms for generating unique IDs
3. Application-level caching of frequently accessed data

## Performance Considerations
1. All data is stored as JSON strings for flexibility
2. Keys are designed for efficient pattern matching with `KEYS` command
3. Counters are used to avoid expensive `KEYS` operations for ID generation
4. Analytics data is updated periodically to minimize write operations

## Backup and Recovery
1. Regular Redis snapshots using RDB persistence
2. AOF (Append Only File) logging for durability
3. Data can be exported using `DUMP` and `RESTORE` commands
4. Demo data scripts provide a recovery mechanism for development environments

## Security Considerations
1. Data is stored in plaintext JSON format
2. Access control should be implemented at the application level
3. Sensitive data should be encrypted before storage
4. Redis authentication should be enabled in production environments

## Scalability
1. Redis single-instance limitations for large datasets
2. Key sharding strategies for horizontal scaling
3. Consider Redis Cluster for production deployments
4. Data partitioning by user or time for better performance

## Maintenance
1. Regular cleanup of expired or obsolete data
2. Counter reset procedures for development environments
3. Data validation and integrity checks
4. Performance monitoring and optimization