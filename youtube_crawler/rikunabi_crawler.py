from collections.abc import Iterable
from enum import Enum
from urllib.parse import urlencode

import pyarrow as pa
from salesnext_crawler.crawler import ScrapyCrawler
from scrapy import FormRequest
from salesnext_crawler.events import CrawlEvent, Event, SitemapEvent
from scrapy import Request

from rikunabi_crawler.parser.parse_recruit_search_condition_list import (
    ParseRecruitSearchConditionListMetadata,
    parse_recruit_search_condition_list,
)


class CrawlType(str, Enum):
    RECRUIT_LIST = "RECRUIT_LIST"
    COMPANY_LIST = "COMPANY_LIST"
    SITEMAP = "SITEMAP"

class RikunabiCrawler(ScrapyCrawler):
    def __init__(
        self,
       
        daily: bool = False,
    ):
        self.daily = daily

    def start(self) -> Iterable[Event]:
        crawled_company_ids = set()
        crawled_recruit_ids = set()
      
        if self.daily:
            company_table: pa.Table = self.readers["rikunabi_company_table"].read()
            crawled_company_ids = set(company_table.select(["company_id"]).drop_null().to_pydict()["company_id"])

            recruit_table: pa.Table = self.readers["rikunabi_recruit_table"].read()
            crawled_recruit_ids = set(recruit_table.select(["job_id"]).drop_null().to_pydict()["job_id"])

           
            
        yield CrawlEvent(
            request=Request("https://next.rikunabi.com/sitemap", method="POST",
                            headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0",
"Accept-Language": "ja,en-US;q=0.9,en;q=0.8",
"Referer": "https://next.rikunabi.com/",
},
                          
),
            metadata= {'crawled_recruit_ids': crawled_recruit_ids, 
                       'crawled_company_ids': crawled_company_ids}, 
            callback=parse_recruit_search_condition_list,
        )
        