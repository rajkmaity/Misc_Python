import multiprocessing
import time
import random
from functools import partial

# Basic function for demonstrations
def square(x):
    """Simple function to square a number"""
    print(f"Processing {x} in process {multiprocessing.current_process().name}")
    time.sleep(0.1)  # Simulate some work
    return x * x

def slow_function(x):
    """Function that takes variable time to complete"""
    sleep_time = random.uniform(0.1, 0.5)
    time.sleep(sleep_time)
    return x * 2, sleep_time

# =============================================================================
# BASIC POOL CREATION AND USAGE
# =============================================================================

def basic_pool_example():
    print("1. Basic Pool Creation and Usage")
    print("=" * 50)
    
    # Method 1: Basic pool creation
    pool = multiprocessing.Pool(processes=4)
    
    numbers = [1, 2, 3, 4, 5, 6, 7, 8]
    results = pool.map(square, numbers)
    
    print(f"Input: {numbers}")
    print(f"Results: {results}")
    
    # Important: Always close and join the pool
    pool.close()  # No more tasks will be submitted
    pool.join()   # Wait for all processes to complete
    
    print("\n" + "="*50 + "\n")

def context_manager_pool():
    print("2. Using Pool with Context Manager (Recommended)")
    print("=" * 50)
    
    numbers = [1, 2, 3, 4, 5, 6, 7, 8]
    
    # Context manager automatically handles close() and join()
    with multiprocessing.Pool(processes=4) as pool:
        results = pool.map(square, numbers)
    
    print(f"Input: {numbers}")
    print(f"Results: {results}")
    print("\n" + "="*50 + "\n")

# =============================================================================
# POOL METHODS: map, imap, starmap, apply_async, etc.
# =============================================================================

def map_method_example():
    print("3. Pool.map() - Blocking, Returns Results in Order")
    print("=" * 50)
    
    with multiprocessing.Pool(processes=4) as pool:
        numbers = list(range(1, 9))
        
        start_time = time.time()
        results = pool.map(square, numbers)
        end_time = time.time()
        
        print(f"Results: {results}")
        print(f"Time taken: {end_time - start_time:.2f} seconds")
        print("Note: Results are returned in the same order as input")
    
    print("\n" + "="*50 + "\n")

def imap_method_example():
    print("4. Pool.imap() - Non-blocking Iterator")
    print("=" * 50)
    
    with multiprocessing.Pool(processes=4) as pool:
        numbers = list(range(1, 9))
        
        print("Processing with imap (results as they complete):")
        result_iterator = pool.imap(square, numbers)
        
        # Process results as they become available
        for i, result in enumerate(result_iterator):
            print(f"Got result {i+1}: {result}")
    
    print("\n" + "="*50 + "\n")

def imap_unordered_example():
    print("5. Pool.imap_unordered() - Results in Completion Order")
    print("=" * 50)
    
    with multiprocessing.Pool(processes=4) as pool:
        numbers = list(range(1, 9))
        
        print("Processing with imap_unordered:")
        result_iterator = pool.imap_unordered(slow_function, numbers)
        
        for result in result_iterator:
            value, sleep_time = result
            print(f"Got result: {value} (took {sleep_time:.2f}s)")
    
    print("\n" + "="*50 + "\n")

def starmap_example():
    print("6. Pool.starmap() - For Functions with Multiple Arguments")
    print("=" * 50)
    
    def power(base, exponent):
        """Function that takes multiple arguments"""
        result = base ** exponent
        print(f"{base}^{exponent} = {result}")
        return result
    
    with multiprocessing.Pool(processes=4) as pool:
        # List of tuples, each tuple contains arguments for one function call
        arguments = [(2, 3), (4, 2), (5, 3), (3, 4), (6, 2)]
        
        results = pool.starmap(pow, arguments)
        print(f"Results: {results}")
    
    print("\n" + "="*50 + "\n")

def apply_async_example():
    print("7. Pool.apply_async() - Asynchronous Single Function Calls")
    print("=" * 50)
    
    with multiprocessing.Pool(processes=4) as pool:
        # Submit multiple async jobs
        async_results = []
        for i in range(1, 6):
            result = pool.apply_async(square, (i,))
            async_results.append(result)
        
        # Collect results
        print("Collecting results from async jobs:")
        for i, async_result in enumerate(async_results):
            result = async_result.get()  # This blocks until result is ready
            print(f"Job {i+1} result: {result}")
    
    print("\n" + "="*50 + "\n")

def map_async_example():
    print("8. Pool.map_async() - Asynchronous Batch Processing")
    print("=" * 50)
    
    with multiprocessing.Pool(processes=4) as pool:
        numbers = list(range(1, 9))
        
        # Submit the entire batch asynchronously
        async_result = pool.map_async(square, numbers)
        
        # Do other work while processing happens
        print("Submitted batch job, doing other work...")
        time.sleep(0.5)
        
        # Get results when ready
        results = async_result.get()
        print(f"Batch results: {results}")
    
    print("\n" + "="*50 + "\n")

# =============================================================================
# ADVANCED POOL FEATURES
# =============================================================================

def pool_with_initializer():
    print("9. Pool with Initializer Function")
    print("=" * 50)
    
    # Global variable that will be initialized in each worker process
    worker_data = None
    
    def init_worker(initial_value):
        """Initialize each worker process"""
        global worker_data
        worker_data = initial_value
        print(f"Worker {multiprocessing.current_process().name} initialized with {initial_value}")
    
    def worker_function(x):
        """Function that uses the initialized data"""
        global worker_data
        return x * worker_data
    
    with multiprocessing.Pool(processes=4, initializer=init_worker, initargs=(10)) as pool:
        numbers = [1, 2, 3, 4, 5]
        results = pool.map(worker_function, numbers)
        print(f"Results: {results}")
    
    print("\n" + "="*50 + "\n")

def pool_with_callback():
    print("10. Pool with Callback Functions")
    print("=" * 50)
    
    def success_callback(result):
        """Called when a task completes successfully"""
        print(f"✓ Task completed successfully: {result}")
    
    def error_callback(error):
        """Called when a task fails"""
        print(f"✗ Task failed: {error}")
    
    def risky_function(x):
        """Function that might fail"""
        if x == 3:
            raise ValueError(f"Number {x} is not allowed!")
        return x * x
    
    with multiprocessing.Pool(processes=4) as pool:
        # Submit jobs with callbacks
        for i in range(1, 6):
            pool.apply_async(risky_function, (i,), 
                           callback=success_callback, 
                           error_callback=error_callback)
        
        # Wait for all jobs to complete
        pool.close()
        pool.join()
    
    print("\n" + "="*50 + "\n")

def pool_with_timeout():
    print("11. Pool with Timeout Handling")
    print("=" * 50)
    
    def slow_function(x):
        """Function that might take too long"""
        sleep_time = x * 0.5
        time.sleep(sleep_time)
        return x * x
    
    with multiprocessing.Pool(processes=4) as pool:
        numbers = [1, 2, 3, 4, 5]
        
        try:
            # Set timeout for the entire operation
            results = pool.map(slow_function, numbers, timeout=2)
            print(f"Results: {results}")
        except multiprocessing.TimeoutError:
            print("Operation timed out!")
        
        # Individual timeout with apply_async
        print("\nTesting individual timeouts:")
        for i in [1, 3, 5]:  # 3 and 5 will likely timeout
            try:
                result = pool.apply_async(slow_function, (i,))
                value = result.get(timeout=1)  # 1 second timeout
                print(f"Result for {i}: {value}")
            except multiprocessing.TimeoutError:
                print(f"Task with input {i} timed out")
    
    print("\n" + "="*50 + "\n")

def pool_with_partial():
    print("12. Using functools.partial with Pool")
    print("=" * 50)
    
    def multiply_and_add(x, multiplier, addend):
        """Function with multiple parameters"""
        return x * multiplier + addend
    
    with multiprocessing.Pool(processes=4) as pool:
        # Create a partial function with fixed parameters
        multiply_by_3_add_10 = partial(multiply_and_add, multiplier=3, addend=10)
        
        numbers = [1, 2, 3, 4, 5]
        results = pool.map(multiply_by_3_add_10, numbers)
        
        print(f"Input: {numbers}")
        print(f"Results (x*3+10): {results}")
    
    print("\n" + "="*50 + "\n")

# =============================================================================
# PRACTICAL EXAMPLES
# =============================================================================

def image_processing_simulation():
    print("13. Practical Example: Image Processing Simulation")
    print("=" * 50)
    
    def process_image(image_name):
        """Simulate image processing"""
        print(f"Processing {image_name}...")
        
        # Simulate processing time
        processing_time = random.uniform(0.5, 1.5)
        time.sleep(processing_time)
        
        # Simulate processing result
        result = {
            'image': image_name,
            'size': random.randint(1024, 4096),
            'processing_time': processing_time,
            'status': 'success'
        }
        
        print(f"Finished processing {image_name}")
        return result
    
    # Simulate list of images
    images = [f"image_{i:03d}.jpg" for i in range(1, 11)]
    
    print(f"Processing {len(images)} images...")
    
    start_time = time.time()
    
    with multiprocessing.Pool(processes=4) as pool:
        results = pool.map(process_image, images)
    
    end_time = time.time()
    
    print(f"\nProcessed {len(images)} images in {end_time - start_time:.2f} seconds")
    print("Results summary:")
    for result in results:
        print(f"  {result['image']}: {result['size']}px, {result['processing_time']:.2f}s")
    
    print("\n" + "="*50 + "\n")

def data_processing_with_chunksize():
    print("14. Optimizing with Chunksize")
    print("=" * 50)
    
    def simple_computation(x):
        """Simple computation for demonstration"""
        return sum(i * i for i in range(x))
    
    # Large dataset
    data = list(range(1, 1001))
    
    with multiprocessing.Pool(processes=4) as pool:
        # Test different chunksizes
        for chunksize in [1, 10, 50, 100]:
            start_time = time.time()
            results = pool.map(simple_computation, data, chunksize=chunksize)
            end_time = time.time()
            
            print(f"Chunksize {chunksize}: {end_time - start_time:.2f} seconds")
    
    print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    print("MULTIPROCESSING.POOL COMPREHENSIVE GUIDE")
    print("=" * 60)
    print(f"Available CPU cores: {multiprocessing.cpu_count()}")
    print()
    
    # Run all examples
    basic_pool_example()
    context_manager_pool()
    map_method_example()
    imap_method_example()
    imap_unordered_example()
    starmap_example()
    apply_async_example()
    map_async_example()
 #   pool_with_initializer()
    pool_with_callback()
    pool_with_timeout()
    pool_with_partial()
    image_processing_simulation()
    data_processing_with_chunksize()
    
    print("Guide completed!")