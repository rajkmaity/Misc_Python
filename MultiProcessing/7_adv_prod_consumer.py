import multiprocessing
import time
import random
from multiprocessing import Queue, Pipe, Value, Array, Lock, Manager


def producer(queue, num_items):
    """Producer that generates items"""
    for i in range(num_items):
        item = f"item_{i}"
        queue.put(item)
        print(f"Produced: {item}")
        time.sleep(0.1)
    # Signal completion
    queue.put(None)

def consumer(queue, consumer_id):
    """Consumer that processes items"""
    while True:
        item = queue.get()
        if item is None:
            # Put None back for other consumers
            queue.put(None)
            break
        print(f"Consumer {consumer_id} processing: {item}")
        time.sleep(0.2)  # Simulate processing time

def producer_consumer_example():
    print("\nProducer-Consumer example:")
    # Create queue
    queue = multiprocessing.Queue()
    # Create producer process
    producer_proc = multiprocessing.Process(target=producer, args=(queue, 10))
    # Create consumer processes
    consumer_procs = []
    for i in range(3):
        p = multiprocessing.Process(target=consumer, args=(queue, i))
        consumer_procs.append(p)
    # Start all processes
    producer_proc.start()
    for p in consumer_procs:
        p.start()
    # Wait for producer to finish
    producer_proc.join()
    # Wait for consumers to finish
    for p in consumer_procs:
        p.join()


if __name__ == "__main__":
    producer_consumer_example()