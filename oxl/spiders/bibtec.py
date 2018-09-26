# -*- coding: utf-8 -*-
import time
import scrapy
import urllib

from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.linkextractors import LinkExtractor

class BibtecSpider(CrawlSpider):
    name = "bibtec"
    allowed_domains = ["dblp.uni-trier.de"]
    start_urls = [
        'https://dblp.uni-trier.de/db/journals/publ/'
    ]

    rules = {
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//*[@id="main"]/ul/li/a')),   #xpaths de los menus
            callback="parse_item", 
            follow=True)
        
    }

    def parse_item(self, response):
        url = (str)(response.url)
        n = len(url.split("/"))
        contiene = "publ" in url
        if (n==7 and url.endswith("index.html")==False and contiene==False):
            hxs = HtmlXPathSelector(response)
            vols = hxs.select('//*[@id="main"]/ul')
            n = len(vols)
            for i in range(1,n+1):
                paths = '//*[@id="main"]/ul['+str(i)+']/li'
                pubs = hxs.select(paths)
                o  = len(pubs)
                for j in range(1, o+1):
                    pathbibtec = '//*[@id="main"]/ul['+str(i)+']/li['+str(j)+']/nav/ul/li[2]/div/ul/li[1]/a'
                    pathauthors = '//*[@id="main"]/ul['+str(i)+']/li['+str(j)+']/div[2]/span/a'
                    urlbib = (str)(response.xpath(pathbibtec).extract())
                    urlbib = urlbib.split('"')[1]
                    f = urllib.urlopen(urlbib)
                    s = f.read()
                    s = s.split('<pre class="verbatim select-on-click">')[1]
                    s = s.split('</pre>')[0]
                    s = s.encode('utf8')
                    print(s)

                    s = (str)(response.xpath(pathauthors).extract())
                    s2 = s.split("href")
                    p=len(s2)
                    authors = []
                    for k in range(0,p):
                        s3 = s2[k]
                        if '"' in s3:
                            s3 = s3.split('"')[1]
                            authors.append(s3)
                    for k in range(0, len(authors)):
                        print(authors[k])

            time.sleep(1)
