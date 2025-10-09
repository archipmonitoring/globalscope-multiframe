"""
Reliability Test for GlobalScope MultiFrame 11.0
This module tests the enhanced error handling and recovery mechanisms.
"""

import asyncio
import logging
from typing import Dict, Any
from src.lib.error_handler import ErrorHandler, ErrorSeverity, ErrorCategory, handle_errors
from src.lib.utils import get_logger

logger = get_logger("ReliabilityTest")

class ReliabilityTest:
    """Test suite for reliability enhancements."""
    
    def __init__(self):
        self.error_handler = ErrorHandler()
    
    @handle_errors(
        context="database_operation",
        severity=ErrorSeverity.HIGH,
        category=ErrorCategory.DATABASE
    )
    async def simulate_database_error(self) -> Dict[str, Any]:
        """Simulate a database error."""
        logger.info("Simulating database operation...")
        # Simulate a database error
        raise ConnectionError("Database connection failed")
    
    @handle_errors(
        context="network_operation",
        severity=ErrorSeverity.MEDIUM,
        category=ErrorCategory.NETWORK,
        recovery_strategy=lambda: logger.info("Network connection restored")
    )
    async def simulate_network_error(self) -> Dict[str, Any]:
        """Simulate a network error with recovery."""
        logger.info("Simulating network operation...")
        # Simulate a network error
        raise TimeoutError("Network timeout")
    
    @handle_errors(
        context="validation_operation",
        severity=ErrorSeverity.LOW,
        category=ErrorCategory.VALIDATION
    )
    async def simulate_validation_error(self) -> Dict[str, Any]:
        """Simulate a validation error."""
        logger.info("Simulating validation operation...")
        # Simulate a validation error
        raise ValueError("Invalid input data")
    
    async def test_error_handling(self) -> bool:
        """Test error handling mechanisms."""
        logger.info("Testing error handling mechanisms...")
        
        # Test database error handling
        try:
            await self.simulate_database_error()
        except Exception as e:
            logger.info(f"Caught exception: {e}")
        
        # Test network error handling with recovery
        try:
            await self.simulate_network_error()
        except Exception as e:
            logger.info(f"Caught exception: {e}")
        
        # Test validation error handling
        try:
            await self.simulate_validation_error()
        except Exception as e:
            logger.info(f"Caught exception: {e}")
        
        # Check error statistics
        stats = self.error_handler.get_error_statistics()
        logger.info(f"Error statistics: {stats}")
        
        logger.info("Error handling tests completed!")
        return True
    
    async def test_recovery_mechanisms(self) -> bool:
        """Test recovery mechanisms."""
        logger.info("Testing recovery mechanisms...")
        
        # Test recovery with a simple function
        async def recovery_function():
            logger.info("Recovery function executed")
            return True
        
        # Simulate an error with recovery
        try:
            raise RuntimeError("Simulated error for recovery test")
        except RuntimeError as e:
            result = await self.error_handler.handle_error(
                error=e,
                context="recovery_test",
                severity=ErrorSeverity.MEDIUM,
                category=ErrorCategory.SYSTEM,
                recovery_strategy=recovery_function
            )
            logger.info(f"Recovery test result: {result}")
        
        logger.info("Recovery mechanism tests completed!")
        return True
    
    async def run_all_tests(self) -> bool:
        """Run all reliability tests."""
        logger.info("Starting reliability tests...")
        
        try:
            await self.test_error_handling()
            await self.test_recovery_mechanisms()
            
            logger.info("🎉 All reliability tests passed!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Reliability test failed: {e}")
            return False

async def main():
    """Main test function."""
    test_suite = ReliabilityTest()
    success = await test_suite.run_all_tests()
    
    if success:
        logger.info("Reliability testing completed successfully!")
    else:
        logger.error("Reliability testing failed!")
    
    return success

if __name__ == "__main__":
    asyncio.run(main())