"""
Performance tests for security enhancements
"""
import pytest
import asyncio
import time
from unittest.mock import Mock, patch, AsyncMock

# Import the modules we want to test
from src.security.enhanced_firewall import EnhancedQuantumSingularityFirewall

@pytest.fixture
def enhanced_firewall():
    """Create a test instance of EnhancedQuantumSingularityFirewall"""
    with patch('src.security.enhanced_firewall.holo_misha_instance'), \
         patch('src.security.enhanced_firewall.security_logger'):
        firewall = EnhancedQuantumSingularityFirewall()
        return firewall

@pytest.mark.asyncio
async def test_firewall_process_validation_performance(enhanced_firewall):
    """Test firewall process validation performance"""
    # Test valid process validation performance
    valid_process_data = {
        "type": "design_process",
        "name": "test_chip",
        "parameters": {"frequency": "2.5GHz"}
    }
    
    start_time = time.time()
    
    # Perform multiple validations
    for i in range(1000):
        result = await enhanced_firewall.validate_process(f"process_{i}", valid_process_data)
        assert result is True
    
    end_time = time.time()
    validation_time = end_time - start_time
    
    # Validations should be efficient
    assert validation_time < 5.0  # Should complete within 5 seconds
    assert enhanced_firewall.threats_blocked == 0

@pytest.mark.asyncio
async def test_firewall_threat_detection_performance(enhanced_firewall):
    """Test firewall threat detection performance"""
    # Test malicious process detection performance
    malicious_process_data = {
        "type": "malicious",
        "name": "test_chip",
        "payload": "malicious_code"
    }
    
    start_time = time.time()
    
    # Perform multiple threat detections
    for i in range(1000):
        result = await enhanced_firewall.validate_process(f"process_{i}", malicious_process_data)
        assert result is False
    
    end_time = time.time()
    detection_time = end_time - start_time
    
    # Threat detections should be efficient
    assert detection_time < 5.0  # Should complete within 5 seconds
    assert enhanced_firewall.threats_blocked == 1000

@pytest.mark.asyncio
async def test_firewall_input_validation_performance(enhanced_firewall):
    """Test firewall input validation performance"""
    # Test input validation performance with various data
    test_cases = [
        # Valid data
        {"type": "design_process", "name": "test_chip"},
        # Invalid data with dangerous keys
        {"__proto__": "malicious", "name": "test_chip"},
        # Invalid data with long values
        {"type": "design_process", "data": "A" * 15000},
        # Valid complex data
        {"type": "design_process", "name": "test_chip", "params": {"nested": {"deep": "value"}}}
    ]
    
    start_time = time.time()
    
    # Perform multiple validations for each test case
    for test_case in test_cases:
        for i in range(100):
            await enhanced_firewall._validate_input(test_case)
    
    end_time = time.time()
    validation_time = end_time - start_time
    
    # Input validation should be efficient
    assert validation_time < 2.0  # Should complete within 2 seconds

@pytest.mark.asyncio
async def test_firewall_rate_limiting_performance(enhanced_firewall):
    """Test firewall rate limiting performance"""
    valid_process_data = {
        "type": "design_process",
        "name": "test_chip"
    }
    
    start_time = time.time()
    
    # Test rate limiting with multiple identifiers
    for identifier in range(100):
        for request in range(enhanced_firewall.max_requests_per_minute + 10):
            result = await enhanced_firewall._check_rate_limit(f"user_{identifier}")
            # Rate limiting check should be fast
            assert isinstance(result, bool)
    
    end_time = time.time()
    rate_limiting_time = end_time - start_time
    
    # Rate limiting should be efficient
    assert rate_limiting_time < 3.0  # Should complete within 3 seconds

@pytest.mark.asyncio
async def test_firewall_suspicious_activity_detection_performance(enhanced_firewall):
    """Test firewall suspicious activity detection performance"""
    start_time = time.time()
    
    # Test suspicious activity detection with multiple identifiers
    for identifier in range(1000):
        result = await enhanced_firewall._is_suspicious_activity(f"user_{identifier}")
        # Suspicious activity check should be fast
        assert isinstance(result, bool)
    
    end_time = time.time()
    suspicious_detection_time = end_time - start_time
    
    # Suspicious activity detection should be efficient
    assert suspicious_detection_time < 2.0  # Should complete within 2 seconds

@pytest.mark.asyncio
async def test_firewall_zkp_operations_performance(enhanced_firewall):
    """Test firewall ZKP operations performance"""
    test_data = {"key": "value", "number": 42}
    
    start_time = time.time()
    
    # Test ZKP generation performance
    for i in range(100):
        result = await enhanced_firewall.generate_zkp(test_data)
        assert "proof" in result
        assert "data" in result
    
    end_time = time.time()
    zkp_generation_time = end_time - start_time
    
    # Reset mock for verification operations
    start_time = time.time()
    
    # Test ZKP verification performance
    proof_data = {"proof": "test_proof", "data": test_data}
    for i in range(100):
        result = await enhanced_firewall.verify_zkp(proof_data, "public_input")
        assert result is True
    
    end_time = time.time()
    zkp_verification_time = end_time - start_time
    
    # ZKP operations should be efficient
    assert zkp_generation_time < 5.0  # Should complete within 5 seconds
    assert zkp_verification_time < 5.0  # Should complete within 5 seconds

@pytest.mark.asyncio
async def test_firewall_encryption_decryption_performance(enhanced_firewall):
    """Test firewall encryption/decryption performance"""
    test_data = "sensitive_data_for_testing" * 10
    key = "encryption_key_for_testing"
    
    start_time = time.time()
    
    # Test encryption performance
    encrypted_data_list = []
    for i in range(100):
        encrypted = await enhanced_firewall.encrypt_data(test_data, key)
        encrypted_data_list.append(encrypted)
        assert encrypted is not None
        assert isinstance(encrypted, str)
    
    end_time = time.time()
    encryption_time = end_time - start_time
    
    # Test decryption performance
    start_time = time.time()
    
    for encrypted_data in encrypted_data_list:
        decrypted = await enhanced_firewall.decrypt_data(encrypted_data, key)
        assert decrypted is not None
    
    end_time = time.time()
    decryption_time = end_time - start_time
    
    # Encryption/decryption should be efficient
    assert encryption_time < 3.0  # Should complete within 3 seconds
    assert decryption_time < 3.0  # Should complete within 3 seconds

@pytest.mark.asyncio
async def test_firewall_concurrent_performance(enhanced_firewall):
    """Test firewall concurrent performance"""
    valid_process_data = {
        "type": "design_process",
        "name": "test_chip",
        "parameters": {"frequency": "2.5GHz"}
    }
    
    # Test concurrent process validations
    async def validate_process(identifier):
        return await enhanced_firewall.validate_process(f"process_{identifier}", valid_process_data)
    
    start_time = time.time()
    
    # Run multiple concurrent validations
    tasks = [validate_process(i) for i in range(100)]
    results = await asyncio.gather(*tasks)
    
    end_time = time.time()
    concurrent_time = end_time - start_time
    
    # All validations should succeed
    assert len(results) == 100
    assert all(result is True for result in results)
    
    # Concurrent operations should be efficient
    assert concurrent_time < 3.0  # Should complete within 3 seconds

if __name__ == "__main__":
    pytest.main([__file__])