import multiprocessing
import time
import os
"""
start a multiprocessing example
multiprocessing.Process(function, args)

put the process in a list
join the process to wait for it to finish

for p in processes:
    p.join()
"""
# Example 1: Basic Process Creation
def worker_function(name):
    """A simple worker function that simulates some work"""
    print(f"Process {name} starting (PID: {os.getpid()})")
    time.sleep(2)  # Simulate some work
    print(f"Process {name} finished")

def basic_multiprocessing():
    print("Starting basic multiprocessing example")
    # Create and start processes
    processes = []
    for i in range(3):
        p = multiprocessing.Process(target=worker_function, args=(f"Worker-{i}",))
        processes.append(p)
        p.start()
    # Wait for all processes to complete
    for p in processes:
        p.join()
    print("All processes completed")


if __name__ == "__main__":
    # Note: This guard is important for multiprocessing on Windows
    print(f"Main process PID: {os.getpid()}")
    print(f"Number of CPU cores: {multiprocessing.cpu_count()}")
    # Run examples
    basic_multiprocessing()
