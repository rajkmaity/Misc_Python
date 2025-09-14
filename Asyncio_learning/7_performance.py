import asyncio
import aiohttp
import time
from typing import List, Dict, Any


async def performance_comparison():
    """Compare sync vs async performance"""
    
    urls = ['https://httpbin.org/delay/1'] * 5  # 5 URLs with 1-second delay each
    
    # Async version
    start_time = time.time()
    async with aiohttp.ClientSession() as session:
        tasks = [
            asyncio.create_task(session.get(url))
            for url in urls
        ]
        responses = await asyncio.gather(*tasks)
        # Close responses
        for response in responses:
            response.close()
    
    async_time = time.time() - start_time
    
    return {
        "urls_count": len(urls),
        "async_time": async_time,
        "note": "Async version processes all URLs concurrently"
    }

async def main():
    print("=== Performance Comparison ===")
    perf_results = await performance_comparison()
    print(f"Performance: {perf_results['urls_count']} URLs in {perf_results['async_time']:.2f}s")
    
    ## Not asynchronous version is commented out to avoid blocking the event loop
    print("Starting synchronous version (this will block)...")
    start_time = time.time()
    import requests
    for url in ['https://httpbin.org/delay/1'] * 5:
        response = requests.get(url)
        response.close()
    sync_time = time.time() - start_time
    print(f"Synchronous version took {sync_time:.2f}s")
    
if __name__ == "__main__":
    asyncio.run(main())