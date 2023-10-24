import scrapy
from typing import Iterable
from bs4 import BeautifulSoup
from scrapy.http import Request
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

class MailarchiveSpider(scrapy.Spider):
    name = "mailarchive"
    allowed_domains = ["www.mailarchive.ietf.org"]

    # 選定的郵件列表名稱
    listname = 'sframe'

    start_urls = [
        "https://mailarchive.ietf.org/arch/browse/%s" % listname,
    ]

    # rules = [
    #     Rule(LinkExtractor(allow=('msg\/%s\/[A-Za-z0-9_-]{,27}\/$')), callback='parse_email', follow=True)
    # ]

    # def _save_as_file(self, response, format='txt'):
    #     page = response.url.split('/')
    #     filename = f"page-{page}.html"
    #     file = open(f'{filename}.{format}','w+')

    #     file.write(response.body)``

    def parse(self, response):
        self.logger.info(f'Full URL: {response.url}')
        
        # 欲抓取email訊息的正規表達式
        pattern = 'msg\/%s\/[A-Za-z0-9_-]{,27}\/' % MailarchiveSpider.listname

        for a in response.css("a.msg-detail::attr(href)").re(pattern):
            print('catched link:', a)
            # print(response.url.replace(f'browse/{MailarchiveSpider.listname}/', a))
            yield scrapy.Request(response.url.replace(f'browse/{MailarchiveSpider.listname}/', a))
        
        
        yield from self.scrape_email(response)
        
    

    def scrape_urls(self, response):
        pattern = 'msg\/%s\/[A-Za-z0-9_-]{,27}\/' % MailarchiveSpider.listname
        
    # 抓取每個email頁面的function
    def scrape_email(self, response):
        # 解析工具
        def extract_with_css(query):
            return response.css(query).getall()

        subjects = extract_with_css("div#msg-body h3")
        authors  = extract_with_css("span#msg-from::text")
        dates    = extract_with_css("span#msg-date::text")
        contents = extract_with_css(".wordwrap::text")

        print("Subject:", subjects)
        print("From   :", authors)
        print("Date   :", dates)
        print("Content:", contents)


        for (title, author, date, msg) in zip(subjects, authors, dates, contents):

            ScrapytItem = {
                "mail_title"  : title if title else None,
                "mail_author" : author if author else None,
                "mail_date"   : date if date else None,
                "mail_content": msg if msg else None,
            }
        
            yield ScrapytItem