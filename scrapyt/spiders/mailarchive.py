import scrapy
from typing import Iterable
from bs4 import BeautifulSoup
from scrapy.http import Request
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

class MailarchiveSpider(scrapy.Spider):
    name = "mailarchive"
    allowed_domains = ["mailarchive.ietf.org"]

    # 選定的郵件列表名稱
    listname = 'sframe'

    start_urls = [
        "https://mailarchive.ietf.org/arch/browse/%s" % listname,
    ]

    def parse(self, response):
        # self.logger.debug(f'Full URL: {response.url}')
        # print(response.url.split('/')[4]) # browse

        # catch all the urls toward the email messages in the WG mailbox(email list)
        # 在WG信箱(email list)擷取通往所有email訊息頁面的連結
        # yield from self.scrape_urls(response)
        
        # the regular expression that can catch the massages
        # 欲抓取email訊息的正規表達式
        pattern = 'msg\/%s\/[A-Za-z0-9_-]{,27}\/' % MailarchiveSpider.listname

        for a in response.css("a.msg-detail::attr(href)").re(pattern):
            # print('catched link:', a)
            # print(response.url.replace(f'browse/{MailarchiveSpider.listname}/', a))
            yield scrapy.Request(response.url.replace(f'browse/{MailarchiveSpider.listname}/', a), callback=self.scrape_email)
        
        
    

    def scrape_urls(self, response):
        # the regular expression that can catch the massages
        # 欲抓取email訊息的正規表達式
        pattern = 'msg\/%s\/[A-Za-z0-9_-]{,27}\/' % MailarchiveSpider.listname

        all_urls = response.css("a.msg-detail::attr(href)").re(pattern)

        for link in all_urls:
            self.logger.debug(f"catched url: {link}")

        return all_urls

        
    # 抓取每個email頁面的function
    def scrape_email(self, response):
        # 解析工具
        def extract_with_css(query):
            return response.css(query).getall()

        subjects = extract_with_css("div#msg-body h3::text")
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