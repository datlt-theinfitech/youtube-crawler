from typing import List
from playwright.sync_api import sync_playwright
import time

def parse_channel_list_from_recommendation() -> List[str]:
    # Hard coded channel URLs
    channels = [
        "https://www.youtube.com/@F8Official",
        "https://www.youtube.com/@evondev",
        "https://www.youtube.com/@ThangDev"
    ]
    return channels

def parse_channel_list_from_search(search_queries: List[str]) -> List[str]:
    """
    Parse channel URLs from YouTube search results based on multiple search queries using Playwright.
    
    Args:
        search_queries (List[str]): List of search terms to find channels
        
    Returns:
        List[str]: List of channel URLs found from all searches
    """
    channels = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        for search_query in search_queries:
            # Navigate to YouTube search with channel filter
            search_url = f"https://www.youtube.com/results?search_query={search_query}&sp=EgIQAg%253D%253D"
            page.goto(search_url)
            
            # Wait for the results to load
            page.wait_for_selector('ytd-channel-renderer')
            
            # Scroll a few times to load more results
            for _ in range(3):
                page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                time.sleep(1)
            
            # Extract channel URLs
            channel_elements = page.query_selector_all('ytd-channel-renderer a#main-link')
            for element in channel_elements:
                href = element.get_attribute('href')
                if href and '/channel/' in href or '/@' in href:
                    channel_url = f"https://www.youtube.com{href}"
                    if channel_url not in channels:
                        channels.append(channel_url)
            
            # Add a small delay between searches
            time.sleep(2)
        
        browser.close()
    
    return channels 