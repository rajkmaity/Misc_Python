import multiprocessing
import time
import os



def worker_with_result(name, queue):
    """Worker function that returns a result via queue"""
    result = f"Result from {name}: {sum(range(1000000))}"
    queue.put(result)

def multiprocessing_with_queue():
    print("\nMultiprocessing with Queue example")
    # Create a queue to collect results
    result_queue = multiprocessing.Queue() 
    # Create and start processes
    processes = []
    for i in range(3):
        p = multiprocessing.Process(target=worker_with_result, 
                                    args=(f"Process-{i}", result_queue))
        processes.append(p)
        p.start()
    # Wait for all processes to complete
    for p in processes:
        p.join()
    # Collect results from queue
    results = []
    while not result_queue.empty():
        results.append(result_queue.get())
    for result in results:
        print(result)


if __name__ == "__main__":
    # Note: This guard is important for multiprocessing on Windows
    print(f"Main process PID: {os.getpid()}")
    print(f"Number of CPU cores: {multiprocessing.cpu_count()}")
    multiprocessing_with_queue()