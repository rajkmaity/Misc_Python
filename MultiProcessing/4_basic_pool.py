import multiprocessing
import time
import os

def square_number(x):
    """Simple function to square a number"""
    return x * x

def process_pool_examples():
    print("\nProcess Pool examples:")
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    with multiprocessing.Pool(processes=4) as pool:
        # Method 1: map() - applies function to each element
        squares = pool.map(square_number, numbers)
        print(f"Squares using map(): {squares}")
        # Method 2: starmap() - for functions with multiple arguments
        pairs = [(2, 3), (4, 5), (6, 7)]
        powers = pool.starmap(pow, pairs)
        print(f"Powers using starmap(): {powers}")
        # Method 3: apply_async() - asynchronous execution
        async_results = []
        for num in numbers[:5]:
            result = pool.apply_async(square_number, (num,))
            async_results.append(result)
        # Get results from async operations
        async_squares = [result.get() for result in async_results]
        print(f"Squares using apply_async(): {async_squares}")

if __name__ == "__main__":
    # Note: This guard is important for multiprocessing on Windows
    print(f"Main process PID: {os.getpid()}")
    print(f"Number of CPU cores: {multiprocessing.cpu_count()}")

    process_pool_examples()