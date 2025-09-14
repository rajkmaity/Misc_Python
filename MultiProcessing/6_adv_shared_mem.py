import multiprocessing
import time
import random
from multiprocessing import Queue, Pipe, Value, Array, Lock, Manager

def worker_with_shared_memory(shared_value, shared_array, lock, worker_id):
    """Worker that modifies shared memory"""
    for i in range(5):
        time.sleep(random.uniform(0.1, 0.3))
        # Use lock to safely modify shared data
        with lock:
            shared_value.value += 1
            shared_array[worker_id] = shared_value.value
            print(f"Worker {worker_id}: shared_value = {shared_value.value}")

def shared_memory_example():
    print("\nShared Memory example:")
    # Create shared memory objects
    shared_value = multiprocessing.Value('i', 0)  # 'i' for integer
    shared_array = multiprocessing.Array('i', [0] * 4)  # Array of 4 integers
    lock = multiprocessing.Lock()
    # Create processes
    processes = []
    for i in range(4):
        p = multiprocessing.Process(target=worker_with_shared_memory,
                                  args=(shared_value, shared_array, lock, i))
        processes.append(p)
        p.start()
    # Wait for all processes
    for p in processes:
        p.join()
    print(f"Final shared_value: {shared_value.value}")
    print(f"Final shared_array: {list(shared_array)}")


if __name__ == "__main__":
    shared_memory_example()