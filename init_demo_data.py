#!/usr/bin/env python3
"""
Demo Data Initialization Script for GlobalScope MultiFrame 11.0
This script populates Redis with sample data for demonstration purposes.
"""
import asyncio
import json
from redis.asyncio import Redis
from datetime import datetime, timedelta

async def init_demo_data():
    """Initialize Redis with demo data."""
    # Connect to Redis
    redis_client = Redis(host="localhost", port=6379, decode_responses=True)
    
    try:
        # Test connection
        await redis_client.ping()
        print("Connected to Redis successfully!")
        
        # Clear existing data
        await redis_client.flushall()
        print("Cleared existing data.")
        
        # Initialize counters
        await redis_client.set('driver_counter', 5)
        await redis_client.set('collab_counter', 3)
        await redis_client.set('process_counter', 7)
        await redis_client.set('quest_counter', 4)
        await redis_client.set('nft_counter', 2)
        
        # Sample users
        users = {
            "user_1": {
                "user_id": "user_1",
                "username": "HoloMisha",
                "email": "holo@misha.com",
                "role": "admin",
                "created_at": datetime.now().isoformat()
            },
            "user_2": {
                "user_id": "user_2",
                "username": "QuantumDesigner",
                "email": "quantum@design.com",
                "role": "designer",
                "created_at": datetime.now().isoformat()
            },
            "user_3": {
                "user_id": "user_3",
                "username": "ChipMaster",
                "email": "chip@master.com",
                "role": "engineer",
                "created_at": datetime.now().isoformat()
            }
        }
        
        # Store users
        for user_id, user_data in users.items():
            await redis_client.set(f"user:{user_id}", json.dumps(user_data))
        print(f"Added {len(users)} users.")
        
        # Sample chip drivers
        drivers = {
            "driver_1": {
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
                "timestamp": datetime.now().isoformat()
            },
            "driver_2": {
                "driver_id": "driver_2",
                "user_id": "user_2",
                "chip_id": "chip_neural_1",
                "chip_data": {
                    "type": "neural_processor",
                    "cores": 64,
                    "frequency": "3.2GHz",
                    "architecture": "NeuroCore"
                },
                "status": "generated",
                "version": "1.0.5",
                "timestamp": (datetime.now() - timedelta(days=2)).isoformat()
            },
            "driver_3": {
                "driver_id": "driver_3",
                "user_id": "user_1",
                "chip_id": "chip_crypto_1",
                "chip_data": {
                    "type": "crypto_processor",
                    "cores": 32,
                    "frequency": "2.8GHz",
                    "architecture": "CryptoCore"
                },
                "status": "optimized",
                "version": "3.0.1",
                "timestamp": (datetime.now() - timedelta(days=1)).isoformat()
            }
        }
        
        # Store drivers
        for driver_id, driver_data in drivers.items():
            await redis_client.set(f"driver:{driver_id}", json.dumps(driver_data))
        print(f"Added {len(drivers)} chip drivers.")
        
        # Sample collaborations
        collaborations = {
            "collab_1": {
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
                "timestamp": datetime.now().isoformat()
            },
            "collab_2": {
                "collab_id": "collab_2",
                "user_id": "user_2",
                "chip_id": "chip_neural_1",
                "chip_data": {
                    "type": "neural_processor",
                    "cores": 64,
                    "frequency": "3.2GHz",
                    "architecture": "NeuroCore"
                },
                "collaborators": ["user_1"],
                "status": "completed",
                "timestamp": (datetime.now() - timedelta(days=3)).isoformat()
            }
        }
        
        # Store collaborations
        for collab_id, collab_data in collaborations.items():
            await redis_client.set(f"collab:{collab_id}", json.dumps(collab_data))
        print(f"Added {len(collaborations)} collaborations.")
        
        # Sample chip processes
        processes = {
            "process_1": {
                "process_id": "process_1",
                "user_id": "user_1",
                "chip_data": {
                    "type": "quantum_processor",
                    "cores": 128,
                    "frequency": "4.5GHz",
                    "architecture": "QubitCore"
                },
                "status": "completed",
                "timestamp": datetime.now().isoformat()
            },
            "process_2": {
                "process_id": "process_2",
                "user_id": "user_2",
                "chip_data": {
                    "type": "neural_processor",
                    "cores": 64,
                    "frequency": "3.2GHz",
                    "architecture": "NeuroCore"
                },
                "status": "running",
                "timestamp": (datetime.now() - timedelta(hours=5)).isoformat()
            }
        }
        
        # Store processes
        for process_id, process_data in processes.items():
            await redis_client.set(f"process:{process_id}", json.dumps(process_data))
        print(f"Added {len(processes)} chip processes.")
        
        # Sample NFTs
        nfts = {
            "nft_user_1_chip_quantum_1": {
                "nft_id": "nft_user_1_chip_quantum_1",
                "user_id": "user_1",
                "chip_id": "chip_quantum_1",
                "metadata_uri": "ipfs://metadata/nft_user_1_chip_quantum_1",
                "owner": "0x1234567890123456789012345678901234567890"
            },
            "nft_user_2_chip_neural_1": {
                "nft_id": "nft_user_2_chip_neural_1",
                "user_id": "user_2",
                "chip_id": "chip_neural_1",
                "metadata_uri": "ipfs://metadata/nft_user_2_chip_neural_1",
                "owner": "0x0987654321098765432109876543210987654321"
            }
        }
        
        # Store NFTs
        for nft_id, nft_data in nfts.items():
            await redis_client.set(f"nft:{nft_id}", json.dumps(nft_data))
        print(f"Added {len(nfts)} NFTs.")
        
        # Sample quests
        quests = {
            "quest_1": {
                "quest_id": "quest_1",
                "user_id": "user_1",
                "title": "Quantum Chip Design",
                "description": "Design a quantum processor with 128 cores",
                "status": "completed",
                "reward": "nft_quantum_designer",
                "timestamp": datetime.now().isoformat()
            },
            "quest_2": {
                "quest_id": "quest_2",
                "user_id": "user_2",
                "title": "Neural Network Optimization",
                "description": "Optimize neural network processing efficiency",
                "status": "active",
                "reward": "nft_neural_expert",
                "timestamp": (datetime.now() - timedelta(days=1)).isoformat()
            }
        }
        
        # Store quests
        for quest_id, quest_data in quests.items():
            await redis_client.set(f"quest:{quest_id}", json.dumps(quest_data))
        print(f"Added {len(quests)} quests.")
        
        # Sample configuration data
        config_data = {
            "system": {
                "version": "11.0.0",
                "mode": "production",
                "maintenance": False
            },
            "subscription_price": 10,
            "supported_fabs": ["TSMC", "Intel", "Samsung"],
            "supported_protocols": ["MQTT", "OPC_UA"]
        }
        
        # Store configuration
        await redis_client.set("config:system", json.dumps(config_data))
        print("Added system configuration.")
        
        # Sample analytics data
        analytics_data = {
            "chip_metrics": {
                "chip_quantum_1": {
                    "performance": 95.5,
                    "efficiency": 87.2,
                    "temperature": 45.3,
                    "last_updated": datetime.now().isoformat()
                },
                "chip_neural_1": {
                    "performance": 82.1,
                    "efficiency": 91.7,
                    "temperature": 38.9,
                    "last_updated": datetime.now().isoformat()
                }
            }
        }
        
        # Store analytics
        await redis_client.set("analytics:metrics", json.dumps(analytics_data))
        print("Added analytics data.")
        
        print("\nDemo data initialization completed successfully!")
        print("\nSummary:")
        print(f"- Users: {len(users)}")
        print(f"- Chip Drivers: {len(drivers)}")
        print(f"- Collaborations: {len(collaborations)}")
        print(f"- Processes: {len(processes)}")
        print(f"- NFTs: {len(nfts)}")
        print(f"- Quests: {len(quests)}")
        
    except Exception as e:
        print(f"Error initializing demo data: {e}")
    finally:
        await redis_client.close()

if __name__ == "__main__":
    asyncio.run(init_demo_data())