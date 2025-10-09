"""
Performance Monitoring Dashboard for HoloMesh Interaction Modes
"""

import asyncio
import json
import time
from typing import Dict, Any, List
from dataclasses import dataclass, asdict
from collections import defaultdict
import numpy as np

@dataclass
class OptimizationRecord:
    """Record of a single optimization run"""
    timestamp: float
    tool_name: str
    interaction_mode: str
    strategy: str
    execution_time: float
    iterations: int
    confidence_score: float
    final_metrics: Dict[str, float]
    success: bool
    project_id: str
    process_id: str

class PerformanceMonitor:
    """Monitor and analyze performance of HoloMesh interaction modes"""
    
    def __init__(self):
        self.records: List[OptimizationRecord] = []
        self.mode_stats = defaultdict(lambda: {
            "total_runs": 0,
            "successful_runs": 0,
            "total_execution_time": 0.0,
            "total_iterations": 0,
            "confidence_scores": [],
            "metrics_history": defaultdict(list)
        })
    
    def record_optimization(self, record: OptimizationRecord):
        """Record an optimization run"""
        self.records.append(record)
        
        # Update mode statistics
        mode_key = f"{record.tool_name}_{record.interaction_mode}"
        stats = self.mode_stats[mode_key]
        
        stats["total_runs"] += 1
        if record.success:
            stats["successful_runs"] += 1
        
        stats["total_execution_time"] += record.execution_time
        stats["total_iterations"] += record.iterations
        stats["confidence_scores"].append(record.confidence_score)
        
        # Store metrics history
        for metric_name, value in record.final_metrics.items():
            stats["metrics_history"][metric_name].append(value)
    
    def get_mode_performance(self, tool_name: str, interaction_mode: str) -> Dict[str, Any]:
        """Get performance statistics for a specific mode"""
        mode_key = f"{tool_name}_{interaction_mode}"
        stats = self.mode_stats[mode_key]
        
        if stats["total_runs"] == 0:
            return {"error": "No data available"}
        
        success_rate = stats["successful_runs"] / stats["total_runs"]
        avg_execution_time = stats["total_execution_time"] / stats["total_runs"]
        avg_iterations = stats["total_iterations"] / stats["total_runs"]
        avg_confidence = np.mean(stats["confidence_scores"]) if stats["confidence_scores"] else 0.0
        
        # Calculate metric averages and improvements
        metric_averages = {}
        metric_improvements = {}
        for metric_name, values in stats["metrics_history"].items():
            if values:
                metric_averages[metric_name] = np.mean(values)
                if len(values) > 1:
                    metric_improvements[metric_name] = (values[-1] - values[0]) / values[0] if values[0] != 0 else 0.0
        
        return {
            "mode": interaction_mode,
            "tool": tool_name,
            "total_runs": stats["total_runs"],
            "success_rate": success_rate,
            "avg_execution_time": avg_execution_time,
            "avg_iterations": avg_iterations,
            "avg_confidence_score": avg_confidence,
            "metric_averages": metric_averages,
            "metric_improvements": metric_improvements
        }
    
    def get_overall_performance(self) -> Dict[str, Any]:
        """Get overall performance across all modes"""
        all_modes = list(self.mode_stats.keys())
        mode_performances = []
        
        for mode_key in all_modes:
            tool_name, interaction_mode = mode_key.split("_", 1)
            performance = self.get_mode_performance(tool_name, interaction_mode)
            if "error" not in performance:
                mode_performances.append(performance)
        
        if not mode_performances:
            return {"error": "No data available"}
        
        # Aggregate statistics
        total_runs = sum(p["total_runs"] for p in mode_performances)
        avg_success_rate = np.mean([p["success_rate"] for p in mode_performances])
        avg_execution_time = np.mean([p["avg_execution_time"] for p in mode_performances])
        avg_confidence = np.mean([p["avg_confidence_score"] for p in mode_performances])
        
        # Find best performing modes
        best_success_rate = max(mode_performances, key=lambda x: x["success_rate"])
        fastest_execution = min(mode_performances, key=lambda x: x["avg_execution_time"])
        highest_confidence = max(mode_performances, key=lambda x: x["avg_confidence_score"])
        
        return {
            "total_optimizations": total_runs,
            "avg_success_rate": avg_success_rate,
            "avg_execution_time": avg_execution_time,
            "avg_confidence_score": avg_confidence,
            "best_success_rate_mode": {
                "mode": best_success_rate["mode"],
                "tool": best_success_rate["tool"],
                "rate": best_success_rate["success_rate"]
            },
            "fastest_execution_mode": {
                "mode": fastest_execution["mode"],
                "tool": fastest_execution["tool"],
                "time": fastest_execution["avg_execution_time"]
            },
            "highest_confidence_mode": {
                "mode": highest_confidence["mode"],
                "tool": highest_confidence["tool"],
                "confidence": highest_confidence["avg_confidence_score"]
            },
            "mode_count": len(mode_performances)
        }
    
    def get_recent_records(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent optimization records"""
        recent = sorted(self.records, key=lambda x: x.timestamp, reverse=True)[:limit]
        return [asdict(record) for record in recent]
    
    def export_data(self) -> Dict[str, Any]:
        """Export all monitoring data"""
        return {
            "records": [asdict(record) for record in self.records],
            "mode_stats": dict(self.mode_stats),
            "export_timestamp": time.time()
        }

# Global performance monitor instance
_performance_monitor = None

def get_performance_monitor() -> PerformanceMonitor:
    """Get the global performance monitor instance"""
    global _performance_monitor
    if _performance_monitor is None:
        _performance_monitor = PerformanceMonitor()
    return _performance_monitor

def record_optimization_result(tool_name: str, interaction_mode: str, strategy: str,
                             execution_time: float, iterations: int, confidence_score: float,
                             final_metrics: Dict[str, float], success: bool,
                             project_id: str, process_id: str):
    """Record an optimization result in the performance monitor"""
    monitor = get_performance_monitor()
    record = OptimizationRecord(
        timestamp=time.time(),
        tool_name=tool_name,
        interaction_mode=interaction_mode,
        strategy=strategy,
        execution_time=execution_time,
        iterations=iterations,
        confidence_score=confidence_score,
        final_metrics=final_metrics,
        success=success,
        project_id=project_id,
        process_id=process_id
    )
    monitor.record_optimization(record)