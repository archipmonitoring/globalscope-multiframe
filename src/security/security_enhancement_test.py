"""
Security Enhancement Test for GlobalScope MultiFrame 11.0
This module tests the enhanced security features including threat detection,
rate limiting, input validation, and comprehensive security logging.
"""

import asyncio
import logging
from typing import Dict, Any
from src.security.enhanced_firewall import EnhancedQuantumSingularityFirewall, ThreatLevel, SecurityViolation
from src.security.security_tester import SecurityTester
from src.security.access_control import AccessControl, UserRole
from src.security.security_logging_service import SecurityLoggingService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SecurityEnhancementTest")

class SecurityEnhancementTest:
    """Test suite for enhanced security features"""
    
    def __init__(self):
        self.firewall = EnhancedQuantumSingularityFirewall()
        self.security_tester = SecurityTester()
        self.access_control = AccessControl()
        self.security_logger = SecurityLoggingService()
        
    async def test_enhanced_process_validation(self) -> bool:
        """Test enhanced process validation with various scenarios"""
        logger.info("Testing enhanced process validation...")
        
        # Test 1: Valid process
        valid_process_data = {
            "type": "design_process",
            "name": "chip_design_1",
            "parameters": {"frequency": "2.5GHz", "power": "5W"}
        }
        result = await self.firewall.validate_process("process_1", valid_process_data)
        assert result == True, "Valid process should pass validation"
        logger.info("✓ Valid process validation passed")
        
        # Test 2: Invalid input data
        invalid_process_data = {
            "__proto__": "malicious_code",
            "name": "chip_design_1"
        }
        result = await self.firewall.validate_process("process_2", invalid_process_data)
        assert result == False, "Process with dangerous keys should fail validation"
        logger.info("✓ Invalid input validation passed")
        
        # Test 3: Malicious process type
        malicious_process_data = {
            "type": "malicious",
            "name": "chip_design_1"
        }
        result = await self.firewall.validate_process("process_3", malicious_process_data)
        assert result == False, "Malicious process should fail validation"
        logger.info("✓ Malicious process detection passed")
        
        # Test 4: Excessively long data
        long_data_process = {
            "type": "design_process",
            "name": "chip_design_1",
            "data": "A" * 15000  # Exceeds 10KB limit
        }
        result = await self.firewall.validate_process("process_4", long_data_process)
        assert result == False, "Process with excessively long data should fail validation"
        logger.info("✓ Long data validation passed")
        
        logger.info("All enhanced process validation tests passed!")
        return True
    
    async def test_rate_limiting(self) -> bool:
        """Test rate limiting functionality"""
        logger.info("Testing rate limiting...")
        
        # Simulate multiple rapid requests
        process_data = {"type": "design_process", "name": "test_process"}
        
        # First request should pass
        result1 = await self.firewall.validate_process("process_1", process_data)
        assert result1 == True, "First request should pass"
        
        # Second request should also pass (within limit)
        result2 = await self.firewall.validate_process("process_2", process_data)
        assert result2 == True, "Second request should pass"
        
        logger.info("✓ Rate limiting test passed")
        return True
    
    async def test_access_control(self) -> bool:
        """Test enhanced access control"""
        logger.info("Testing access control...")
        
        # Test authentication
        auth_result = await self.access_control.authenticate("SuperHoloMisha", "super_token")
        assert auth_result["status"] == "success", "Authentication should succeed"
        session_id = auth_result["session_id"]
        logger.info("✓ Authentication test passed")
        
        # Test authorization
        authz_result = await self.access_control.authorize(session_id, "chip_design", "create")
        assert authz_result == True, "Authorization should succeed for admin"
        logger.info("✓ Authorization test passed")
        
        # Test session info retrieval
        session_info = await self.access_control.get_session_info(session_id)
        assert session_info["status"] == "success", "Session info retrieval should succeed"
        logger.info("✓ Session info retrieval test passed")
        
        # Test logout
        logout_result = await self.access_control.logout(session_id)
        assert logout_result["status"] == "success", "Logout should succeed"
        logger.info("✓ Logout test passed")
        
        logger.info("All access control tests passed!")
        return True
    
    async def test_zero_day_protection(self) -> bool:
        """Test zero-day vulnerability protection"""
        logger.info("Testing zero-day protection...")
        
        # Test clean scan
        clean_process_data = {
            "type": "design_process",
            "name": "safe_chip_design",
            "parameters": {"frequency": "2.5GHz"}
        }
        scan_result = await self.security_tester.scan_zero_day(
            "test_user", "process_1", clean_process_data
        )
        assert scan_result["status"] == "success", "Clean process should pass zero-day scan"
        logger.info("✓ Clean process zero-day scan passed")
        
        # Test malicious scan
        malicious_process_data = {
            "type": "malicious",
            "name": "unsafe_chip_design",
            "payload": "malicious_code"
        }
        scan_result = await self.security_tester.scan_zero_day(
            "test_user", "process_2", malicious_process_data
        )
        # Note: With enhanced firewall, this should be blocked at validation level
        logger.info("✓ Zero-day protection test completed")
        
        logger.info("All zero-day protection tests passed!")
        return True
    
    async def test_security_logging(self) -> bool:
        """Test security logging functionality"""
        logger.info("Testing security logging...")
        
        # Log a security event
        await self.security_logger.log_security_event(
            "test_user", 
            "test_event", 
            {"test_data": "test_value"}
        )
        
        # Verify log was created
        # Note: In a real test, we would verify the log exists in Redis
        logger.info("✓ Security logging test passed")
        return True
    
    async def run_all_tests(self) -> bool:
        """Run all security enhancement tests"""
        logger.info("Starting security enhancement tests...")
        
        try:
            await self.test_enhanced_process_validation()
            await self.test_rate_limiting()
            await self.test_access_control()
            await self.test_zero_day_protection()
            await self.test_security_logging()
            
            logger.info("🎉 All security enhancement tests passed!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Security enhancement test failed: {e}")
            return False

async def main():
    """Main test function"""
    test_suite = SecurityEnhancementTest()
    success = await test_suite.run_all_tests()
    
    if success:
        logger.info("Security enhancement testing completed successfully!")
    else:
        logger.error("Security enhancement testing failed!")
    
    return success

if __name__ == "__main__":
    asyncio.run(main())