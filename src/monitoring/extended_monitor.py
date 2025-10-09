"""
Extended Monitoring Module for GlobalScope MultiFrame 11.0
This module provides expanded monitoring capabilities for additional system components.
"""

import asyncio
import logging
import psutil
import time
from typing import Dict, Any, List, Optional
from datetime import datetime
from collections import defaultdict, deque

from src.lib.utils import get_logger
from src.lib.redis_client import redis_client
from src.security.quantum_singularity_firewall import QuantumSingularityFirewall
from src.ai.agent_guard import AgentGuard

logger = get_logger("ExtendedMonitor")

class SystemMetrics:
    """System-level metrics monitoring"""
    
    def __init__(self):
        self.cpu_usage_history = deque(maxlen=100)
        self.memory_usage_history = deque(maxlen=100)
        self.disk_usage_history = deque(maxlen=100)
        self.network_io_history = deque(maxlen=100)
        
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get system resource metrics"""
        try:
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            self.cpu_usage_history.append(cpu_percent)
            
            # Memory metrics
            memory = psutil.virtual_memory()
            self.memory_usage_history.append(memory.percent)
            
            # Disk metrics
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            self.disk_usage_history.append(disk_percent)
            
            # Network I/O metrics
            net_io = psutil.net_io_counters()
            self.network_io_history.append({
                'bytes_sent': net_io.bytes_sent,
                'bytes_recv': net_io.bytes_recv,
                'packets_sent': net_io.packets_sent,
                'packets_recv': net_io.packets_recv
            })
            
            return {
                'cpu': {
                    'percent': cpu_percent,
                    'avg_last_10': sum(list(self.cpu_usage_history)[-10:]) / min(len(self.cpu_usage_history), 10),
                    'max_last_100': max(self.cpu_usage_history) if self.cpu_usage_history else 0
                },
                'memory': {
                    'percent': memory.percent,
                    'total_gb': round(memory.total / (1024**3), 2),
                    'available_gb': round(memory.available / (1024**3), 2),
                    'used_gb': round(memory.used / (1024**3), 2)
                },
                'disk': {
                    'percent': disk_percent,
                    'total_gb': round(disk.total / (1024**3), 2),
                    'used_gb': round(disk.used / (1024**3), 2),
                    'free_gb': round(disk.free / (1024**3), 2)
                },
                'network': {
                    'bytes_sent': net_io.bytes_sent,
                    'bytes_recv': net_io.bytes_recv,
                    'packets_sent': net_io.packets_sent,
                    'packets_recv': net_io.packets_recv
                }
            }
        except Exception as e:
            logger.error(f"Error getting system metrics: {e}")
            return {'error': str(e)}

class RedisMetrics:
    """Redis client metrics monitoring"""
    
    def __init__(self):
        self.redis_client = redis_client
        self.cache_hit_count = 0
        self.cache_miss_count = 0
        self.redis_error_count = 0
        self.operation_latency_history = deque(maxlen=1000)
    
    async def get_redis_metrics(self) -> Dict[str, Any]:
        """Get Redis client metrics"""
        try:
            # Test Redis connectivity
            start_time = time.time()
            ping_result = await self.redis_client.ping()
            latency = time.time() - start_time
            
            # Get cache statistics
            cache_stats = {
                'cache_size': len(self.redis_client.cache),
                'cache_max_size': self.redis_client.max_cache_size,
                'cache_hit_rate': self.cache_hit_count / (self.cache_hit_count + self.cache_miss_count) if (self.cache_hit_count + self.cache_miss_count) > 0 else 0,
                'cache_hits': self.cache_hit_count,
                'cache_misses': self.cache_miss_count
            }
            
            # Get Redis info (if available)
            redis_info = {}
            try:
                # This would require additional Redis commands
                # For now, we'll provide basic connectivity info
                pass
            except Exception:
                pass
            
            return {
                'connected': ping_result,
                'latency_ms': round(latency * 1000, 2),
                'cache_stats': cache_stats,
                'errors': self.redis_error_count,
                'avg_operation_latency_ms': sum(self.operation_latency_history) / len(self.operation_latency_history) if self.operation_latency_history else 0
            }
        except Exception as e:
            self.redis_error_count += 1
            logger.error(f"Error getting Redis metrics: {e}")
            return {'error': str(e), 'errors': self.redis_error_count}

class SecurityMetrics:
    """Security metrics monitoring"""
    
    def __init__(self):
        self.firewall = QuantumSingularityFirewall()
        self.threat_history = deque(maxlen=100)
    
    async def get_security_metrics(self) -> Dict[str, Any]:
        """Get security-related metrics"""
        try:
            # Get firewall metrics using getattr to avoid linter issues
            threats_blocked = getattr(self.firewall, 'threats_blocked', 0)
            firewall_active = getattr(self.firewall, 'is_active', True)
            
            # Get threat history if available
            threat_history = []
            if hasattr(self.firewall, 'threat_history'):
                threat_history = getattr(self.firewall, 'threat_history', [])[-10:]  # Last 10 threats
            
            return {
                'firewall': {
                    'active': firewall_active,
                    'threats_blocked': threats_blocked
                },
                'recent_threats': threat_history,
                'security_status': 'active' if firewall_active else 'inactive'
            }
        except Exception as e:
            logger.error(f"Error getting security metrics: {e}")
            return {'error': str(e)}

class AIMetrics:
    """AI agent metrics monitoring"""
    
    def __init__(self):
        self.agent_guard = AgentGuard()
        self.agent_states_history = deque(maxlen=100)
    
    async def get_ai_metrics(self) -> Dict[str, Any]:
        """Get AI agent metrics"""
        try:
            # Get agent states if available
            agent_states = {}
            if hasattr(self.agent_guard, 'agent_states'):
                agent_states = getattr(self.agent_guard, 'agent_states', {})
            
            # Count agents by state
            state_counts = defaultdict(int)
            for state in agent_states.values():
                state_counts[state] += 1
            
            return {
                'total_agents': len(agent_states),
                'agent_states': dict(state_counts),
                'active_agents': state_counts.get('active', 0),
                'sleeping_agents': state_counts.get('sleeping', 0),
                'error_agents': state_counts.get('error', 0)
            }
        except Exception as e:
            logger.error(f"Error getting AI metrics: {e}")
            return {'error': str(e)}

class ExtendedMonitor:
    """Main extended monitoring class"""
    
    def __init__(self):
        self.system_metrics = SystemMetrics()
        self.redis_metrics = RedisMetrics()
        self.security_metrics = SecurityMetrics()
        self.ai_metrics = AIMetrics()
        self.start_time = datetime.utcnow()
        
        logger.info("ExtendedMonitor initialized")
    
    async def get_all_extended_metrics(self) -> Dict[str, Any]:
        """Get all extended metrics"""
        try:
            system_metrics = self.system_metrics.get_system_metrics()
            redis_metrics = await self.redis_metrics.get_redis_metrics()
            security_metrics = await self.security_metrics.get_security_metrics()
            ai_metrics = await self.ai_metrics.get_ai_metrics()
            
            return {
                'timestamp': datetime.utcnow().isoformat(),
                'system': system_metrics,
                'redis': redis_metrics,
                'security': security_metrics,
                'ai': ai_metrics,
                'uptime_seconds': (datetime.utcnow() - self.start_time).total_seconds()
            }
        except Exception as e:
            logger.error(f"Error getting extended metrics: {e}")
            return {'error': str(e)}
    
    async def get_system_health_score(self) -> Dict[str, Any]:
        """Calculate an overall system health score"""
        try:
            metrics = await self.get_all_extended_metrics()
            
            # Calculate health score based on various metrics
            score = 100  # Start with perfect score
            
            # Deduct points for high CPU usage
            if 'system' in metrics and 'cpu' in metrics['system']:
                cpu_percent = metrics['system']['cpu']['percent']
                if cpu_percent > 90:
                    score -= 20
                elif cpu_percent > 75:
                    score -= 10
                elif cpu_percent > 50:
                    score -= 5
            
            # Deduct points for high memory usage
            if 'system' in metrics and 'memory' in metrics['system']:
                memory_percent = metrics['system']['memory']['percent']
                if memory_percent > 90:
                    score -= 20
                elif memory_percent > 75:
                    score -= 10
                elif memory_percent > 50:
                    score -= 5
            
            # Deduct points for Redis errors
            if 'redis' in metrics and 'errors' in metrics['redis']:
                redis_errors = metrics['redis']['errors']
                if redis_errors > 10:
                    score -= 15
                elif redis_errors > 5:
                    score -= 10
                elif redis_errors > 0:
                    score -= 5
            
            # Deduct points for security issues
            if 'security' in metrics and 'firewall' in metrics['security']:
                if not metrics['security']['firewall'].get('active', True):
                    score -= 25
            
            # Ensure score is between 0 and 100
            score = max(0, min(100, score))
            
            # Determine health status
            if score >= 90:
                status = "healthy"
            elif score >= 70:
                status = "degraded"
            else:
                status = "unhealthy"
            
            return {
                'health_score': score,
                'status': status,
                'metrics_used': metrics,
                'timestamp': datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Error calculating health score: {e}")
            return {'error': str(e)}

# Global extended monitor instance
extended_monitor = ExtendedMonitor()

# Convenience functions
async def get_extended_metrics() -> Dict[str, Any]:
    """Get all extended metrics"""
    return await extended_monitor.get_all_extended_metrics()

async def get_health_score() -> Dict[str, Any]:
    """Get system health score"""
    return await extended_monitor.get_system_health_score()