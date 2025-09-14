import asyncio
import aiohttp
import time

url = 'https://httpbin.org/get'

async def basic_aiohttp_session():
    """Basic aiohttp session usage
    
    - Create a ClientSession with aiohttp and async
    - Make a GET request to a URL as response
    - Await the response and return the JSON data
    
    All the call needs to be in an async function
    """
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            print(f"Response: {data}")
            return "data fetched"
        
async def main():
    """Main function demonstrating all concepts"""
    
    print("Basic Session Example")
    data = await basic_aiohttp_session()
    print(f"Fetched data: {data}\n")


if __name__ == "__main__":
    # Run the main function
    asyncio.run(main())