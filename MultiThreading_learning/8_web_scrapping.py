import threading
import requests
import time
from queue import Queue

def fetch_url(url):
    """Simulate fetching a URL"""
    print(f"Fetching {url}")
    time.sleep(2)  # Simulate network delay
    return f"Content from {url}"


def worker(queue, results, lock):
    """Worker thread function"""
    while True:
        url = queue.get()
        if url is None:
            break     
        result = fetch_url(url)   
        ## Make sure to lock when accessing shared resources   
        with lock:
            results.append(result)
            print (f"\t \t Fetched and stored result for {url}")
            print(f"\t \t Total results stored: {len(results)}")   
        queue.task_done()
# URLs to fetch
urls = [
    "http://example.com/page1",
    "http://example.com/page2",
    "http://example.com/page3",
    "http://example.com/page4",
    "http://example.com/page5"
]
# Create queue and add URLs
url_queue = Queue()
for url in urls:
    url_queue.put(url)
# Results storage
results = []
results_lock = threading.Lock()
# Create and start worker threads
threads = []
for i in range(3):  # 3 worker threads
    thread = threading.Thread(target=worker, args=(url_queue, results, results_lock))
    threads.append(thread)
    thread.start()
# Wait for all tasks to complete
url_queue.join()
# Signal threads to exit
for _ in threads:
    url_queue.put(None)
# Wait for threads to finish
for thread in threads:
    thread.join()
print(f"Fetched {len(results)} URLs")
print("All tasks completed")
print(results)