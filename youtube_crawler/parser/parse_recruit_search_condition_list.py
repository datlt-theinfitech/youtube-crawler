from collections.abc import Iterable
from typing import TypedDict

from salesnext_crawler.events import CrawlEvent, Event
from scrapy import FormRequest, Request
from scrapy.http.response.html import HtmlResponse

from rikunabi_crawler.parser.parse_recruit_list import parse_recruit_list


class ParseRecruitSearchConditionListMetadata(TypedDict):
    condition: str
    crawled_recruit_ids: set[str]
    daily: bool


def parse_recruit_search_condition_list(
    event: CrawlEvent[None, Event, HtmlResponse],
    response: HtmlResponse,
) -> Iterable[Event]:
    csrf_token = response.xpath("//meta[@name='csrfToken']/@content").get()
    metadata = event.metadata
    categories = response.xpath('//div[@class="styles_module___bI19"]//@href').getall()
    industry_text = response.xpath('//div[@class="styles_module___bI19"]//text()').getall()
  
    for category, industry in zip(categories, industry_text):
       
        yield CrawlEvent(
            request = Request(f'https://next.rikunabi.com{category}',
                            headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0",
    "Accept-Language": "ja,en-US;q=0.9,en;q=0.8",
    "Referer": "https://next.rikunabi.com/",
    "csrf-token": csrf_token,
},),
            metadata= {"industries": industry,
                       'crawled_company_ids': event.metadata['crawled_company_ids'],
                       'crawled_recruit_ids': event.metadata["crawled_recruit_ids"],
                       "token": csrf_token},
            callback= parse_recruit_list,
            
                
            )