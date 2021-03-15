import scrapy


class HsbcItem(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
    date = scrapy.Field()
