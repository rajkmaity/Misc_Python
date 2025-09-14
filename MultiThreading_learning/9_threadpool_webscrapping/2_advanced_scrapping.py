from utils import *

def scrape_urls_advanced(urls: List[str], max_workers: int = 5, timeout: int = 10) -> List[Dict[str, any]]:
    """
    Advanced web scraping using ThreadPoolExecutor with submit() and as_completed()
    
    Args:
        urls: List of URLs to scrape
        max_workers: Maximum number of concurrent threads
        timeout: Request timeout for each URL
    
    Returns:
        List of results for each URL
    """
    print(f"Starting advanced scraping with {max_workers} workers...")
    start_time = time.time()
    results = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks and get future objects
        future_to_url = { executor.submit(fetch_url, url, timeout): url
                         for url in urls}
        
        # Process results as they complete
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                result = future.result()
                results.append(result)
                print(f"Completed {len(results)}/{len(urls)} URLs")
            except Exception as e:
                print(f"Exception occurred for {url}: {e}")
                results.append({
                    'url': url,
                    'status': None,
                    'content_length': 0,
                    'response_time': 0,
                    'success': False,
                    'error': str(e)
                })
    
    total_time = time.time() - start_time
    print(f"Advanced scraping completed in {total_time:.2f} seconds")
    return results

if __name__ == "__main__":
    
    # Advanced scraping with submit() and as_completed()
    print("Advanced approach using submit() and as_completed():")
    results= scrape_urls_advanced(urls, max_workers=3, timeout=5)
    process_results(results)