import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from typing import List, Dict, Optional


urls = [
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/2",
        "https://httpbin.org/status/200",
        "https://httpbin.org/status/404",  # This will fail
        "https://httpbin.org/json",
        "https://httpbin.org/html",
        "https://httpbin.org/xml",
        "https://httpbin.org/user-agent",
        "https://httpbin.org/headers",
        "https://httpbin.org/ip"
    ]

def fetch_url(url: str, timeout: int = 10) -> Dict[str, any]:
    """
    Fetch a single URL and return result information
    
    Args:
        url: URL to fetch
        timeout: Request timeout in seconds
    
    Returns:
        Dictionary containing URL, status, content length, and response time
    """
    start_time = time.time()
    try:
        print(f"Fetching: {url}")
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()  # Raise exception for bad status codes
        
        result = {
            'url': url,
            'status': response.status_code,
            'content_length': len(response.content),
            'response_time': time.time() - start_time,
            'success': True,
            'error': None
        }
        print(f"Successfully fetched {url} ({response.status_code})")
        return result
        
    except requests.exceptions.RequestException as e:
        result = {
            'url': url,
            'status': None,
            'content_length': 0,
            'response_time': time.time() - start_time,
            'success': False,
            'error': str(e)
        }
        print(f"Failed to fetch {url}: {e}")
        return result


def process_results(results: List[Dict[str, any]]) -> None:
    """
    Process and display scraping results
    
    Args:
        results: List of scraping results
    """
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    print(f"\n=== SCRAPING RESULTS ===")
    print(f"Total URLs: {len(results)}")
    print(f"Successful: {len(successful)}")
    print(f"Failed: {len(failed)}")
    
    if successful:
        avg_response_time = sum(r['response_time'] for r in successful) / len(successful)
        total_content = sum(r['content_length'] for r in successful)
        print(f"Average response time: {avg_response_time:.2f}s")
        print(f"Total content downloaded: {total_content:,} bytes")
    
    if failed:
        print(f"\nFailed URLs:")
        for result in failed:
            print(f"  - {result['url']}: {result['error']}")



def scrape_with_retry(url: str, max_retries: int = 3, delay: float = 1.0) -> Dict[str, any]:
    """
    Fetch URL with retry logic
    
    Args:
        url: URL to fetch
        max_retries: Maximum number of retry attempts
        delay: Delay between retries in seconds
    
    Returns:
        Result dictionary
    """
    for attempt in range(max_retries + 1):
        try:
            if attempt > 0:
                print(f"Retry {attempt} for {url}")
                time.sleep(delay * attempt)  # Exponential backoff
            
            return fetch_url(url)
            
        except Exception as e:
            if attempt == max_retries:
                return {
                    'url': url,
                    'status': None,
                    'content_length': 0,
                    'response_time': 0,
                    'success': False,
                    'error': f"Failed after {max_retries} retries: {str(e)}"
                }
            continue

def scrape_with_custom_headers(url: str, headers: Dict[str, str] = None) -> Dict[str, any]:
    """
    Fetch URL with custom headers
    
    Args:
        url: URL to fetch
        headers: Custom headers to send
    
    Returns:
        Result dictionary
    """
    start_time = time.time()
    
    if headers is None:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        return {
            'url': url,
            'status': response.status_code,
            'content_length': len(response.content),
            'response_time': time.time() - start_time,
            'success': True,
            'error': None,
            'headers': dict(response.headers)
        }
        
    except requests.exceptions.RequestException as e:
        return {
            'url': url,
            'status': None,
            'content_length': 0,
            'response_time': time.time() - start_time,
            'success': False,
            'error': str(e),
            'headers': None
        }

def batch_scrape_with_rate_limiting(urls: List[str], max_workers: int = 5, 
                                   requests_per_second: float = 2.0) -> List[Dict[str, any]]:
    """
    Scrape URLs with rate limiting to be respectful to servers
    
    Args:
        urls: List of URLs to scrape
        max_workers: Maximum number of concurrent threads
        requests_per_second: Maximum requests per second
    
    Returns:
        List of results
    """
    import threading
    from queue import Queue
    
    # Rate limiting using a semaphore and timer
    request_times = Queue()
    rate_limit_lock = threading.Lock()
    
    def rate_limited_fetch(url: str) -> Dict[str, any]:
        with rate_limit_lock:
            now = time.time()
            
            # Remove old timestamps
            while not request_times.empty():
                if now - request_times.queue[0] > 1.0:  # Remove timestamps older than 1 second
                    request_times.get()
                else:
                    break
            
            # Check if we need to wait
            if request_times.qsize() >= requests_per_second:
                sleep_time = 1.0 / requests_per_second
                time.sleep(sleep_time)
            
            request_times.put(now)
        
        return fetch_url(url)
    
    print(f"Starting rate-limited scraping ({requests_per_second} req/s) with {max_workers} workers...")
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(rate_limited_fetch, urls))
    
    total_time = time.time() - start_time
    print(f"Rate-limited scraping completed in {total_time:.2f} seconds")
    return results