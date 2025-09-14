import asyncio
import aiohttp
import time
from typing import List, Dict, Any


async def multiple_requests_basic():
    """Making multiple requests with a single session
    - Create a single ClientSession to be reused for all requests.
    - Iterate over the list of URLs, making a GET request for each.
    - Collect and return the JSON responses in a list.
    
    """
    urls = [
        'https://httpbin.org/get?page=1',
        'https://httpbin.org/get?page=2',
        'https://httpbin.org/get?page=3'
    ]
 
    async with aiohttp.ClientSession() as session:
        results = []
        for url in urls:
            async with session.get(url) as response:
                print(f"Fetching {url}...")
                data = await response.json()
                await asyncio.sleep(1)
                results.append(data)
        
        return results
    
    
async def main():
    
    print("Multiple Requests Example")
    results = await multiple_requests_basic()
    print(f"Fetched {len(results)} URLs\n")
    for i, result in enumerate(results, start=1):
        print(f"Result {i}: {result['args']}")

if __name__ == "__main__":
    asyncio.run(main())