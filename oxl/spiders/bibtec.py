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
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//*[@id="main"]/ul/li/a'))),                         #xpaths de los menus
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//*[@id="main"]/ul//li[2]/div[2]/ul[1]/li[1]/a')),   #xpaths de los enlace a las bibtec
            callback="parse_item", 
            follow=False)
        
    }

    def parse_item(self, response):
        url = str(response.xpath('//*[@id="main"]/p/a').extract())  #xpath del enlace a descarga
        url = url.split(' ')[1]
        url = url.split('"')[1]
        
        if (url.endswith(".bib")):
            print('Bibtec URL.. ' + url) #link de descarga
            filename = url.rsplit('/',1)[1]
            print(filename)
            urllib.urlretrieve (url, filename) #descarga
        
        time.sleep(5)