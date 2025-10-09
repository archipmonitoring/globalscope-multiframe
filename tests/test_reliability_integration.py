"""
Integration tests for reliability enhancements
"""
import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock

# Import the modules we want to test integration between
from src.lib.error_handler import ErrorHandler
from src.chip_design.chip_driver_generator import ChipDriverGenerator
from src.chip_design.zero_defect_engine import ZeroDefectEngine

@pytest.fixture
def error_handler():
    """Create a test instance of ErrorHandler"""
    with patch('src.lib.error_handler.event_bus'):
        handler = ErrorHandler()
        return handler

@pytest.fixture
def chip_driver_generator_with_error_handling(error_handler):
    """Create a test instance of ChipDriverGenerator with error handling"""
    with patch('src.chip_design.chip_driver_generator.holo_misha_instance'), \
         patch('src.chip_design.chip_driver_generator.security_logger'), \
         patch('src.chip_design.chip_driver_generator.ai_design'), \
         patch('src.chip_design.chip_driver_generator.redis_client'), \
         patch('src.chip_design.chip_driver_generator.firewall'):
        generator = ChipDriverGenerator()
        return generator

@pytest.fixture
def zero_defect_engine_with_error_handling(error_handler):
    """Create a test instance of ZeroDefectEngine with error handling"""
    with patch('src.chip_design.zero_defect_engine.holo_misha_instance'), \
         patch('src.chip_design.zero_defect_engine.ai_design'), \
         patch('src.chip_design.zero_defect_engine.pipeline_guard'), \
         patch('src.chip_design.zero_defect_engine.redis_client'), \
         patch('src.chip_design.zero_defect_engine.config_manager'), \
         patch('src.chip_design.zero_defect_engine.firewall'):
        engine = ZeroDefectEngine()
        return engine

@pytest.mark.asyncio
async def test_chip_driver_generator_error_handling_integration(chip_driver_generator_with_error_handling, error_handler):
    """Test ChipDriverGenerator integration with error handling"""
    with patch('src.chip_design.chip_driver_generator.error_handler', error_handler), \
         patch.object(chip_driver_generator_with_error_handling, 'ai_design') as mock_ai_design:
        
        # Test normal operation
        mock_ai_design.optimize_design = AsyncMock(return_value={"status": "success", "optimized_data": {}})
        
        result = await chip_driver_generator_with_error_handling.generate_driver(
            "test_user",
            "test_chip",
            {"design_data": "test"}
        )
        
        assert result["status"] == "success"
        assert len(error_handler.error_history) == 0  # No errors should occur

@pytest.mark.asyncio
async def test_chip_driver_generator_error_recovery(chip_driver_generator_with_error_handling, error_handler):
    """Test ChipDriverGenerator error recovery"""
    with patch('src.chip_design.chip_driver_generator.error_handler', error_handler), \
         patch.object(chip_driver_generator_with_error_handling, 'ai_design') as mock_ai_design:
        
        # Test error handling when AI design fails
        mock_ai_design.optimize_design = AsyncMock(return_value={"status": "error", "message": "AI failed"})
        
        result = await chip_driver_generator_with_error_handling.generate_driver(
            "test_user",
            "test_chip",
            {"design_data": "test"}
        )
        
        assert result["status"] == "error"
        assert "Optimization failed" in result["message"]
        # Error should be handled gracefully
        assert isinstance(result, dict)  # Should return error result, not raise exception

@pytest.mark.asyncio
async def test_chip_driver_generator_exception_handling(chip_driver_generator_with_error_handling, error_handler):
    """Test ChipDriverGenerator exception handling"""
    with patch('src.chip_design.chip_driver_generator.error_handler', error_handler), \
         patch.object(chip_driver_generator_with_error_handling, 'ai_design') as mock_ai_design:
        
        # Test exception handling when AI design raises an exception
        mock_ai_design.optimize_design = AsyncMock(side_effect=Exception("AI service unavailable"))
        
        result = await chip_driver_generator_with_error_handling.generate_driver(
            "test_user",
            "test_chip",
            {"design_data": "test"}
        )
        
        assert result["status"] == "error"
        assert "Driver generation failed" in result["message"]
        # Exception should be caught and handled
        assert isinstance(result, dict)  # Should return error result, not raise exception

@pytest.mark.asyncio
async def test_zero_defect_engine_error_handling_integration(zero_defect_engine_with_error_handling, error_handler):
    """Test ZeroDefectEngine integration with error handling"""
    with patch('src.chip_design.zero_defect_engine.error_handler', error_handler), \
         patch.object(zero_defect_engine_with_error_handling, 'ai_design') as mock_ai_design, \
         patch.object(zero_defect_engine_with_error_handling, 'pipeline_guard') as mock_pipeline_guard:
        
        # Test normal operation
        mock_ai_design.optimize_design = AsyncMock(return_value={"status": "success", "optimized_data": {}})
        mock_pipeline_guard.validate_process = AsyncMock(return_value={"status": "success"})
        
        result = await zero_defect_engine_with_error_handling.ensure_zero_defect(
            "test_user",
            "test_chip",
            {"design_data": "test"}
        )
        
        assert result["status"] == "success"
        assert len(error_handler.error_history) == 0  # No errors should occur

@pytest.mark.asyncio
async def test_zero_defect_engine_pipeline_error_handling(zero_defect_engine_with_error_handling, error_handler):
    """Test ZeroDefectEngine pipeline error handling"""
    with patch('src.chip_design.zero_defect_engine.error_handler', error_handler), \
         patch.object(zero_defect_engine_with_error_handling, 'pipeline_guard') as mock_pipeline_guard:
        
        # Test error handling when pipeline validation fails
        mock_pipeline_guard.validate_process = AsyncMock(return_value={"status": "error", "message": "Pipeline validation failed"})
        
        result = await zero_defect_engine_with_error_handling.ensure_zero_defect(
            "test_user",
            "test_chip",
            {"design_data": "test"}
        )
        
        assert result["status"] == "error"
        assert "Pipeline validation failed" in result["message"]
        # Error should be handled gracefully

@pytest.mark.asyncio
async def test_zero_defect_engine_ai_error_handling(zero_defect_engine_with_error_handling, error_handler):
    """Test ZeroDefectEngine AI error handling"""
    with patch('src.chip_design.zero_defect_engine.error_handler', error_handler), \
         patch.object(zero_defect_engine_with_error_handling, 'ai_design') as mock_ai_design, \
         patch.object(zero_defect_engine_with_error_handling, 'pipeline_guard') as mock_pipeline_guard:
        
        # Test error handling when AI optimization fails
        mock_pipeline_guard.validate_process = AsyncMock(return_value={"status": "success"})
        mock_ai_design.optimize_design = AsyncMock(return_value={"status": "error", "message": "AI optimization failed"})
        
        result = await zero_defect_engine_with_error_handling.ensure_zero_defect(
            "test_user",
            "test_chip",
            {"design_data": "test"}
        )
        
        assert result["status"] == "error"
        assert "AI optimization failed" in result["message"]
        # Error should be handled gracefully

@pytest.mark.asyncio
async def test_error_handler_statistics_integration(error_handler):
    """Test error handler statistics integration"""
    with patch('src.lib.error_handler.event_bus'):
        # Generate some errors
        try:
            raise ValueError("Test error 1")
        except ValueError as e:
            await error_handler.handle_error(
                error=e,
                context="test_context_1",
                severity=error_handler.ErrorSeverity.LOW,
                category=error_handler.ErrorCategory.VALIDATION
            )
        
        try:
            raise RuntimeError("Test error 2")
        except RuntimeError as e:
            await error_handler.handle_error(
                error=e,
                context="test_context_2",
                severity=error_handler.ErrorSeverity.HIGH,
                category=error_handler.ErrorCategory.SYSTEM
            )
        
        # Get statistics
        stats = error_handler.get_error_statistics()
        assert stats["total_errors"] == 2
        assert "validation_low" in stats["error_counts_by_type"]
        assert "system_high" in stats["error_counts_by_type"]

@pytest.mark.asyncio
async def test_error_handler_event_bus_integration(error_handler):
    """Test error handler event bus integration"""
    with patch('src.lib.error_handler.event_bus') as mock_event_bus:
        mock_event_bus.publish = AsyncMock()
        
        try:
            raise ValueError("Test error")
        except ValueError as e:
            await error_handler.handle_error(
                error=e,
                context="test_context",
                severity=error_handler.ErrorSeverity.MEDIUM,
                category=error_handler.ErrorCategory.VALIDATION
            )
        
        # Verify event was published
        mock_event_bus.publish.assert_called_once()
        call_args = mock_event_bus.publish.call_args
        assert call_args[0][0] == "system_error"  # Event type
        assert "data" in call_args[0][1]  # Event data

if __name__ == "__main__":
    pytest.main([__file__])