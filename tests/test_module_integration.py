"""
Integration test for Redis optimization with existing modules in GlobalScope MultiFrame 11.0
This file tests the integration of the optimized Redis client with existing system modules.
"""
import pytest
import asyncio
import json
from src.chip_design.family_collaboration_engine import FamilyCollaborationEngine
from src.chip_design.chip_driver_generator import ChipDriverGenerator
from src.lib.redis_client import redis_client

@pytest.mark.asyncio
async def test_family_collaboration_engine_integration():
    """Test FamilyCollaborationEngine integration with optimized Redis client"""
    # Create engine instance
    engine = FamilyCollaborationEngine()
    
    # Test starting a collaboration
    chip_data = {
        "type": "quantum_processor",
        "cores": 128,
        "frequency": "4.5GHz"
    }
    
    result = await engine.start_collaboration(
        user_id="test_user",
        chip_id="test_chip_1",
        chip_data=chip_data,
        collaborators=["collab_user_1", "collab_user_2"],
        lang="uk"
    )
    
    assert result["status"] == "success"
    assert "collab_id" in result
    assert result["chip_id"] == "test_chip_1"
    
    # Test updating a collaboration
    update_result = await engine.update_collaboration(
        user_id="test_user",
        collab_id=result["collab_id"],
        update_data={"status": "in_progress"},
        lang="uk"
    )
    
    assert update_result["status"] == "success"
    assert update_result["collab_id"] == result["collab_id"]

@pytest.mark.asyncio
async def test_chip_driver_generator_integration():
    """Test ChipDriverGenerator integration with optimized Redis client"""
    # Create generator instance
    generator = ChipDriverGenerator()
    
    # Test generating a driver
    chip_data = {
        "type": "neural_processor",
        "cores": 64,
        "frequency": "3.2GHz"
    }
    
    result = await generator.generate_driver(
        user_id="test_user",
        chip_id="test_chip_2",
        chip_data=chip_data,
        lang="uk"
    )
    
    assert result["status"] == "success"
    assert "driver_id" in result
    assert result["chip_id"] == "test_chip_2"
    
    # Test updating firmware
    update_result = await generator.update_firmware(
        user_id="test_user",
        driver_id=result["driver_id"],
        update_data={"version": "2.0.0", "status": "updated"},
        lang="uk"
    )
    
    assert update_result["status"] == "success"
    assert update_result["driver_id"] == result["driver_id"]

@pytest.mark.asyncio
async def test_redis_data_persistence():
    """Test that data is properly persisted in Redis"""
    # Test family collaboration data
    collab_keys = await redis_client.keys("collab:*")
    assert len(collab_keys) > 0
    
    # Test driver data
    driver_keys = await redis_client.keys("driver:*")
    assert len(driver_keys) > 0
    
    # Verify data can be retrieved
    for key in collab_keys[:1]:  # Test first collaboration
        data = await redis_client.get_json(key)
        assert data is not None
        assert "collab_id" in data
    
    for key in driver_keys[:1]:  # Test first driver
        data = await redis_client.get_json(key)
        assert data is not None
        assert "driver_id" in data

@pytest.mark.asyncio
async def test_counter_functionality():
    """Test Redis counter functionality"""
    # Test collaboration counter
    initial_collab_count = await redis_client.get("collab_counter")
    initial_collab_count = int(initial_collab_count) if initial_collab_count else 0
    
    # Test driver counter
    initial_driver_count = await redis_client.get("driver_counter")
    initial_driver_count = int(initial_driver_count) if initial_driver_count else 0
    
    # Create new collaboration
    engine = FamilyCollaborationEngine()
    chip_data = {"type": "test_chip", "cores": 32}
    await engine.start_collaboration(
        user_id="test_user",
        chip_id="test_chip_3",
        chip_data=chip_data,
        collaborators=[],
        lang="uk"
    )
    
    # Create new driver
    generator = ChipDriverGenerator()
    await generator.generate_driver(
        user_id="test_user",
        chip_id="test_chip_4",
        chip_data=chip_data,
        lang="uk"
    )
    
    # Check that counters were incremented
    new_collab_count = await redis_client.get("collab_counter")
    new_collab_count = int(new_collab_count) if new_collab_count else 0
    
    new_driver_count = await redis_client.get("driver_counter")
    new_driver_count = int(new_driver_count) if new_driver_count else 0
    
    assert new_collab_count > initial_collab_count
    assert new_driver_count > initial_driver_count

@pytest.mark.asyncio
async def test_caching_integration():
    """Test caching integration with module operations"""
    # Create test data
    test_key = "cache_integration_test"
    test_value = {"test": "data", "id": 123}
    
    # Set data with caching
    await redis_client.set_json(test_key, test_value, use_cache=True)
    
    # Verify data is cached
    assert test_key in redis_client.cache
    
    # Retrieve data (should use cache)
    retrieved_value = await redis_client.get_json(test_key, use_cache=True)
    assert retrieved_value == test_value
    
    # Verify cache hit
    # (In a more comprehensive test, we would check cache hit metrics)

if __name__ == "__main__":
    # Run integration tests
    asyncio.run(test_family_collaboration_engine_integration())
    asyncio.run(test_chip_driver_generator_integration())
    asyncio.run(test_redis_data_persistence())
    asyncio.run(test_counter_functionality())
    asyncio.run(test_caching_integration())
    
    print("All module integration tests passed!")