import re

import scrapy

from scrapy.loader import ItemLoader

from ..items import BancaprofiloitItem
from itemloaders.processors import TakeFirst


class BancaprofiloitSpider(scrapy.Spider):
	name = 'bancaprofiloit'
	start_urls = ['https://www.bancaprofilo.it/interna.php?numpag=8']

	def parse(self, response):
		post_links = response.xpath('//tr[contains(@class, "evento ")]/@onclick').getall()
		for post in post_links:
			page = re.findall(r"\d+", post)[0]
			url = f'https://www.bancaprofilo.it/interna.php?numpag={page}'
			yield response.follow(url, self.parse_post)


	def parse_post(self, response):
		title = response.xpath('//h1/text()').getall()
		title = [p.strip() for p in title]
		title = ' '.join(title).strip()
		description = response.xpath('//td[@class="testoPagina"]//text()[normalize-space() and not(ancestor::h1)]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		try:
			date = re.findall(r'\d{1,2}\s\D+\s\d{4}', description)[0]
		except:
			print(response)
			date = ''

		item = ItemLoader(item=BancaprofiloitItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
