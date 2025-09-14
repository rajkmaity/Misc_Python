import multiprocessing
import time
import random
from multiprocessing import Queue, Pipe, Value, Array, Lock, Manager


def worker_with_manager(shared_dict, shared_list, worker_id):
    """Worker using managed shared objects"""
    # Add to shared dictionary
    shared_dict[f"worker_{worker_id}"] = f"Hello from worker {worker_id}"
    # Add to shared list
    shared_list.append(f"Item from worker {worker_id}")
    time.sleep(0.1)

def manager_example():
    print("\nManager example:")
    # Create a manager
    manager = multiprocessing.Manager()
    # Create shared objects
    shared_dict = manager.dict()
    shared_list = manager.list()
    # Create processes
    processes = []
    for i in range(4):
        p = multiprocessing.Process(target=worker_with_manager,
                                  args=(shared_dict, shared_list, i))
        processes.append(p)
        p.start()
    
    # Wait for all processes
    for p in processes:
        p.join()
    print(f"Shared dictionary: {dict(shared_dict)}")
    print(f"Shared list: {list(shared_list)}")


if __name__ == "__main__":
    manager_example()
