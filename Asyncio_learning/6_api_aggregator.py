import asyncio
import aiohttp
import time
from typing import List, Dict, Any

async def api_data_aggregator():
    async def fetch_api_data(session: aiohttp.ClientSession,
                            semaphore: asyncio.Semaphore,
                            endpoint: str,
                            params: dict = None) -> Dict[str, Any]:
        """Fetch data from API endpoint"""
        async with semaphore:
            try:
                async with session.get(endpoint, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {"endpoint": endpoint, "data": data, "success": True}
                    else:
                        return {"endpoint": endpoint, "error": f"HTTP {response.status}", "success": False}
            except Exception as e:
                return {"endpoint": endpoint, "error": str(e), "success": False}
    # Simulate different API endpoints
    endpoints = [
        'https://httpbin.org/json',
        'https://httpbin.org/uuid',
        'https://httpbin.org/get?category=users',
        'https://httpbin.org/get?category=posts',
        'https://httpbin.org/get?category=comments'
    ]
    semaphore = asyncio.Semaphore(3)  # Max 3 concurrent API calls
    async with aiohttp.ClientSession() as session:
        # Create tasks for all endpoints
        tasks = [
            asyncio.create_task(fetch_api_data(session, semaphore, endpoint))
            for endpoint in endpoints
        ]
        # Wait for all tasks with timeout
        try:
            results = await asyncio.wait_for(asyncio.gather(*tasks),timeout=10.0)
            # Process results
            successful = [r for r in results if r.get("success")]
            failed = [r for r in results if not r.get("success")]
            return {"successful": len(successful),"failed": len(failed),"results": results}
        except asyncio.TimeoutError:
            return {"error": "Operation timed out"}
# 10. MAIN EXECUTION EXAMPLES
async def main():
    print("API Data Aggregator Example")
    results = await api_data_aggregator()
    print(f"API aggregator: {results['successful']} successful, {results['failed']} failed\n")
# Run the examples
if __name__ == "__main__":
    asyncio.run(main())
    