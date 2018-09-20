# -*- coding: utf-8 -*-
import time
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
class BibtecSpider(CrawlSpider):
    name = "bibtec"
    allowed_domains = ["dblp.uni-trier.de"]
    start_urls = [
        'https://dblp.uni-trier.de/db/journals/publ/'
    ]

    rules = {
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//*[@id="main"]/ul/li/a')), callback="parse_item", follow=True),
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//li[@class="export drop-down"]/div[@class="body"]/ul/li[last()]')), callback="parse_item", follow=True)
    }

    def parse_item(self, response):
        time.sleep(1)
        print('Processing..' + response.url)