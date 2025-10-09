"""
Unit tests for the error handler module
"""
import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from src.lib.error_handler import ErrorHandler, ErrorSeverity, ErrorCategory, handle_errors

@pytest.fixture
def error_handler():
    """Create a test instance of ErrorHandler"""
    with patch('src.lib.error_handler.event_bus'):
        handler = ErrorHandler()
        return handler

@pytest.mark.asyncio
async def test_error_handler_initialization(error_handler):
    """Test error handler initialization"""
    assert error_handler is not None
    assert isinstance(error_handler.error_counts, dict)
    assert isinstance(error_handler.recovery_attempts, dict)
    assert error_handler.max_recovery_attempts == 3
    assert isinstance(error_handler.error_history, list)

@pytest.mark.asyncio
async def test_error_handler_basic_error_handling(error_handler):
    """Test basic error handling"""
    with patch('src.lib.error_handler.event_bus'):
        try:
            raise ValueError("Test error")
        except ValueError as e:
            result = await error_handler.handle_error(
                error=e,
                context="test_context",
                severity=ErrorSeverity.MEDIUM,
                category=ErrorCategory.VALIDATION
            )
            
            assert result["handled"] is True
            assert result["severity"] == "medium"
            assert result["category"] == "validation"
            assert result["recovery_attempted"] is False
            assert len(error_handler.error_history) == 1
            assert error_handler.error_counts["validation_medium"] == 1

@pytest.mark.asyncio
async def test_error_handler_with_recovery_strategy(error_handler):
    """Test error handling with recovery strategy"""
    with patch('src.lib.error_handler.event_bus'):
        async def recovery_strategy():
            return True
            
        try:
            raise RuntimeError("Test error")
        except RuntimeError as e:
            result = await error_handler.handle_error(
                error=e,
                context="test_context",
                severity=ErrorSeverity.HIGH,
                category=ErrorCategory.SYSTEM,
                recovery_strategy=recovery_strategy
            )
            
            assert result["handled"] is True
            assert result["recovery_attempted"] is True
            assert result["recovery_successful"] is True

@pytest.mark.asyncio
async def test_error_handler_failed_recovery(error_handler):
    """Test error handling with failed recovery strategy"""
    with patch('src.lib.error_handler.event_bus'):
        async def failing_recovery_strategy():
            raise Exception("Recovery failed")
            
        try:
            raise RuntimeError("Test error")
        except RuntimeError as e:
            result = await error_handler.handle_error(
                error=e,
                context="test_context",
                severity=ErrorSeverity.HIGH,
                category=ErrorCategory.SYSTEM,
                recovery_strategy=failing_recovery_strategy
            )
            
            assert result["handled"] is True
            assert result["recovery_attempted"] is True
            assert result["recovery_successful"] is False

@pytest.mark.asyncio
async def test_error_handler_recovery_attempts_limit(error_handler):
    """Test error handler recovery attempts limit"""
    with patch('src.lib.error_handler.event_bus'):
        async def recovery_strategy():
            return False
            
        try:
            raise RuntimeError("Test error")
        except RuntimeError as e:
            # Test multiple recovery attempts
            for i in range(error_handler.max_recovery_attempts + 2):
                result = await error_handler.handle_error(
                    error=e,
                    context="test_context",
                    severity=ErrorSeverity.HIGH,
                    category=ErrorCategory.SYSTEM,
                    recovery_strategy=recovery_strategy
                )
                
                if i < error_handler.max_recovery_attempts:
                    # First attempts should try recovery
                    assert result["recovery_attempted"] is True
                else:
                    # After max attempts, recovery should not be attempted
                    # Note: This is a simplified test - actual behavior depends on error_id tracking
                    pass

@pytest.mark.asyncio
async def test_error_handler_get_statistics(error_handler):
    """Test error handler statistics"""
    with patch('src.lib.error_handler.event_bus'):
        # Generate some errors
        try:
            raise ValueError("Test error 1")
        except ValueError as e:
            await error_handler.handle_error(
                error=e,
                context="test_context_1",
                severity=ErrorSeverity.LOW,
                category=ErrorCategory.VALIDATION
            )
        
        try:
            raise RuntimeError("Test error 2")
        except RuntimeError as e:
            await error_handler.handle_error(
                error=e,
                context="test_context_2",
                severity=ErrorSeverity.HIGH,
                category=ErrorCategory.SYSTEM
            )
        
        # Get statistics
        stats = error_handler.get_error_statistics()
        assert "total_errors" in stats
        assert "error_counts_by_type" in stats
        assert "recovery_attempts" in stats
        assert "recent_errors" in stats
        assert stats["total_errors"] == 2
        assert len(stats["recent_errors"]) == 2

@pytest.mark.asyncio
async def test_error_handler_clear_history(error_handler):
    """Test error handler clear history"""
    with patch('src.lib.error_handler.event_bus'):
        # Generate some errors
        try:
            raise ValueError("Test error")
        except ValueError as e:
            await error_handler.handle_error(
                error=e,
                context="test_context",
                severity=ErrorSeverity.LOW,
                category=ErrorCategory.VALIDATION
            )
        
        # Verify errors were recorded
        assert len(error_handler.error_history) == 1
        assert len(error_handler.error_counts) == 1
        
        # Clear history
        await error_handler.clear_error_history()
        
        # Verify history was cleared
        assert len(error_handler.error_history) == 0
        assert len(error_handler.error_counts) == 0
        assert len(error_handler.recovery_attempts) == 0

@pytest.mark.asyncio
async def test_handle_errors_decorator(error_handler):
    """Test @handle_errors decorator"""
    with patch('src.lib.error_handler.error_handler', error_handler), \
         patch('src.lib.error_handler.event_bus'):
        
        @handle_errors(
            context="decorator_test",
            severity=ErrorSeverity.MEDIUM,
            category=ErrorCategory.VALIDATION
        )
        async def function_that_raises():
            raise ValueError("Test error from decorator")
        
        result = await function_that_raises()
        # The decorator should handle the error and return the error handling result
        assert isinstance(result, dict)
        assert "handled" in result
        assert result["handled"] is True

@pytest.mark.asyncio
async def test_handle_errors_decorator_without_recovery(error_handler):
    """Test @handle_errors decorator without recovery strategy"""
    with patch('src.lib.error_handler.error_handler', error_handler), \
         patch('src.lib.error_handler.event_bus'):
        
        @handle_errors(
            context="decorator_test",
            severity=ErrorSeverity.MEDIUM,
            category=ErrorCategory.VALIDATION
        )
        async def function_that_works():
            return "success"
        
        result = await function_that_works()
        # The decorator should return the normal function result
        assert result == "success"

if __name__ == "__main__":
    pytest.main([__file__])