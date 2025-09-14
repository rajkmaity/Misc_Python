import threading
import time

"""
start an event : event = threading.Event()
wait for the event to be set : event.wait()
set the event : event.set()
clear the event : event.clear()
is the event set: event.is_set()
"""

event = threading.Event()

def waiter(name):
    print(f"{name} waiting for event")
    event.wait()
    print(f"{name} received event")

def setter():
    print("Setting event in 3 seconds")
    time.sleep(3)
    event.set()
    print("Event set")

# Create threads
waiter_thread = threading.Thread(target=waiter, args=("Waiter",))
setter_thread = threading.Thread(target=setter)

waiter_thread.start()
setter_thread.start()

waiter_thread.join()
setter_thread.join()

print("is the event set?", event.is_set())
event.clear()
print("is the event set after clear?", event.is_set())
print("Event cleared")