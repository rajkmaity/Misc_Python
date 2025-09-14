from utils import *

def scrape_urls_with_progress(urls: List[str], max_workers: int = 5) -> List[Dict[str, any]]:
    """
    Web scraping with real-time progress updates
    
    Args:
        urls: List of URLs to scrape
        max_workers: Maximum number of concurrent threads
    
    Returns:
        List of results for each URL
    """
    print(f"Starting scraping with progress tracking using {max_workers} workers...")
    start_time = time.time()
    results = []
    completed = 0
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_url = {
            executor.submit(fetch_url, url): url 
            for url in urls
        }
        
        # Process results as they complete with progress tracking
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                result = future.result()
                results.append(result)
                completed += 1
                
                # Show progress
                progress = (completed / len(urls)) * 100
                print(f"Progress: {progress:.1f}% ({completed}/{len(urls)}) - Latest: {url}")
                
            except Exception as e:
                print(f"Exception for {url}: {e}")
                results.append({
                    'url': url,
                    'status': None,
                    'content_length': 0,
                    'response_time': 0,
                    'success': False,
                    'error': str(e)
                })
                completed += 1
    
    total_time = time.time() - start_time
    print(f"Scraping with progress completed in {total_time:.2f} seconds")
    return results



# Example usage with different approaches
if __name__ == "__main__":

    print("Scraping with progress tracking:")
    results = scrape_urls_with_progress(urls, max_workers=3)
    process_results(results)
