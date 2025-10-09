import asyncio
import logging
from typing import Dict, List, Callable, Any
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("EventBus")

class EventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
        self._event_queue = asyncio.Queue()
        self._processing_task = None
    
    def subscribe(self, event_type: str, callback: Callable):
        """Subscribe to an event type"""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)
        logger.info(f"Subscribed to event type: {event_type}")
    
    async def publish(self, event_type: str, data: Dict[str, Any]):
        """Publish an event to all subscribers"""
        event = {
            "type": event_type,
            "data": data,
            "timestamp": datetime.utcnow().isoformat()
        }
        await self._event_queue.put(event)
        logger.info(f"Published event: {event_type}")
    
    async def start_processing(self):
        """Start processing events from the queue"""
        self._processing_task = asyncio.create_task(self._process_events())
        logger.info("Event bus processing started")
    
    async def stop_processing(self):
        """Stop processing events"""
        if self._processing_task:
            self._processing_task.cancel()
            try:
                await self._processing_task
            except asyncio.CancelledError:
                pass
            logger.info("Event bus processing stopped")
    
    async def _process_events(self):
        """Process events from the queue"""
        while True:
            try:
                event = await self._event_queue.get()
                await self._handle_event(event)
                self._event_queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error processing event: {e}")
    
    async def _handle_event(self, event: Dict[str, Any]):
        """Handle a single event by notifying all subscribers"""
        event_type = event["type"]
        if event_type in self._subscribers:
            for callback in self._subscribers[event_type]:
                try:
                    if asyncio.iscoroutinefunction(callback):
                        await callback(event)
                    else:
                        callback(event)
                except Exception as e:
                    logger.error(f"Error in event callback for {event_type}: {e}")

# Global event bus instance
event_bus = EventBus()