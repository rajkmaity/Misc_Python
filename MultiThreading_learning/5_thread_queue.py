import threading
import queue
import time
import random

"""
Producer : Produces items and puts them in the queue
        - put all the items in the queue
        - sleep for a random time between 0.1 and 0.5 seconds after producing each item
Consumer : Consumes items from the queue
        - check for the queue for items
        - get item from the queue
        - qu.task_done()
        - sleep for a random time between 0.5 and 1.3 seconds after consuming each item
        - if the queue is empty for 1 second, break the loop and exit
        - mark the task as done after consuming each item
"""

def producer(q, name):
    """Produces items and puts them in the queue"""
    for i in range(5):
        item = f"{name}-item-{i}"
        q.put(item)
        print(f"Produced: {item}")
        time.sleep(random.uniform(0.1, 0.5))
    
def consumer(qu, name):
    """Consumes items from the queue"""
    while True:
        try:
            item = qu.get(timeout=1)
            print(f"\t {name} consumed: {item}")
            time.sleep(random.uniform(0.5, 1.3)*2)
            qu.task_done()
        except queue.Empty:
            break

"""
start a queue.
create a producer thread and a consumer thread.
start producer thread and consumer thread.
join all the threads. producer and consumer.
wait for the queue to be empty.
"""

# Create queue
q = queue.Queue()

# Create producer and consumer threads
producer_thread = threading.Thread(target=producer, args=(q, "Producer"))
consumer_thread = threading.Thread(target=consumer, args=(q, "Consumer"))

producer_thread.start()
consumer_thread.start()

producer_thread.join()
consumer_thread.join()