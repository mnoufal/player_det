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
		third_page=response.css("table.playersTable tr td")[5]
		
		next_page = third_page.css('a::attr(href)').extract_first()
		
		if next_page is not None:
			next_page = response.urljoin(next_page)
			yield response.follow(next_page, callback=self.parse_details)

	def parse_details(self, response):
		filename = 'final_page.html'
		final_page=response.css("p.ciPlayerinformationtxt")
		team_list=[]
		for i in final_page[3].css('span::text').extract():
			team_list.append(i.strip(','))
		next_page = response.css('img::attr(src)').extract_first()
		next_page = response.urljoin(next_page)
		final_page1=response.css('div.pnl490M')[0]
		item=[final_page[0].css('span::text').extract_first(),final_page[1].css('span::text').extract_first(),final_page[2].css('span::text').extract_first(),team_list,final_page[4].css('span::text').extract_first(),final_page[5].css('span::text').extract_first(),final_page[6].css('span::text').extract_first(),final_page1.css('h1::text').extract_first(),final_page1.css('h3.PlayersSearchLink b::text').extract_first(),response.url]
		req = scrapy.Request(next_page, callback=self.write_the_data)
		req.meta['item']=item
		yield req

	def write_the_data(self, response):
		page = response.url
		item = response.meta['item']
		item.append(page)
		yield {
			1: item[7],
			2: item[8],
			3: item[0],
			4: item[1],
			5: item[2],
			6: item[3],
			7: item[4],
			8: item[5],
			9: item[6],
			10: page,
			11: '',
			'url': item[9]

			}
