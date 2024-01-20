# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapytItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    mail_title   = scrapy.Field()
    mail_author  = scrapy.Field()
    mail_mail = scrapy.Field() 
    mail_date    = scrapy.Field()
    mail_content = scrapy.Field()
    