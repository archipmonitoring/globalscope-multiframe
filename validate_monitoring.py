"""
Simple validation script for API monitoring enhancements in GlobalScope MultiFrame 11.0
This script tests the enhanced monitoring capabilities added to the API.
"""
import asyncio
import sys
import os

# Add src to path to import modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_api_monitoring():
    """Test the API monitoring enhancements"""
    try:
        # Import the monitoring modules
        from src.monitoring.api_monitor import api_monitor, record_request, get_system_health, get_all_metrics
        from src.monitoring.dashboard import dashboard
        
        print("✓ Successfully imported monitoring modules")
        
        # Test API monitor initialization
        assert api_monitor is not None
        assert api_monitor.total_requests == 0
        assert api_monitor.total_errors == 0
        assert len(api_monitor.endpoints) == 0
        print("✓ API monitor initialization test passed")
        
        # Test recording requests
        record_request("/test/endpoint", 0.1, 200, True)
        assert api_monitor.total_requests == 1
        assert api_monitor.total_errors == 0
        assert "/test/endpoint" in api_monitor.endpoints
        print("✓ Request recording test passed")
        
        # Test system health
        health = get_system_health()
        assert "status" in health
        assert "timestamp" in health
        print("✓ System health test passed")
        
        # Test all metrics
        metrics = get_all_metrics()
        assert "system_health" in metrics
        assert "endpoint_metrics" in metrics
        print("✓ All metrics test passed")
        
        # Test async dashboard functions
        async def test_dashboard():
            overview = await dashboard.get_system_overview()
            assert "timestamp" in overview
            assert "system_status" in overview
            print("✓ Dashboard system overview test passed")
            
            metrics = await dashboard.get_detailed_api_metrics()
            assert "timestamp" in metrics
            assert "system_health" in metrics
            print("✓ Dashboard detailed metrics test passed")
            
            report = await dashboard.get_security_report()
            assert "timestamp" in report
            assert "threats_blocked" in report
            print("✓ Dashboard security report test passed")
        
        # Run async tests
        asyncio.run(test_dashboard())
        
        print("\n🎉 All monitoring validation tests passed!")
        print("The API monitoring enhancements are working correctly.")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing API monitoring enhancements...")
    print("=" * 50)
    
    success = test_api_monitoring()
    
    if success:
        print("\n✅ Monitoring validation completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Monitoring validation failed!")
        sys.exit(1)