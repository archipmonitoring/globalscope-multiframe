#!/usr/bin/env python3
"""
Test script for the enhanced error handling system
"""
import sys
import os
import asyncio

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.lib.error_handler import ErrorHandler, ErrorSeverity, ErrorCategory, handle_errors

async def test_error_handler():
    """Test the error handler functionality"""
    print("Testing Error Handler...")
    
    # Create an error handler instance
    error_handler = ErrorHandler()
    
    # Test basic error handling
    try:
        raise ValueError("Test error")
    except ValueError as e:
        result = await error_handler.handle_error(
            error=e,
            context="test_context",
            severity=ErrorSeverity.MEDIUM,
            category=ErrorCategory.VALIDATION
        )
        print(f"Error handling result: {result}")
    
    # Test error statistics
    stats = error_handler.get_error_statistics()
    print(f"Error statistics: {stats}")
    
    print("Error Handler test completed!")

@handle_errors(
    context="decorator_test",
    severity=ErrorSeverity.HIGH,
    category=ErrorCategory.SYSTEM
)
async def test_decorated_function():
    """Test function with error handling decorator"""
    print("Testing decorated function...")
    raise RuntimeError("Test error from decorated function")

async def main():
    """Main test function"""
    print("Starting error handling tests...")
    
    # Test error handler
    await test_error_handler()
    
    # Test decorated function
    try:
        await test_decorated_function()
    except Exception as e:
        print(f"Caught exception from decorated function: {e}")
    
    print("All tests completed!")

if __name__ == "__main__":
    asyncio.run(main())