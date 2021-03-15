import scrapy

from scrapy.loader import ItemLoader

from ..items import HsbcItem
from itemloaders.processors import TakeFirst


class HsbcSpider(scrapy.Spider):
	name = 'hsbc'
	start_urls = ['https://www.hsbc.com/news-and-media/media-releases?page=1&take=20']

	def parse(self, response):
		post_links = response.xpath('//table[@class="table table--one-col-mobile"]//a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@class="pagination__next hidden-xs"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="sublayout article-sublayout "]//p//text()[normalize-space() and not(ancestor::p[contains(text(), "+44 (0) 20 7991 9813")] | ancestor::p[@class="disclaimer__content"] | ancestor::p[@class="disclaimer__header"])]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//p[@class="link-to-author-page__date"]/text()').get()

		item = ItemLoader(item=HsbcItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
