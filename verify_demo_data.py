#!/usr/bin/env python3
"""
Demo Data Verification Script for GlobalScope MultiFrame 11.0
This script verifies that Redis contains the expected demo data.
"""
import asyncio
import json
from redis.asyncio import Redis

async def verify_demo_data():
    """Verify that Redis contains the expected demo data."""
    # Connect to Redis
    redis_client = Redis(host="localhost", port=6379, decode_responses=True)
    
    try:
        # Test connection
        await redis_client.ping()
        print("Connected to Redis successfully!")
        
        # Verify counters
        counters = ['driver_counter', 'collab_counter', 'process_counter', 'quest_counter', 'nft_counter']
        print("\n--- Counters ---")
        for counter in counters:
            value = await redis_client.get(counter)
            print(f"{counter}: {value}")
        
        # Verify users
        print("\n--- Users ---")
        users = await redis_client.keys("user:*")
        for user_key in users:
            user_data = await redis_client.get(user_key)
            user = json.loads(user_data)
            print(f"User: {user['username']} ({user['role']}) - {user['email']}")
        
        # Verify drivers
        print("\n--- Chip Drivers ---")
        drivers = await redis_client.keys("driver:*")
        for driver_key in drivers:
            driver_data = await redis_client.get(driver_key)
            driver = json.loads(driver_data)
            print(f"Driver: {driver['driver_id']} for {driver['chip_id']} (v{driver['version']}) - {driver['status']}")
        
        # Verify collaborations
        print("\n--- Collaborations ---")
        collaborations = await redis_client.keys("collab:*")
        for collab_key in collaborations:
            collab_data = await redis_client.get(collab_key)
            collab = json.loads(collab_data)
            collaborators = ', '.join(collab['collaborators']) if collab['collaborators'] else 'None'
            print(f"Collaboration: {collab['collab_id']} for {collab['chip_id']} - {collab['status']} (Collaborators: {collaborators})")
        
        # Verify processes
        print("\n--- Chip Processes ---")
        processes = await redis_client.keys("process:*")
        for process_key in processes:
            process_data = await redis_client.get(process_key)
            process = json.loads(process_data)
            print(f"Process: {process['process_id']} - {process['status']}")
        
        # Verify NFTs
        print("\n--- NFTs ---")
        nfts = await redis_client.keys("nft:*")
        for nft_key in nfts:
            nft_data = await redis_client.get(nft_key)
            nft = json.loads(nft_data)
            print(f"NFT: {nft['nft_id']} for {nft['chip_id']} - Owner: {nft['owner'][:10]}...")
        
        # Verify quests
        print("\n--- Quests ---")
        quests = await redis_client.keys("quest:*")
        for quest_key in quests:
            quest_data = await redis_client.get(quest_key)
            quest = json.loads(quest_data)
            print(f"Quest: {quest['title']} - {quest['status']}")
        
        # Verify configuration
        print("\n--- Configuration ---")
        config_data = await redis_client.get("config:system")
        if config_data:
            config = json.loads(config_data)
            print(f"System Version: {config['system']['version']}")
            print(f"Mode: {config['system']['mode']}")
        
        # Verify analytics
        print("\n--- Analytics ---")
        analytics_data = await redis_client.get("analytics:metrics")
        if analytics_data:
            analytics = json.loads(analytics_data)
            chips = analytics.get('chip_metrics', {})
            for chip_id, metrics in chips.items():
                print(f"Chip: {chip_id} - Performance: {metrics['performance']}%")
        
        print("\nDemo data verification completed!")
        
    except Exception as e:
        print(f"Error verifying demo data: {e}")
    finally:
        await redis_client.close()

if __name__ == "__main__":
    asyncio.run(verify_demo_data())