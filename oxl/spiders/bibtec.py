# -*- coding: utf-8 -*-
import time
import scrapy
import urllib

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class BibtecSpider(CrawlSpider):
    name = "bibtec"
    allowed_domains = ["dblp.uni-trier.de"]
    start_urls = [
        'https://dblp.uni-trier.de/db/journals/publ/'
    ]

    rules = {
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//*[@id="main"]/ul/li/a'))),
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//li[@class="export drop-down"]/div[@class="body"]/ul/li[last()]'))),
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//*[@id="main"]/ul//li[2]/div[2]/ul[1]/li[1]/a'))),
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//*[@id="main"]/p/a')), 
            callback="parse_item", 
            follow=False)
    }

    def parse_item(self, response):
        time.sleep(5)
        url = response.url+""
        if (url.endswith(".bib")):
            print('Bibtec URL.. ' + url) #link de descarga
            filename = url.rsplit('/',1)[1]
            print(filename)
            urllib.urlretrieve (url, filename) #descarga
        

        #//*[@id="main"]/p/a                                -- bibtec juntos
        #//*[@id="main"]/ul//li[2]/div[2]/ul[1]/li[1]/a     -- bibtec separados