from typing import TypedDict, Dict, Any
from playwright.sync_api import Page

class ChannelDetail(TypedDict):
    channel_url: str
    channel_name: str
    description: str
    subscriber_count: str
    total_views: str
    join_date: str
    location: str
    links: list[str]
    banner_url: str
    avatar_url: str

def parse_channel_detail(page: Page, channel_url: str) -> ChannelDetail:
    """
    Return hardcoded mock data for YouTube channel details
    """
    return {
        "channel_url": channel_url,
        "channel_name": "Mock Channel Name",
        "description": "This is a mock channel description for testing purposes.",
        "subscriber_count": "1.5M subscribers",
        "total_views": "10,000,000 views",
        "join_date": "Joined Jan 1, 2020",
        "location": "Tokyo, Japan",
        "links": [
            "https://example.com/website",
            "https://example.com/twitter",
            "https://example.com/instagram"
        ],
        "banner_url": "https://example.com/banner.jpg",
        "avatar_url": "https://example.com/avatar.jpg"
    } 