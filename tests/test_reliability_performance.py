"""
Performance tests for reliability enhancements
"""
import pytest
import asyncio
import time
from unittest.mock import Mock, patch, AsyncMock

# Import the modules we want to test
from src.lib.error_handler import ErrorHandler

@pytest.fixture
def error_handler():
    """Create a test instance of ErrorHandler"""
    with patch('src.lib.error_handler.event_bus'):
        handler = ErrorHandler()
        return handler

@pytest.mark.asyncio
async def test_error_handler_performance(error_handler):
    """Test error handler performance"""
    start_time = time.time()
    
    # Generate multiple errors
    for i in range(1000):
        try:
            raise ValueError(f"Test error {i}")
        except ValueError as e:
            await error_handler.handle_error(
                error=e,
                context=f"test_context_{i}",
                severity=error_handler.ErrorSeverity.MEDIUM,
                category=error_handler.ErrorCategory.VALIDATION
            )
    
    end_time = time.time()
    handling_time = end_time - start_time
    
    # Error handling should be efficient
    assert handling_time < 3.0  # Should complete within 3 seconds
    assert len(error_handler.error_history) == 1000
    assert error_handler.error_counts["validation_medium"] == 1000

@pytest.mark.asyncio
async def test_error_handler_recovery_performance(error_handler):
    """Test error handler recovery performance"""
    async def successful_recovery_strategy():
        return True
    
    async def failing_recovery_strategy():
        raise Exception("Recovery failed")
    
    start_time = time.time()
    
    # Test successful recoveries
    for i in range(100):
        try:
            raise RuntimeError(f"Test error {i}")
        except RuntimeError as e:
            await error_handler.handle_error(
                error=e,
                context=f"test_context_{i}",
                severity=error_handler.ErrorSeverity.HIGH,
                category=error_handler.ErrorCategory.SYSTEM,
                recovery_strategy=successful_recovery_strategy
            )
    
    end_time = time.time()
    successful_recovery_time = end_time - start_time
    
    # Test failing recoveries
    start_time = time.time()
    
    for i in range(100):
        try:
            raise RuntimeError(f"Test error {i}")
        except RuntimeError as e:
            await error_handler.handle_error(
                error=e,
                context=f"test_context_{i}",
                severity=error_handler.ErrorSeverity.HIGH,
                category=error_handler.ErrorCategory.SYSTEM,
                recovery_strategy=failing_recovery_strategy
            )
    
    end_time = time.time()
    failing_recovery_time = end_time - start_time
    
    # Recovery operations should be efficient
    assert successful_recovery_time < 2.0  # Should complete within 2 seconds
    assert failing_recovery_time < 2.0  # Should complete within 2 seconds

@pytest.mark.asyncio
async def test_error_handler_statistics_performance(error_handler):
    """Test error handler statistics performance"""
    # Generate some errors first
    for i in range(1000):
        try:
            raise ValueError(f"Test error {i}")
        except ValueError as e:
            await error_handler.handle_error(
                error=e,
                context=f"test_context_{i}",
                severity=error_handler.ErrorSeverity.LOW,
                category=error_handler.ErrorCategory.VALIDATION
            )
    
    start_time = time.time()
    
    # Get statistics multiple times
    for i in range(100):
        stats = error_handler.get_error_statistics()
        assert "total_errors" in stats
        assert "error_counts_by_type" in stats
        assert "recent_errors" in stats
    
    end_time = time.time()
    statistics_time = end_time - start_time
    
    # Statistics retrieval should be efficient
    assert statistics_time < 1.0  # Should complete within 1 second

@pytest.mark.asyncio
async def test_error_handler_concurrent_performance(error_handler):
    """Test error handler concurrent performance"""
    async def handle_error_task(task_id):
        try:
            raise ValueError(f"Concurrent test error {task_id}")
        except ValueError as e:
            return await error_handler.handle_error(
                error=e,
                context=f"concurrent_test_{task_id}",
                severity=error_handler.ErrorSeverity.MEDIUM,
                category=error_handler.ErrorCategory.VALIDATION
            )
    
    start_time = time.time()
    
    # Run multiple concurrent error handling tasks
    tasks = [handle_error_task(i) for i in range(100)]
    results = await asyncio.gather(*tasks)
    
    end_time = time.time()
    concurrent_time = end_time - start_time
    
    # All error handling tasks should complete successfully
    assert len(results) == 100
    assert all(isinstance(result, dict) for result in results)
    assert all(result["handled"] is True for result in results)
    
    # Concurrent operations should be efficient
    assert concurrent_time < 2.0  # Should complete within 2 seconds

@pytest.mark.asyncio
async def test_error_handler_history_management_performance(error_handler):
    """Test error handler history management performance"""
    # Generate many errors to test history management
    for i in range(5000):
        try:
            raise ValueError(f"History test error {i}")
        except ValueError as e:
            await error_handler.handle_error(
                error=e,
                context=f"history_test_{i}",
                severity=error_handler.ErrorSeverity.LOW,
                category=error_handler.ErrorCategory.VALIDATION
            )
    
    # Test history clearing performance
    start_time = time.time()
    
    await error_handler.clear_error_history()
    
    end_time = time.time()
    clear_time = end_time - start_time
    
    # History clearing should be efficient
    assert clear_time < 1.0  # Should complete within 1 second
    assert len(error_handler.error_history) == 0
    assert len(error_handler.error_counts) == 0

@pytest.mark.asyncio
async def test_error_handler_recovery_attempts_tracking_performance(error_handler):
    """Test error handler recovery attempts tracking performance"""
    async def recovery_strategy():
        return False  # Always fail to test recovery attempts tracking
    
    start_time = time.time()
    
    # Test multiple recovery attempts for the same error
    try:
        raise RuntimeError("Recovery attempts test error")
    except RuntimeError as e:
        for i in range(error_handler.max_recovery_attempts + 5):
            await error_handler.handle_error(
                error=e,
                context="recovery_attempts_test",
                severity=error_handler.ErrorSeverity.HIGH,
                category=error_handler.ErrorCategory.SYSTEM,
                recovery_strategy=recovery_strategy
            )
    
    end_time = time.time()
    recovery_tracking_time = end_time - start_time
    
    # Recovery attempts tracking should be efficient
    assert recovery_tracking_time < 1.0  # Should complete within 1 second

@pytest.mark.asyncio
async def test_error_handler_decorator_performance(error_handler):
    """Test error handler decorator performance"""
    with patch('src.lib.error_handler.error_handler', error_handler):
        from src.lib.error_handler import handle_errors
        
        @handle_errors(
            context="decorator_performance_test",
            severity=error_handler.ErrorSeverity.MEDIUM,
            category=error_handler.ErrorCategory.VALIDATION
        )
        async def function_that_raises():
            raise ValueError("Test error from decorator")
        
        @handle_errors(
            context="decorator_performance_test",
            severity=error_handler.ErrorSeverity.MEDIUM,
            category=error_handler.ErrorCategory.VALIDATION
        )
        async def function_that_works():
            return "success"
        
        start_time = time.time()
        
        # Test decorated functions that raise errors
        error_results = []
        for i in range(100):
            result = await function_that_raises()
            error_results.append(result)
        
        # Test decorated functions that work normally
        success_results = []
        for i in range(100):
            result = await function_that_works()
            success_results.append(result)
        
        end_time = time.time()
        decorator_time = end_time - start_time
        
        # All decorated functions should complete successfully
        assert len(error_results) == 100
        assert all(isinstance(result, dict) for result in error_results)
        assert len(success_results) == 100
        assert all(result == "success" for result in success_results)
        
        # Decorator operations should be efficient
        assert decorator_time < 3.0  # Should complete within 3 seconds

if __name__ == "__main__":
    pytest.main([__file__])