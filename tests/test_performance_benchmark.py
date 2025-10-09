"""
Performance benchmark test for Redis optimization in GlobalScope MultiFrame 11.0
This file tests the performance improvements of the optimized Redis client.
"""
import asyncio
import time
import json
from redis.asyncio import Redis
from src.lib.redis_client import redis_client

async def benchmark_original_redis():
    """Benchmark original Redis client performance"""
    # Create original Redis client
    original_client = Redis(host="redis-master", port=6379, decode_responses=True)
    
    start_time = time.time()
    
    # Perform a series of operations
    for i in range(100):
        key = f"original_test_{i}"
        value = f"original_value_{i}"
        
        # Set operation
        await original_client.set(key, value)
        
        # Get operation
        retrieved_value = await original_client.get(key)
        
        # JSON operation
        json_value = {"id": i, "data": value}
        await original_client.set(f"json_{key}", json.dumps(json_value))
        retrieved_json = await original_client.get(f"json_{key}")
        parsed_json = json.loads(retrieved_json)
    
    end_time = time.time()
    await original_client.close()
    
    return end_time - start_time

async def benchmark_optimized_redis():
    """Benchmark optimized Redis client performance"""
    start_time = time.time()
    
    # Perform a series of operations
    for i in range(100):
        key = f"optimized_test_{i}"
        value = f"optimized_value_{i}"
        
        # Set operation
        await redis_client.set(key, value)
        
        # Get operation
        retrieved_value = await redis_client.get(key)
        
        # JSON operation
        json_value = {"id": i, "data": value}
        await redis_client.set_json(f"json_{key}", json_value)
        retrieved_json = await redis_client.get_json(f"json_{key}")
    
    end_time = time.time()
    
    return end_time - start_time

async def benchmark_caching_performance():
    """Benchmark caching performance"""
    start_time = time.time()
    
    # Perform operations with caching
    for i in range(100):
        key = f"cache_test_{i}"
        value = f"cache_value_{i}"
        
        # Set with caching
        await redis_client.set(key, value, use_cache=True)
        
        # Get with caching (should be faster on second access)
        retrieved_value1 = await redis_client.get(key, use_cache=True)
        retrieved_value2 = await redis_client.get(key, use_cache=True)
    
    end_time = time.time()
    
    return end_time - start_time

async def run_performance_benchmarks():
    """Run all performance benchmarks and compare results"""
    print("Running Redis performance benchmarks...")
    print("=" * 50)
    
    # Test 1: Original Redis client
    print("Testing original Redis client...")
    original_time = await benchmark_original_redis()
    print(f"Original Redis client time: {original_time:.4f} seconds")
    
    # Test 2: Optimized Redis client
    print("\nTesting optimized Redis client...")
    optimized_time = await benchmark_optimized_redis()
    print(f"Optimized Redis client time: {optimized_time:.4f} seconds")
    
    # Test 3: Caching performance
    print("\nTesting caching performance...")
    cache_time = await benchmark_caching_performance()
    print(f"Caching performance time: {cache_time:.4f} seconds")
    
    # Calculate improvements
    if original_time > 0:
        improvement = ((original_time - optimized_time) / original_time) * 100
        print(f"\nPerformance improvement: {improvement:.2f}%")
    
    # Summary
    print("\n" + "=" * 50)
    print("PERFORMANCE BENCHMARK SUMMARY")
    print("=" * 50)
    print(f"Original Redis client:     {original_time:.4f} seconds")
    print(f"Optimized Redis client:    {optimized_time:.4f} seconds")
    print(f"Caching performance:       {cache_time:.4f} seconds")
    
    if original_time > optimized_time:
        improvement = ((original_time - optimized_time) / original_time) * 100
        print(f"Overall improvement:       {improvement:.2f}%")
        print("✅ Optimization successful!")
    else:
        print("⚠️  No significant improvement detected")
    
    return {
        "original_time": original_time,
        "optimized_time": optimized_time,
        "cache_time": cache_time,
        "improvement": ((original_time - optimized_time) / original_time * 100) if original_time > 0 else 0
    }

if __name__ == "__main__":
    # Run performance benchmarks
    results = asyncio.run(run_performance_benchmarks())
    
    # Save results to file
    with open("performance_benchmark_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to performance_benchmark_results.json")