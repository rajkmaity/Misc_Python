import threading
import time



# Allow only 2 threads to access the resource simultaneously
semaphore = threading.Semaphore(2)

def access_resource(name, delay=1):
    with semaphore:
        print(f"{name} acquired semaphore")
        time.sleep(delay)
        print(f"----- {name} --------- releasing semaphore")

# Create 5 threads
threads = []
for i in range(5):
    thread = threading.Thread(target=access_resource, args=(f"Thread-{i}",5-i))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()