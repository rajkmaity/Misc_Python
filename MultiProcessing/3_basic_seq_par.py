import multiprocessing
import time
import os


def cpu_intensive_task(n):
    """CPU-intensive task for demonstration"""
    total = 0
    for i in range(n):
        total += i ** 2
    return total

def sequential_execution():
    """Run tasks sequentially"""
    print("\nSequential execution:")
    start_time = time.time()
    
    results = []
    for _ in range(4):
        result = cpu_intensive_task(1000000)
        results.append(result)
    
    end_time = time.time()
    print(f"Sequential time: {end_time - start_time:.2f} seconds")
    return results

def parallel_execution():
    """Run tasks in parallel using multiprocessing"""
    print("\nParallel execution:")
    start_time = time.time()
    
    with multiprocessing.Pool(processes=4) as pool:
        # Map the function to multiple arguments
        results = pool.map(cpu_intensive_task, [1000000] * 4)
    
    end_time = time.time()
    print(f"Parallel time: {end_time - start_time:.2f} seconds")
    return results

if __name__ == "__main__":
    # Note: This guard is important for multiprocessing on Windows
    print(f"Main process PID: {os.getpid()}")
    print(f"Number of CPU cores: {multiprocessing.cpu_count()}")
    
    
    # Compare sequential vs parallel execution
    sequential_execution()
    parallel_execution()
