# Database Setup and Demo Data for GlobalScope MultiFrame 11.0

## Overview

*Документація також доступна українською мовою: [DATABASE_uk.md](DATABASE_uk.md)*

*Дивіться [політику мови](docs/language_policy.md) для отримання додаткової інформації про мовні версії.*

## Overview

GlobalScope MultiFrame 11.0 uses Redis as its primary data store. This document explains how to set up the database and initialize it with demo data for testing and development purposes.

## Prerequisites

1. Redis server installed and running
2. Python 3.8 or higher
3. Required Python packages installed (from requirements.txt)

## Redis Data Structure

The system uses the following Redis key patterns:

- `user:*` - User profiles and authentication data
- `driver:*` - Generated chip drivers
- `collab:*` - Collaboration sessions
- `process:*` - Chip design processes
- `nft:*` - Web3 NFT records
- `quest:*` - Learning quests
- `config:*` - System configuration
- `analytics:*` - Performance metrics

Counters for generating unique IDs:
- `driver_counter`
- `collab_counter`
- `process_counter`
- `quest_counter`
- `nft_counter`

## Initializing Demo Data

### Using the Python Script

1. Ensure Redis server is running on localhost:6379
2. Run the initialization script:

```bash
python init_demo_data.py
```

This will:
- Clear any existing data in Redis
- Create sample users, drivers, collaborations, processes, NFTs, and quests
- Set up system configuration and analytics data

### Using Shell Scripts

For Unix/Linux systems:
```bash
chmod +x init_demo_data.sh
./init_demo_data.sh
```

For Windows systems:
```cmd
init_demo_data.bat
```

## Verifying Demo Data

To verify that the demo data was loaded correctly:

```bash
python verify_demo_data.py
```

This script will display a summary of all data loaded into Redis.

## Sample Data Included

The demo data includes:

1. **Users**:
   - HoloMisha (admin)
   - QuantumDesigner (designer)
   - ChipMaster (engineer)

2. **Chip Drivers**:
   - Quantum processor driver
   - Neural processor driver
   - Crypto processor driver

3. **Collaborations**:
   - Active quantum chip design collaboration
   - Completed neural processor collaboration

4. **Processes**:
   - Completed quantum chip process
   - Running neural processor process

5. **NFTs**:
   - Quantum chip NFT
   - Neural processor NFT

6. **Quests**:
   - Completed quantum chip design quest
   - Active neural network optimization quest

## Docker Compose Setup

The system includes a docker-compose.yml file that can be used to start all services including Redis:

```bash
cd src
docker-compose up -d
```

This will start:
- Redis server on port 6379
- The HoloMisha core API on port 8000
- Kong API gateway on port 8001
- Prometheus monitoring on port 9090
- Grafana dashboard on port 3000

## Troubleshooting

### Redis Connection Issues

If you encounter connection issues:

1. Verify Redis is running:
   ```bash
   redis-cli ping
   ```

2. Check Redis configuration:
   ```bash
   redis-cli info
   ```

3. If using Docker, ensure the Redis container is running:
   ```bash
   docker ps
   ```

### Data Initialization Issues

If the demo data initialization fails:

1. Check Redis connectivity in the Python script
2. Verify all required Python packages are installed
3. Check Redis permissions for data modification

## Customizing Demo Data

To customize the demo data:

1. Edit `init_demo_data.py` to modify the sample data
2. Run the script again to reload the data
3. Use `verify_demo_data.py` to confirm changes

The data initialization script is designed to be idempotent, meaning it can be run multiple times without causing issues.