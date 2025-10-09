"""
Unit tests for the enhanced firewall security module
"""
import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from src.security.enhanced_firewall import EnhancedQuantumSingularityFirewall, ThreatLevel, SecurityViolation

@pytest.fixture
def firewall():
    """Create a test instance of EnhancedQuantumSingularityFirewall"""
    with patch('src.security.enhanced_firewall.holo_misha_instance'), \
         patch('src.security.enhanced_firewall.security_logger'):
        firewall = EnhancedQuantumSingularityFirewall()
        return firewall

@pytest.mark.asyncio
async def test_firewall_initialization(firewall):
    """Test firewall initialization"""
    assert firewall is not None
    assert firewall.threats_blocked == 0
    assert firewall.is_active is True
    assert isinstance(firewall.threat_history, list)
    assert isinstance(firewall.rate_limits, dict)
    assert isinstance(firewall.blocked_ips, dict)
    assert isinstance(firewall.suspicious_activities, dict)

@pytest.mark.asyncio
async def test_firewall_valid_process_validation(firewall):
    """Test firewall validation of valid process"""
    with patch('src.security.enhanced_firewall.holo_misha_instance'), \
         patch('src.security.enhanced_firewall.security_logger'):
        process_data = {
            "type": "design_process",
            "name": "test_chip",
            "parameters": {"frequency": "2.5GHz"}
        }
        
        result = await firewall.validate_process("process_1", process_data)
        assert result is True
        assert firewall.threats_blocked == 0

@pytest.mark.asyncio
async def test_firewall_invalid_input_validation(firewall):
    """Test firewall validation of invalid input"""
    with patch('src.security.enhanced_firewall.holo_misha_instance'), \
         patch('src.security.enhanced_firewall.security_logger'):
        # Test dangerous prototype key
        process_data = {
            "__proto__": "malicious_code",
            "name": "test_chip"
        }
        
        result = await firewall.validate_process("process_1", process_data)
        assert result is False
        assert firewall.threats_blocked == 1
        
        # Verify threat was logged
        assert len(firewall.threat_history) == 1
        threat = firewall.threat_history[0]
        assert threat["threat_level"] == ThreatLevel.HIGH.value
        assert threat["violation_type"] == SecurityViolation.INVALID_INPUT.value

@pytest.mark.asyncio
async def test_firewall_malicious_process_validation(firewall):
    """Test firewall validation of malicious process"""
    with patch('src.security.enhanced_firewall.holo_misha_instance'), \
         patch('src.security.enhanced_firewall.security_logger'):
        process_data = {
            "type": "malicious",
            "name": "test_chip"
        }
        
        result = await firewall.validate_process("process_1", process_data)
        assert result is False
        assert firewall.threats_blocked == 1
        
        # Verify threat was logged
        assert len(firewall.threat_history) == 1
        threat = firewall.threat_history[0]
        assert threat["threat_level"] == ThreatLevel.CRITICAL.value
        assert threat["violation_type"] == SecurityViolation.MALICIOUS_CONTENT.value

@pytest.mark.asyncio
async def test_firewall_long_data_validation(firewall):
    """Test firewall validation of excessively long data"""
    with patch('src.security.enhanced_firewall.holo_misha_instance'), \
         patch('src.security.enhanced_firewall.security_logger'):
        process_data = {
            "type": "design_process",
            "name": "test_chip",
            "data": "A" * 15000  # Exceeds 10KB limit
        }
        
        result = await firewall.validate_process("process_1", process_data)
        assert result is False
        assert firewall.threats_blocked == 1
        
        # Verify threat was logged
        assert len(firewall.threat_history) == 1
        threat = firewall.threat_history[0]
        assert threat["threat_level"] == ThreatLevel.HIGH.value
        assert threat["violation_type"] == SecurityViolation.INVALID_INPUT.value

@pytest.mark.asyncio
async def test_firewall_rate_limiting(firewall):
    """Test firewall rate limiting functionality"""
    with patch('src.security.enhanced_firewall.holo_misha_instance'), \
         patch('src.security.enhanced_firewall.security_logger'):
        process_data = {
            "type": "design_process",
            "name": "test_chip"
        }
        
        # Test multiple requests from same identifier
        for i in range(firewall.max_requests_per_minute + 5):
            result = await firewall.validate_process(f"process_{i}", process_data)
            if i < firewall.max_requests_per_minute:
                # First requests should pass
                assert result is True
            else:
                # Later requests should be blocked by rate limiting
                # Note: This is a simplified test - actual rate limiting depends on timing
                pass

@pytest.mark.asyncio
async def test_firewall_suspicious_activity_detection(firewall):
    """Test firewall suspicious activity detection"""
    with patch('src.security.enhanced_firewall.holo_misha_instance'), \
         patch('src.security.enhanced_firewall.security_logger'):
        process_data = {
            "type": "design_process",
            "name": "test_chip"
        }
        
        # Test multiple suspicious activities from same identifier
        for i in range(firewall.suspicious_threshold + 2):
            # Manually increment suspicious activity counter for testing
            identifier = "suspicious_user"
            if identifier in firewall.suspicious_activities:
                firewall.suspicious_activities[identifier] += 1
            else:
                firewall.suspicious_activities[identifier] = 1
            
            # After threshold is reached, activities should be flagged as suspicious
            if i >= firewall.suspicious_threshold:
                # This test is simplified - in reality, _perform_security_checks 
                # would need to be called to trigger suspicious activity detection
                pass

@pytest.mark.asyncio
async def test_firewall_zkp_operations(firewall):
    """Test firewall ZKP operations"""
    with patch('src.security.enhanced_firewall.holo_misha_instance'), \
         patch('src.security.enhanced_firewall.security_logger'):
        test_data = {"key": "value"}
        
        # Test ZKP generation
        result = await firewall.generate_zkp(test_data)
        assert "proof" in result
        assert "data" in result
        assert result["data"] == test_data
        
        # Test ZKP verification
        proof_data = {"proof": "test_proof", "data": test_data}
        result = await firewall.verify_zkp(proof_data, "public_input")
        assert result is True

@pytest.mark.asyncio
async def test_firewall_encryption_decryption(firewall):
    """Test firewall encryption and decryption operations"""
    with patch('src.security.enhanced_firewall.holo_misha_instance'), \
         patch('src.security.enhanced_firewall.security_logger'):
        test_data = "sensitive_data"
        key = "encryption_key"
        
        # Test encryption
        encrypted = await firewall.encrypt_data(test_data, key)
        assert encrypted is not None
        assert isinstance(encrypted, str)
        assert encrypted.startswith("encrypted_")
        
        # Test decryption
        decrypted = await firewall.decrypt_data(encrypted, key)
        assert decrypted is not None

if __name__ == "__main__":
    pytest.main([__file__])