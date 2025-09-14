import threading
import time

# Shared resource
counter = 0
lock = threading.Lock()

def increment_counter(name):
    global counter
    for _ in range(10):
        with lock:  # Acquire lock before modifying shared resource
            counter += 1
            print(f"{name} incremented counter to {counter}")
            time.sleep(0.1)  # Simulate some work
    print(f"Thread {name} finished")

# Create threads
## Make it count to 100000


threads = []
for i in range(3):
    thread = threading.Thread(target=increment_counter, args=(f"Thread-{i}",))
    threads.append(thread)
    thread.start()

# Wait for completion
for th in threads:
    th.join()

print(f"Final counter value: {counter}")