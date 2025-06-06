from collections.abc import Iterable
from salesnext_crawler.crawler import ScrapyCrawler
from salesnext_crawler.events import DataEvent, Event
from youtube_crawler.parser.parse_channel_list import parse_channel_list
from youtube_crawler.parser.parse_channel_detail import parse_channel_detail
from playwright.sync_api import sync_playwright

class YoutubeCrawler(ScrapyCrawler):
    def __init__(self):
        print("Hello World from YoutubeCrawler!")
        self.channels = []
        
        # Get channel list and visit them with Playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            
            # Get list of channels to crawl
            channel_urls = parse_channel_list()
            
            # Parse details for each channel
            for channel_url in channel_urls:
                print(f"Visiting channel: {channel_url}")
                channel_detail = parse_channel_detail(page, channel_url)
                self.channels.append(channel_detail)
            
            browser.close()

    def start(self) -> Iterable[Event]:
        print("Starting YoutubeCrawler...")
        
        # Yield stored channel data
        for channel in self.channels:
            yield DataEvent("channel", channel)

