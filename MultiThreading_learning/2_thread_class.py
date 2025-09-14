import threading
import time

class WorkerThread(threading.Thread):
    def __init__(self, name, delay):
        super().__init__()
        self.name = name
        self.delay = delay
    
    def run(self):
        print(f"Thread {self.name} starting")
        time.sleep(self.delay)
        print(f"Thread {self.name} finished")

# Create and start threads
threads = []
for i in range(3):
    thread = WorkerThread(f"Worker-{i}", 5 -i )
    threads.append(thread)
    thread.start()


print("-------------------------------")
print("The threads are going to start in order.")
print("As the delay are more for lower rank")
print("They will finish in reverse order.")
print("-------------------------------")
# Wait for all threads to complete
for thread in threads:
    thread.join()