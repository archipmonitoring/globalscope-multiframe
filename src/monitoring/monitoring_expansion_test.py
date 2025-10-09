"""
Monitoring Expansion Test for GlobalScope MultiFrame 11.0
This module tests the expanded monitoring capabilities.
"""

import asyncio
import logging
from typing import Dict, Any
from src.monitoring.extended_monitor import extended_monitor, get_extended_metrics, get_health_score
from src.monitoring.api_monitor import api_monitor, record_request
from src.monitoring.dashboard import dashboard
from src.lib.utils import get_logger

logger = get_logger("MonitoringExpansionTest")

class MonitoringExpansionTest:
    """Test suite for expanded monitoring capabilities."""
    
    def __init__(self):
        self.extended_monitor = extended_monitor
        self.api_monitor = api_monitor
        self.dashboard = dashboard
    
    async def test_system_metrics(self) -> bool:
        """Test system metrics monitoring."""
        logger.info("Testing system metrics monitoring...")
        
        # Record some API requests to generate metrics
        record_request("/api/test", 0.1, 200, True)
        record_request("/api/test", 0.2, 200, True)
        record_request("/api/error", 0.05, 500, False)
        
        # Get system metrics
        metrics = await self.extended_monitor.get_all_extended_metrics()
        
        # Verify we got system metrics
        assert 'system' in metrics, "System metrics should be present"
        assert 'cpu' in metrics['system'], "CPU metrics should be present"
        assert 'memory' in metrics['system'], "Memory metrics should be present"
        assert 'disk' in metrics['system'], "Disk metrics should be present"
        
        logger.info("✓ System metrics monitoring test passed")
        return True
    
    async def test_redis_metrics(self) -> bool:
        """Test Redis metrics monitoring."""
        logger.info("Testing Redis metrics monitoring...")
        
        # Get Redis metrics
        metrics = await self.extended_monitor.get_all_extended_metrics()
        
        # Verify we got Redis metrics
        assert 'redis' in metrics, "Redis metrics should be present"
        assert 'connected' in metrics['redis'], "Redis connection status should be present"
        
        logger.info("✓ Redis metrics monitoring test passed")
        return True
    
    async def test_security_metrics(self) -> bool:
        """Test security metrics monitoring."""
        logger.info("Testing security metrics monitoring...")
        
        # Get security metrics
        metrics = await self.extended_monitor.get_all_extended_metrics()
        
        # Verify we got security metrics
        assert 'security' in metrics, "Security metrics should be present"
        assert 'firewall' in metrics['security'], "Firewall metrics should be present"
        
        logger.info("✓ Security metrics monitoring test passed")
        return True
    
    async def test_ai_metrics(self) -> bool:
        """Test AI metrics monitoring."""
        logger.info("Testing AI metrics monitoring...")
        
        # Get AI metrics
        metrics = await self.extended_monitor.get_all_extended_metrics()
        
        # Verify we got AI metrics
        assert 'ai' in metrics, "AI metrics should be present"
        
        logger.info("✓ AI metrics monitoring test passed")
        return True
    
    async def test_health_score(self) -> bool:
        """Test health score calculation."""
        logger.info("Testing health score calculation...")
        
        # Get health score
        health_score = await get_health_score()
        
        # Verify we got a health score
        assert 'health_score' in health_score, "Health score should be present"
        assert 'status' in health_score, "Health status should be present"
        
        logger.info(f"✓ Health score calculation test passed (score: {health_score['health_score']})")
        return True
    
    async def test_dashboard_integration(self) -> bool:
        """Test dashboard integration with extended metrics."""
        logger.info("Testing dashboard integration...")
        
        # Get system overview from dashboard
        overview = await self.dashboard.get_system_overview()
        
        # Verify we got system overview
        assert 'system_status' in overview, "System status should be present"
        assert 'timestamp' in overview, "Timestamp should be present"
        
        # Get detailed API metrics
        api_metrics = await self.dashboard.get_detailed_api_metrics()
        
        # Verify we got API metrics
        assert 'system_health' in api_metrics, "System health should be present"
        
        logger.info("✓ Dashboard integration test passed")
        return True
    
    async def run_all_tests(self) -> bool:
        """Run all monitoring expansion tests."""
        logger.info("Starting monitoring expansion tests...")
        
        try:
            await self.test_system_metrics()
            await self.test_redis_metrics()
            await self.test_security_metrics()
            await self.test_ai_metrics()
            await self.test_health_score()
            await self.test_dashboard_integration()
            
            logger.info("🎉 All monitoring expansion tests passed!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Monitoring expansion test failed: {e}")
            return False

async def main():
    """Main test function."""
    test_suite = MonitoringExpansionTest()
    success = await test_suite.run_all_tests()
    
    if success:
        logger.info("Monitoring expansion testing completed successfully!")
    else:
        logger.error("Monitoring expansion testing failed!")
    
    return success

if __name__ == "__main__":
    asyncio.run(main())