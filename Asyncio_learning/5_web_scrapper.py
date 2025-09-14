import asyncio
import aiohttp
import time
from typing import List, Dict, Any

async def advanced_web_scraper():
    """Advanced example with error handling, timeouts, and retries"""
    
    async def fetch_with_retry(session: aiohttp.ClientSession,
                               semaphore: asyncio.Semaphore,
                               url: str,
                               max_retries: int = 3) -> Dict[str, Any]:
        """Fetch URL with retry logic"""
        ## First, acquire the semaphore to limit concurrent requests
        ## Then, make the request with error handling and retries
        ## Use exponential backoff for retries
        
        async with semaphore:
            for attempt in range(max_retries):
                try:
                    timeout = aiohttp.ClientTimeout(total=20)
                    async with session.get(url, timeout=timeout) as response:
                        print(f"Starting fetch for {url}")
                        if response.status == 200:
                            data = await response.json()
                            return {
                                "url": url, "status": response.status, "data": data,"attempt": attempt + 1
                            }
                        else:
                            print(f"\t \t HTTP {response.status} for {url}")
                except asyncio.TimeoutError:
                    print(f"\t \t Timeout for {url}, attempt {attempt + 1}")
                except Exception as e:
                    print(f"\t \t Error for {url}, attempt {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
            return {"url": url, "error": "Max retries exceeded"}
    
    # Test URLs (some may fail intentionally)
    urls = [
        'https://httpbin.org/get?id=1',
        'https://httpbin.org/status/500',  # Will return 500 error
        'https://httpbin.org/delay/5',
        'https://httpbin.org/get?id=2',
        'https://httpbin.org/status/200'
    ]
    semaphore = asyncio.Semaphore(2)  # Limit to 2 concurrent requests
    # Create a session for making requests
    # Create tasks for all URLs
    async with aiohttp.ClientSession() as session:
        tasks = [
            asyncio.create_task(fetch_with_retry(session, semaphore, url))
            for url in urls
        ]
        results = await asyncio.gather(*tasks,return_exceptions=True)
        return results

async def main():
    print("Advanced Scraper Example")
    results = await advanced_web_scraper()
    successful = sum(1 for r in results if not isinstance(r, Exception) and "error" not in r)
    for result in results:
        if 'error' not in result:
            print(result['url'])
        else:
            print(f"Failed: {result['url']} with error {result['error']}")
    print(f"Advanced scraper: {successful}/{len(results)} successful\n")
   
# Run the examples
if __name__ == "__main__":
    # Run the main function
    asyncio.run(main())