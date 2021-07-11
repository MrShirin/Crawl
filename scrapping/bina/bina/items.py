# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BinaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    price = scrapy.Field() 
    price_per_m = scrapy.Field()
    description = scrapy.Field()
    kateqoriya = scrapy.Field()
    mertebe = scrapy.Field()
    kupca = scrapy.Field()
    ipoteka = scrapy.Field()
    sahe = scrapy.Field()
    otaq_sayi = scrapy.Field()
