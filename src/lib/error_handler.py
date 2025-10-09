"""
Enhanced Error Handler for GlobalScope MultiFrame 11.0
This module provides comprehensive error handling and recovery mechanisms.
"""

import asyncio
import logging
import traceback
from typing import Any, Callable, Optional, Dict
from datetime import datetime
from enum import Enum

from src.lib.utils import get_logger
from src.lib.event_bus import event_bus

logger = get_logger("ErrorHandler")

class ErrorSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ErrorCategory(Enum):
    NETWORK = "network"
    DATABASE = "database"
    SECURITY = "security"
    VALIDATION = "validation"
    SYSTEM = "system"
    UNKNOWN = "unknown"

class ErrorHandler:
    """Enhanced error handler with recovery mechanisms."""
    
    def __init__(self):
        self.error_counts: Dict[str, int] = {}
        self.recovery_attempts: Dict[str, int] = {}
        self.max_recovery_attempts = 3
        self.error_history: list = []
        
        # Subscribe to error events
        event_bus.subscribe("system_error", self._handle_system_error)
        
        logger.info("ErrorHandler initialized")
    
    async def handle_error(
        self, 
        error: Exception, 
        context: str, 
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        category: ErrorCategory = ErrorCategory.UNKNOWN,
        recovery_strategy: Optional[Callable] = None,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Handle an error with comprehensive logging and optional recovery.
        
        Args:
            error: The exception that occurred
            context: Description of where the error occurred
            severity: Severity level of the error
            category: Category of the error
            recovery_strategy: Optional function to attempt recovery
            user_id: Optional user ID associated with the error
            
        Returns:
            Dictionary with error handling result
        """
        error_id = f"error_{datetime.utcnow().timestamp()}"
        
        # Log the error
        error_info = {
            "error_id": error_id,
            "context": context,
            "severity": severity.value,
            "category": category.value,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "traceback": traceback.format_exc(),
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id
        }
        
        self.error_history.append(error_info)
        
        # Update error counts
        error_key = f"{category.value}_{severity.value}"
        self.error_counts[error_key] = self.error_counts.get(error_key, 0) + 1
        
        # Log to system logger
        logger.error(f"Error in {context}: {error}")
        
        # Publish error event
        await event_bus.publish("system_error", error_info)
        
        # Attempt recovery if strategy provided
        recovery_result = None
        if recovery_strategy:
            recovery_result = await self._attempt_recovery(
                error_id, error, context, recovery_strategy
            )
        
        return {
            "error_id": error_id,
            "handled": True,
            "severity": severity.value,
            "category": category.value,
            "recovery_attempted": recovery_strategy is not None,
            "recovery_successful": recovery_result is True,
            "error_info": error_info
        }
    
    async def _attempt_recovery(
        self, 
        error_id: str, 
        error: Exception, 
        context: str, 
        recovery_strategy: Callable
    ) -> bool:
        """
        Attempt to recover from an error.
        
        Args:
            error_id: Unique identifier for the error
            error: The exception that occurred
            context: Description of where the error occurred
            recovery_strategy: Function to attempt recovery
            
        Returns:
            True if recovery successful, False otherwise
        """
        # Check if we've exceeded max recovery attempts
        attempts = self.recovery_attempts.get(error_id, 0)
        if attempts >= self.max_recovery_attempts:
            logger.warning(f"Max recovery attempts exceeded for error {error_id}")
            return False
        
        # Increment attempt count
        self.recovery_attempts[error_id] = attempts + 1
        
        try:
            # Attempt recovery
            if asyncio.iscoroutinefunction(recovery_strategy):
                result = await recovery_strategy()
            else:
                result = recovery_strategy()
            
            if result:
                logger.info(f"Recovery successful for error {error_id} in {context}")
                return True
            else:
                logger.warning(f"Recovery failed for error {error_id} in {context}")
                return False
                
        except Exception as recovery_error:
            logger.error(f"Recovery attempt failed for error {error_id}: {recovery_error}")
            return False
    
    async def _handle_system_error(self, event: Dict[str, Any]):
        """Handle system error events."""
        error_info = event["data"]
        logger.info(f"Processing system error event: {error_info['error_id']}")
        
        # In a real implementation, this could trigger alerts, notifications, etc.
        # For now, we just log it
        pass
    
    def get_error_statistics(self) -> Dict[str, Any]:
        """Get error statistics."""
        return {
            "total_errors": len(self.error_history),
            "error_counts_by_type": self.error_counts,
            "recovery_attempts": self.recovery_attempts,
            "recent_errors": self.error_history[-10:] if self.error_history else []
        }
    
    async def clear_error_history(self):
        """Clear error history."""
        self.error_history.clear()
        self.error_counts.clear()
        self.recovery_attempts.clear()
        logger.info("Error history cleared")

# Global error handler instance
error_handler = ErrorHandler()

# Decorator for automatic error handling
def handle_errors(
    context: str,
    severity: ErrorSeverity = ErrorSeverity.MEDIUM,
    category: ErrorCategory = ErrorCategory.UNKNOWN,
    recovery_strategy: Optional[Callable] = None
):
    """
    Decorator for automatic error handling.
    
    Args:
        context: Description of where the error occurred
        severity: Severity level of the error
        category: Category of the error
        recovery_strategy: Optional function to attempt recovery
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            try:
                if asyncio.iscoroutinefunction(func):
                    return await func(*args, **kwargs)
                else:
                    return func(*args, **kwargs)
            except Exception as e:
                result = await error_handler.handle_error(
                    error=e,
                    context=context,
                    severity=severity,
                    category=category,
                    recovery_strategy=recovery_strategy
                )
                # Re-raise critical errors
                if severity == ErrorSeverity.CRITICAL:
                    raise e
                return result
        return wrapper
    return decorator