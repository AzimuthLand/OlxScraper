# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from olx.items import OlxItem


class LandSpider(CrawlSpider):
    name = "Lands"
    allowed_domains = ["www.olx.ua"]
    start_urls = [
        'https://www.olx.ua/d/uk/nedvizhimost/zemlya/arenda-zemli/',
        'https://www.olx.ua/d/uk/nedvizhimost/zemlya/prodazha-zemli/'
    ]

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "uk-UA,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0",
    }

    rules = (
        Rule(LinkExtractor(allow=(), restrict_css=('.pageNextPrev',)),
             callback="parse_item",
             follow=False),)

    def parse_item(self, response):
        item_links = response.css('.large > .detailsLink::attr(href)').extract()
        for a in item_links:
            yield scrapy.Request(a, callback=self.parse_detail_page)

    def parse_detail_page(self, response):
        title = response.css('h1::text').extract()[0].strip()
        price = response.css('.pricelabel > strong::text').extract()[0]

        item = OlxItem()
        item['title'] = title
        item['price'] = price
        item['url'] = response.url
        yield item
