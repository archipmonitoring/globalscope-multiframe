"""
Test file for Analytics optimization enhancements in GlobalScope MultiFrame 11.0
This file tests the optimized analytics module and its integration with the optimized Redis client.
"""
import pytest
import asyncio
from src.analytics.chip_analytics import ChipAnalytics

@pytest.mark.asyncio
async def test_analytics_collect_metrics():
    """Test collecting metrics with optimized analytics"""
    analytics = ChipAnalytics()
    
    # Test collecting metrics
    chip_id = "test_chip_analytics_1"
    metrics = await analytics.collect_metrics(chip_id)
    
    assert metrics["chip_id"] == chip_id
    assert "defect_rate" in metrics
    assert "yield" in metrics
    assert "energy_consumption" in metrics
    assert "timestamp" in metrics

@pytest.mark.asyncio
async def test_analytics_get_metrics():
    """Test getting metrics with caching"""
    analytics = ChipAnalytics()
    
    # First, collect some metrics
    chip_id = "test_chip_analytics_2"
    await analytics.collect_metrics(chip_id)
    
    # Then retrieve them
    metrics = await analytics.get_metrics(chip_id)
    
    assert metrics["chip_id"] == chip_id
    assert "defect_rate" in metrics
    assert "yield" in metrics
    assert "energy_consumption" in metrics

@pytest.mark.asyncio
async def test_analytics_trend_analysis():
    """Test trend analysis with caching"""
    analytics = ChipAnalytics()
    
    # Collect multiple metrics over time
    chip_id = "test_chip_analytics_3"
    for i in range(5):
        await analytics.collect_metrics(chip_id)
    
    # Analyze trends
    trends = await analytics.analyze_trends(chip_id, hours=24)
    
    assert trends["status"] == "success"
    assert trends["chip_id"] == chip_id
    assert "trends" in trends
    assert len(trends["trends"]) > 0

@pytest.mark.asyncio
async def test_analytics_caching_performance():
    """Test caching performance improvements"""
    analytics = ChipAnalytics()
    
    # Collect metrics
    chip_id = "test_chip_analytics_4"
    await analytics.collect_metrics(chip_id)
    
    # First retrieval (no cache)
    metrics1 = await analytics.get_metrics(chip_id)
    
    # Second retrieval (should use cache)
    metrics2 = await analytics.get_metrics(chip_id)
    
    # Both should be the same
    assert metrics1 == metrics2

@pytest.mark.asyncio
async def test_analytics_error_handling():
    """Test error handling for non-existent chips"""
    analytics = ChipAnalytics()
    
    # Try to get metrics for non-existent chip
    metrics = await analytics.get_metrics("non_existent_chip")
    
    assert metrics["status"] == "error"
    assert "message" in metrics

if __name__ == "__main__":
    # Run tests
    asyncio.run(test_analytics_collect_metrics())
    asyncio.run(test_analytics_get_metrics())
    asyncio.run(test_analytics_trend_analysis())
    asyncio.run(test_analytics_caching_performance())
    asyncio.run(test_analytics_error_handling())
    
    print("All analytics optimization tests passed!")