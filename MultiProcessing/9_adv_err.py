import multiprocessing
import time
import random
from multiprocessing import Queue, Pipe, Value, Array, Lock, Manager


def unreliable_worker(worker_id):
    """Worker that might fail or take long time"""
    if worker_id == 2:
        raise ValueError(f"Worker {worker_id} failed!")
    
    if worker_id == 3:
        time.sleep(10)  # This will timeout
    
    return f"Worker {worker_id} completed successfully"

def error_handling_example():
    print("\nError handling example:")
    
    with multiprocessing.Pool(processes=4) as pool:
        # Submit tasks with timeout
        results = []
        for i in range(5):
            result = pool.apply_async(unreliable_worker, (i,))
            results.append((i, result))
        
        # Collect results with error handling
        for worker_id, result in results:
            try:
                # Wait for result with timeout
                output = result.get(timeout=2)
                print(f"Success: {output}")
            except multiprocessing.TimeoutError:
                print(f"Worker {worker_id} timed out")
            except Exception as e:
                print(f"Worker {worker_id} failed: {e}")


if __name__ == "__main__":

    error_handling_example()