import multiprocessing
import time
import random
from multiprocessing import Queue, Pipe, Value, Array, Lock, Manager



def process_file(filename):
    """Simulate processing a file"""
    print(f"Processing {filename}...")
    time.sleep(random.uniform(0.5, 1.5))  # Simulate processing time
    
    # Simulate some result
    word_count = random.randint(100, 1000)
    return {"filename": filename, "word_count": word_count}

def parallel_file_processing():
    print("\nParallel file processing example:")
    
    # Simulate list of files
    files = [f"file_{i}.txt" for i in range(10)]
    
    start_time = time.time()
    
    # Process files in parallel
    with multiprocessing.Pool(processes=4) as pool:
        results = pool.map(process_file, files)
    
    end_time = time.time()
    
    print(f"Processed {len(files)} files in {end_time - start_time:.2f} seconds")
    print("Results:")
    for result in results:
        print(f"  {result['filename']}: {result['word_count']} words")


if __name__ == "__main__":
    parallel_file_processing()