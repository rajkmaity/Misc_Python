import asyncio
import aiohttp
import time
from typing import List, Dict, Any

"""
Semaphore Example
- Use asyncio.Semaphore to limit the number of concurrent requests.
- Create tasks for each URL and gather results.

"""

urls = [
        'https://httpbin.org/delay/1',
        'https://httpbin.org/delay/2',
        'https://httpbin.org/delay/1',
        'https://httpbin.org/get?id=1',
        'https://httpbin.org/get?id=2'
    ]

async def fetch_with_semaphore(session: aiohttp.ClientSession,
                              semaphore: asyncio.Semaphore,
                              url: str) -> Dict[str, Any]:
    """Fetch URL with semaphore to limit concurrent requests
    - Acquire semaphore before making the request.
    - Release semaphore after the request is complete.
    - Return the JSON response or error information.
    """
    async with semaphore:  # Acquire semaphore
        print(f"Fetching {url}")
        try:
            async with session.get(url) as response:
                data = await response.json()
                print(f"\t Completed {url}")
                return {"url": url, "status": response.status, "data": data}
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return {"url": url, "error": str(e)}

# 5. TASK CREATION AND GATHERING
async def fetch_urls_with_tasks():
    """Using asyncio.create_task() and asyncio.gather()"""
    
    
    # Create semaphore to limit concurrent requests
    semaphore = asyncio.Semaphore(3)  # Max 3 concurrent requests
    # Creqate a session for making requests // only one session is needed
    async with aiohttp.ClientSession() as session:
        # Create tasks for all URLs
        tasks = [
            asyncio.create_task(fetch_with_semaphore(session, semaphore, url))
            for url in urls
        ]
        
        # Wait for all tasks to complete
        results = await asyncio.gather(*tasks)
        return results

async def main():
    results = await fetch_urls_with_tasks()
    print(f"Fetched {len(results)} URLs\n")
    for i, result in enumerate(results, start=1):
        if "error" in result:
            print(f"Result {i}: Error fetching {result['url']}: {result['error']}")
        else:
            print(f"Result {i}: Fetched {result['url']} with status {result['status']}")


if __name__ == "__main__":
    print("All urls:")
    print(urls)
    asyncio.run(main())