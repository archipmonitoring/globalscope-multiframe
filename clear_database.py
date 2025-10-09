#!/usr/bin/env python3
"""
Database Clearing Script for GlobalScope MultiFrame 11.0
This script clears all data from Redis.
"""
import asyncio
import json
from redis.asyncio import Redis

async def clear_database():
    """Clear all data from Redis."""
    # Connect to Redis
    redis_client = Redis(host="localhost", port=6379, decode_responses=True)
    
    try:
        # Test connection
        await redis_client.ping()
        print("Connected to Redis successfully!")
        
        # Get current key count
        initial_count = await redis_client.dbsize()
        print(f"Current database contains {initial_count} keys.")
        
        # Confirm before clearing
        confirmation = input("Are you sure you want to clear all data? Type 'yes' to confirm: ")
        if confirmation.lower() != 'yes':
            print("Database clearing cancelled.")
            return
        
        # Clear all data
        await redis_client.flushall()
        print("Database cleared successfully!")
        
        # Verify clearing
        final_count = await redis_client.dbsize()
        print(f"Database now contains {final_count} keys.")
        
    except Exception as e:
        print(f"Error clearing database: {e}")
    finally:
        await redis_client.close()

if __name__ == "__main__":
    asyncio.run(clear_database())