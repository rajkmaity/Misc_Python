from concurrent.futures import ThreadPoolExecutor
import time

def task(n, delay):
    print(f"Task {n} starting")
    time.sleep(delay)
    return f"Task {n} completed"

start = time.time()
# Using ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=3) as executor:
    # Submit tasks
    futures = [executor.submit(task, i,5-i) for i in range(5)]
    
    # Get results
    for future in futures:
        result = future.result()
        print(result)
end = time.time()
print(f"All tasks completed in {end - start:.2f} seconds")
print("All tasks completed")