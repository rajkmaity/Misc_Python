import multiprocessing
import time
import random
from multiprocessing import Queue, Pipe, Value, Array, Lock, Manager

# Inter-process Communication with Pipes
def sender(conn, data):
    """Send data through pipe"""
    for item in data:
        conn.send(item)
        time.sleep(0.1)
    conn.send("DONE")
    conn.close()

def receiver(conn):
    """Receive data through pipe"""
    while True:
        msg = conn.recv()
        if msg == "DONE":
            break
        print(f"Received: {msg}")
    conn.close()

def pipe_example():
    print("Pipe communication example:")
    # Create a pipe
    parent_conn, child_conn = multiprocessing.Pipe()
    # Data to send
    data = ["Hello", "World", "From", "Multiprocessing"]
    # Create processes
    sender_process = multiprocessing.Process(target=sender, args=(parent_conn, data))
    receiver_process = multiprocessing.Process(target=receiver, args=(child_conn,))
    # Start processes
    sender_process.start()
    receiver_process.start()
    # Wait for completion
    sender_process.join()
    receiver_process.join()
    
if __name__ == "__main__":
    pipe_example()