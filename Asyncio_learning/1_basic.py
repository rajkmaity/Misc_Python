import asyncio
import time

'''
Basic structure of an async function
async def fun():
    do something

async def main():
    await fun()

if __name__ == "__main__":
    asyncio.run(main())
'''


async def basic_async_example():
    """Basic async function example"""
    print("Starting async operation...")
    await asyncio.sleep(1)  # Simulate async operation
    print()
    return "Async operation completed!"

async def main():
    """Main function demonstrating all concepts"""
    
    print("=== 1. Basic Async Example ===")
    ## basis async example: awaiting a simple async function
    result = await basic_async_example()
    print(f"Result: {result}\n")
    
if __name__ == "__main__":
    # Run the main function
    asyncio.run(main())