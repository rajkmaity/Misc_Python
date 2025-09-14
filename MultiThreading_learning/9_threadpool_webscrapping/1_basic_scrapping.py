from utils import *



def scrape_urls_basic(urls: List[str], max_workers: int = 5) -> List[Dict[str, any]]:
    """
    Basic web scraping using ThreadPoolExecutor with map()
    
    Args:
        urls: List of URLs to scrape
        max_workers: Maximum number of concurrent threads
    
    Returns:
        List of results for each URL
    """
    print(f"Starting basic scraping with {max_workers} workers...")
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # map() maintains order and waits for all to complete
        results = list(executor.map(fetch_url, urls))
    
    total_time = time.time() - start_time
    print(f"Basic scraping completed in {total_time:.2f} seconds")
    return results


if __name__ == "__main__":
    # Sample URLs to scrape (replace with real URLs)
    print("=== COMPARISON OF DIFFERENT APPROACHES ===\n")
    
    # Basic scraping with map()
    print("Basic approach using map():")
    results = scrape_urls_basic(urls, max_workers=3)
    process_results(results)