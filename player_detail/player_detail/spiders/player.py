# -*- coding: utf-8 -*-
import scrapy


class MyplayerSpider(scrapy.Spider):
	name = "player"
	start_urls = ['http://www.espncricinfo.com/ci/content/site/cricket_squads_teams/index.html']

	def parse(self, response):
		page = response.url.split("/")[-2]
		filename = 'page1.html'
		first_page=response.css("table.teamList tr td")[1]
		one=first_page.css('a::attr(href)').extract_first()
		next_page = first_page.css('a::attr(href)').extract_first()
		
		if next_page is not None:
			next_page = response.urljoin(next_page)
			yield response.follow(next_page, callback=self.parse_country)
		with open(filename, 'wb') as f:
            		f.write(response.body)
	def parse_country(self, response):
		filename = 'page2.html'
		
		with open(filename, 'wb') as f:
            		f.write(response.body)

