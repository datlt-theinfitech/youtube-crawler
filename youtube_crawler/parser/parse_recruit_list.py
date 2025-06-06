import re
from collections.abc import Iterable
from typing import TypedDict
from urllib.parse import urljoin
from salesnext_crawler.events import CrawlEvent, Event
from scrapy import Request
from scrapy.http.response.html import HtmlResponse
from rikunabi_crawler.parser.parse_recruit_detail import parse_recruit_detail



def parse_recruit_list(
    event: CrawlEvent[None, Event, HtmlResponse],
    response: HtmlResponse,
) -> Iterable[Event]:
    job_urls = response.xpath("//a[@class='styles_bigCard__pKdMA']/@href").getall()
    print(job_urls)
    next_page = response.xpath("//a[@class='styles_arrowButton__UZns7 styles_next__9KVqV']/@href").get()
    next_page = urljoin(response.url, next_page) if next_page else None
    if next_page:
        yield CrawlEvent(
            request=Request(next_page),
            metadata=event.metadata,
            callback=parse_recruit_list,
        )
    for url in job_urls:
        url = urljoin(response.url, url)
        job_id = url.split("/")[-2]
        if job_id in event.metadata["crawled_recruit_ids"]:
            continue
        yield CrawlEvent(
            request=Request(url,              
                            headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0",
    "Accept-Language": "ja,en-US;q=0.9,en;q=0.8",
    "Referer": "https://next.rikunabi.com/",
    "csrf-token": event.metadata["token"]
},),
            metadata= event.metadata,
            callback=parse_recruit_detail,
        )
    