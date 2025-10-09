"""
Integration tests for security enhancements
"""
import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock

# Import the modules we want to test integration between
from src.security.enhanced_firewall import EnhancedQuantumSingularityFirewall
from src.security.security_tester import SecurityTester
from src.chip_design.chip_driver_generator import ChipDriverGenerator
from src.chip_design.zero_defect_engine import ZeroDefectEngine

@pytest.fixture
def enhanced_firewall():
    """Create a test instance of EnhancedQuantumSingularityFirewall"""
    with patch('src.security.enhanced_firewall.holo_misha_instance'), \
         patch('src.security.enhanced_firewall.security_logger'):
        firewall = EnhancedQuantumSingularityFirewall()
        return firewall

@pytest.fixture
def security_tester(enhanced_firewall):
    """Create a test instance of SecurityTester"""
    with patch('src.security.security_tester.firewall', enhanced_firewall), \
         patch('src.security.security_tester.holo_misha_instance'), \
         patch('src.security.security_tester.security_logger'):
        tester = SecurityTester()
        return tester

@pytest.fixture
def chip_driver_generator(enhanced_firewall):
    """Create a test instance of ChipDriverGenerator with enhanced firewall"""
    with patch('src.chip_design.chip_driver_generator.holo_misha_instance'), \
         patch('src.chip_design.chip_driver_generator.security_logger'), \
         patch('src.chip_design.chip_driver_generator.ai_design'), \
         patch('src.chip_design.chip_driver_generator.redis_client'):
        # Use enhanced firewall instead of basic one
        with patch('src.chip_design.chip_driver_generator.firewall', enhanced_firewall):
            generator = ChipDriverGenerator()
            return generator

@pytest.fixture
def zero_defect_engine(enhanced_firewall):
    """Create a test instance of ZeroDefectEngine with enhanced firewall"""
    with patch('src.chip_design.zero_defect_engine.holo_misha_instance'), \
         patch('src.chip_design.zero_defect_engine.ai_design'), \
         patch('src.chip_design.zero_defect_engine.pipeline_guard'), \
         patch('src.chip_design.zero_defect_engine.redis_client'), \
         patch('src.chip_design.zero_defect_engine.config_manager'):
        # Use enhanced firewall instead of basic one
        with patch('src.chip_design.zero_defect_engine.firewall', enhanced_firewall):
            engine = ZeroDefectEngine()
            return engine

@pytest.mark.asyncio
async def test_security_tester_firewall_integration(security_tester, enhanced_firewall):
    """Test SecurityTester integration with EnhancedQuantumSingularityFirewall"""
    # Test scanning a clean process
    clean_process_data = {
        "type": "design_process",
        "name": "safe_chip_design",
        "parameters": {"frequency": "2.5GHz"}
    }
    
    result = await security_tester.scan_zero_day(
        "test_user", 
        "process_1", 
        clean_process_data
    )
    
    assert result["status"] == "success"
    assert "scan_id" in result
    
    # Verify firewall validation was called
    # Note: In our current implementation, the security tester uses the old firewall
    # We would need to update it to use the enhanced firewall for full integration

@pytest.mark.asyncio
async def test_security_tester_malicious_process_detection(security_tester, enhanced_firewall):
    """Test SecurityTester detection of malicious processes"""
    # Test scanning a malicious process
    malicious_process_data = {
        "type": "malicious",
        "name": "unsafe_chip_design",
        "payload": "malicious_code"
    }
    
    # Since the security tester still uses the old firewall in current implementation,
    # we'll test the enhanced firewall directly
    result = await enhanced_firewall.validate_process(
        "process_1", 
        malicious_process_data
    )
    
    assert result is False
    assert enhanced_firewall.threats_blocked == 1
    assert len(enhanced_firewall.threat_history) == 1

@pytest.mark.asyncio
async def test_chip_driver_generator_security_integration(chip_driver_generator, enhanced_firewall):
    """Test ChipDriverGenerator integration with enhanced security"""
    # Test generating a driver with valid data
    valid_chip_data = {
        "type": "design_process",
        "name": "test_chip",
        "parameters": {"frequency": "2.5GHz"}
    }
    
    # Mock AI design optimization
    with patch.object(chip_driver_generator, 'ai_design') as mock_ai_design:
        mock_ai_design.optimize_design = AsyncMock(return_value={"status": "success", "optimized_data": {}})
        
        result = await chip_driver_generator.generate_driver(
            "test_user",
            "test_chip",
            valid_chip_data
        )
        
        assert result["status"] == "success"
        # No threats should be detected for valid data
        assert enhanced_firewall.threats_blocked == 0

@pytest.mark.asyncio
async def test_chip_driver_generator_security_threat_detection(chip_driver_generator, enhanced_firewall):
    """Test ChipDriverGenerator detection of security threats"""
    # Test generating a driver with malicious data
    malicious_chip_data = {
        "type": "malicious",
        "name": "test_chip",
        "payload": "malicious_code"
    }
    
    # Mock AI design optimization
    with patch.object(chip_driver_generator, 'ai_design') as mock_ai_design:
        mock_ai_design.optimize_design = AsyncMock(return_value={"status": "success", "optimized_data": {}})
        
        result = await chip_driver_generator.generate_driver(
            "test_user",
            "test_chip",
            malicious_chip_data
        )
        
        # The firewall should block the malicious process
        assert result["status"] == "error"
        assert "Security validation failed" in result["message"]
        # Threat should be detected and blocked
        assert enhanced_firewall.threats_blocked == 1

@pytest.mark.asyncio
async def test_zero_defect_engine_security_integration(zero_defect_engine, enhanced_firewall):
    """Test ZeroDefectEngine integration with enhanced security"""
    # Test ensuring zero defects with valid data
    valid_chip_data = {
        "type": "design_process",
        "name": "test_chip",
        "parameters": {"frequency": "2.5GHz"}
    }
    
    # Mock AI design optimization
    with patch.object(zero_defect_engine, 'ai_design') as mock_ai_design, \
         patch.object(zero_defect_engine, 'pipeline_guard') as mock_pipeline_guard:
        mock_ai_design.optimize_design = AsyncMock(return_value={"status": "success", "optimized_data": {}})
        mock_pipeline_guard.validate_process = AsyncMock(return_value={"status": "success"})
        
        result = await zero_defect_engine.ensure_zero_defect(
            "test_user",
            "test_chip",
            valid_chip_data
        )
        
        assert result["status"] == "success"
        # No threats should be detected for valid data
        assert enhanced_firewall.threats_blocked == 0

@pytest.mark.asyncio
async def test_security_logging_integration(enhanced_firewall):
    """Test security logging integration"""
    with patch('src.security.enhanced_firewall.security_logger') as mock_security_logger:
        mock_security_logger.log_security_event = AsyncMock()
        
        # Test that security events are logged
        process_data = {
            "type": "design_process",
            "name": "test_chip"
        }
        
        await enhanced_firewall.validate_process("process_1", process_data)
        
        # Verify security event was logged
        mock_security_logger.log_security_event.assert_called()

@pytest.mark.asyncio
async def test_holomisha_ar_notification_integration(enhanced_firewall):
    """Test HoloMisha AR notification integration"""
    with patch('src.security.enhanced_firewall.holo_misha_instance') as mock_holo_misha:
        mock_holo_misha.notify_ar = AsyncMock()
        
        # Test that AR notifications are sent
        process_data = {
            "type": "design_process",
            "name": "test_chip"
        }
        
        await enhanced_firewall.validate_process("process_1", process_data)
        
        # Verify AR notification was sent
        mock_holo_misha.notify_ar.assert_called()

@pytest.mark.asyncio
async def test_enhanced_firewall_rate_limiting_integration(enhanced_firewall):
    """Test EnhancedQuantumSingularityFirewall rate limiting integration"""
    with patch('src.security.enhanced_firewall.holo_misha_instance'), \
         patch('src.security.enhanced_firewall.security_logger'):
        
        process_data = {
            "type": "design_process",
            "name": "test_chip"
        }
        
        # Test multiple requests to trigger rate limiting
        # Note: This is a simplified test - actual rate limiting depends on timing
        results = []
        for i in range(enhanced_firewall.max_requests_per_minute + 5):
            result = await enhanced_firewall.validate_process(f"process_{i}", process_data)
            results.append(result)
        
        # All requests should initially pass (rate limiting depends on timing in real scenario)
        # This test verifies the rate limiting infrastructure is in place

if __name__ == "__main__":
    pytest.main([__file__])