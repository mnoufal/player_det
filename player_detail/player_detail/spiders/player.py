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
	def parse_country(self, response):
		filename = 'page2.html'
		second_page=response.css("div.global-nav-container")[0]
		second_page1=second_page.css("li.sub")[2]
		next_page = second_page1.css('a::attr(href)').extract_first()

		if next_page is not None:
			next_page = response.urljoin(next_page)
			yield response.follow(next_page, callback=self.parse_players)
		
	def parse_players(self, response):
		filename = 'page3.html'
		third_page=response.css("table.playersTable tr td")[0]
		
		next_page = third_page.css('a::attr(href)').extract_first()
		
		if next_page is not None:
			next_page = response.urljoin(next_page)
			yield response.follow(next_page, callback=self.parse_details)
		
	def parse_details(self, response):
		filename = 'final_page.html'

		with open(filename, 'wb') as f:
            		f.write(response.body)


