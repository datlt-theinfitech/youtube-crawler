import logging
from collections.abc import Iterable
from typing import TypedDict
import uuid
from salesnext_crawler.events import CrawlEvent, DataEvent, Event
from scrapy import Request
from scrapy.http.response.html import HtmlResponse
from rikunabi_crawler.schema.v1.rikunabi_recruit import Recruit
from rikunabi_crawler.schema.v1.rikunabi_company import Company
import re
import json

def parse_recruit_detail(
    event: CrawlEvent[None, Event, HtmlResponse],
    response: HtmlResponse,
) -> Iterable[Event]:
    
    script = response.xpath('//script[@id="__NEXT_DATA__"]/text()').get()
    script = json.loads(script)
    recruit = script["props"]["pageProps"]["data"]["jobData"]
    
    job = Recruit(
    source_job_url = response.url,
    job_id = recruit.get("indeedJobKey"),
    job_is_new_arrival = recruit.get("IsNewArrival", False),
    job_employment_type = recruit.get("recruitmentForm", None),
    job_permanent_employment_type = recruit.get("permanentEmploymentType", []),
    job_position_count = recruit.get("positionCount", None),
    job_title = recruit.get("title", None),
    job_sub_title = recruit.get("subTitle", None),
    job_description = recruit.get("jobDescriptionContent", None),
    job_requirement = recruit.get("qualificationContent", None),
    job_address = recruit.get("officeAddress", None),
    job_commute_info = recruit.get("commuteInfo", None),
    job_office_name = recruit.get("officeName", None),
    job_working_location = recruit.get("summaryWorkLocation", None),
    job_summary_salary = recruit.get("summarySalary", None),
    job_tags = recruit.get("preferenceTag", []),
    job_business_content = recruit.get("jobOverview", None),
    job_published_at = recruit.get("datePublished", None),
    job_company_name = recruit.get("companyName", None),
    job_salary = recruit.get("baseSalary", None),
    job_working_style = recruit.get("workStyle", None),
    job_working_hour = recruit.get("workHours", None),
    job_holiday = recruit.get("holidays", None),
    job_trial_period = recruit.get("probationaryPeriod", None),
    job_welfare_insurance = recruit.get("welfareInsurance", None),
    job_welfare_benefit = recruit.get("welfareBenefit", None),
    job_working_environment = recruit.get("workEnvironment", None),
    job_business_detail = recruit.get("businessDetail", None),
    job_company_hp_url = recruit.get("corporateWebsite", None),
    job_apply_info = recruit.get("applyInfo", None),
    
    )
    salary = script.get("props", {}).get("pageProps", {}).get("data", {}).get("lettice", {}).get("letticeLogBase").get("baseSalary", {})
    if salary:
        job.job_max_salary = salary.get("max", None)
        job.job_min_salary = salary.get("min", None)
        job.job_salary_unit = salary.get("code", None)
    
    
    namespace = uuid.NAMESPACE_DNS
    company = Company()
    company.company_name = recruit.get("employerName", None)
    company.company_id = str(uuid.uuid5(namespace, company.company_name))    
    company.company_phone_number = recruit.get("phoneNumber", None) 
    company.company_address =  recruit.get("employerAddress", None)
    company.company_hp_url = recruit.get("corporateWebsite", None) 
    company.company_representative = recruit.get("ceoName", None)
    company.company_business_detail = recruit.get("businessDetails", None)
    company.company_industry = event.metadata["industries"]
    
    job.job_company_id = company.company_id 

    yield DataEvent("company", company)
    yield DataEvent("recruit", job)
    
    
     
    
    
    
    
    
