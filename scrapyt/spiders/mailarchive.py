import re
from typing import Iterable
import bs4
import scrapy
from scrapy.http import Request
from scrapy.spiders import Rule, Request
from scrapy.linkextractors import LinkExtractor
import logging

class MailarchiveSpider(scrapy.Spider):
    name = "mailarchive"
    allowed_domains = ["www.mailarchive.ietf.org"]

    # 選定的郵件列表名稱
    listname = 'sframe'

    # 欲抓取email訊息的正規表達式
    pattern = 'msg\/%s\/[A-Za-z0-9_-]{,27}\/' % listname
    # start_urls = [
    #     "https://mailarchive.ietf.org/arch/", 
    #     "https://mailarchive.ietf.org/arch/browse/" + listname,

    # ]

    def start_requests(self) -> Iterable[Request]:
        urls = [
            "https://mailarchive.ietf.org/arch/", 
            "https://mailarchive.ietf.org/arch/browse/%s/" % MailarchiveSpider.listname
        ]

    # def _save_as_file(self, response, format='txt'):
    #     page = response.url.split('/')
    #     filename = f"page-{page}.html"
    #     file = open(f'{filename}.{format}','w+')

    #     file.write(response.body)
    
    

    def parse(self, response):
        for a in response.css("a.msg-detail::attr(href)").re(MailarchiveSpider.pattern):
            print('catched link:', a)
            yield response.follow(a, self.parse_email)
            
                # print("Subject:", self.extract_with_css(response,"h3::text"),
                #       "\nFrom:",    self.extract_with_css(response, "span#msg-from::text"),
                #       "\nDate:" ,   self.extract_with_css(response, "span#msg-date::text"),
                #       "\nContent:", self.extract_with_css(response, "pre.wordwrap::text"))
        
    # 實際解析email頁面的function
    def parse_email(self, response):
        
        # 解析工具
        def extract_with_css(query):
            return response.css(query).get(default="").strip()

        subject = extract_with_css("msg-body + h3::text")
        fromwho = extract_with_css("span#msg-from::text")
        date    = extract_with_css("span#msg-date::text")
        content = extract_with_css(".wordwrap::text")

        print("Subject:", subject)
        print("From   :", fromwho)
        print("Date   :", date)
        print("Content:", content)

        ScrapytItem = {
            "mail_title": subject if subject else "NULL",
            "mail_author":    fromwho if fromwho else "NULL",
            "mail_date":    date if date else "NULL",
            "mail_content": content if content else "NULL",
        }
        
        if ScrapytItem:
            yield ScrapytItem
        
