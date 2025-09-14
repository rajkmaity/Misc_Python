import threading
import time

"""
Write the function 

Create thread = threading.Thread(target=worker_function, args=("A", 3))
that will run in a separate thread and demonstrate starting and joining threads.

then start the threads using thread.start()

then join the threads to wait for their completion.
that will run in a separate thread and demonstrate starting and joining threads.

"""


def worker_function(name, delay):
    """Function that will run in a separate thread"""
    print(f"Thread {name} starting")
    time.sleep(delay)
    print(f"Thread {name} finished after {delay} seconds")

# Create threads
thread1 = threading.Thread(target=worker_function, args=("A", 3))
thread2 = threading.Thread(target=worker_function, args=("B", 1))

# Start threads
thread1.start()
thread2.start()

# Wait for threads to complete
thread1.join()
thread2.join()

print("All threads completed")