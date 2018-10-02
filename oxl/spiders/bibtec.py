# -*- coding: utf-8 -*-
import time
import scrapy
import urllib
import urllib2
import bibtexparser
import re

from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.linkextractors import LinkExtractor
from pybtex.database import parse_string

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
        try:
            print("\nSe intenta parsear "+response.url)
            hxs = HtmlXPathSelector(response)
            vols = hxs.select('//*[@id="main"]/ul')
            journalurl = (str)(response.xpath('//*[@id="breadcrumbs"]/ul/li/span[3]/a').extract())
            journalurl = journalurl.split('"')[1]
            journal = (str)(response.xpath('//*[@id="breadcrumbs"]/ul/li/span[3]/a/span').extract())
            journal = journal.split(">")[1]
            journal = journal.split("<")[0]
            print("El journal es "+journal)
            print("El url del journal es "+journalurl)
            n = len(vols)
            for i in range(1,n+1):
                paths = '//*[@id="main"]/ul['+str(i)+']/li'
                print("Se parsea el bloque "+paths)
                pubs = hxs.select(paths)
                o  = len(pubs)
                for j in range(1, o+1):
                    print("Se parsea el bloque "+'//*[@id="main"]/ul['+str(i)+']/li['+str(j)+']')
                    titulo = (str)(response.xpath('//*[@id="main"]/ul['+str(i)+']/li['+str(j)+']/div[2]/span[last()-1]').extract())
                    titulo = titulo.split(">")[1]
                    titulo = titulo.split("<")[0]
                    publicacionurl = (str)(response.xpath('//*[@id="main"]/ul['+str(i)+']/li['+str(j)+']/nav/ul/li[4]/div[2]/ul[2]/li/small').extract())
                    publicacionurl = publicacionurl.split(">")[1]
                    publicacionurl = publicacionurl.split("<")[0]
                    print("El título es "+titulo)
                    print("El url del artículo es "+publicacionurl)
                    pathbibtec = '//*[@id="main"]/ul['+str(i)+']/li['+str(j)+']/nav/ul/li[2]/div/ul/li[1]/a'
                    pathauthors = '//*[@id="main"]/ul['+str(i)+']/li['+str(j)+']/div[2]/span/a'
                    urlbib = (str)(response.xpath(pathbibtec).extract())
                    urlbib = urlbib.split('"')[1]

                    try:
                        s = (str)(response.xpath(pathauthors).extract()) #Obtiene las url de los autores
                        s2 = s.split("href")
                        p=len(s2)
                        authors = []
                        for k in range(0,p):
                            s3 = s2[k]
                            if '"' in s3:
                                s3 = s3.split('"')[1]
                                authors.append(s3)
                        print ("Autores")
                        for k in range(0, len(authors)):
                            print(authors[k])
                    except:
                        print ("No hay autores")

                    try:
                        print("La URL del bibtec es: "+urlbib)
                        
                        f = urllib.urlopen(urlbib) #Abre la URL del bibtec
                        s = f.read()
                        s = s.split('<pre class="verbatim select-on-click">')[1]
                        s = s.split('</pre>')[0]
                        s = s.replace("\n","")
                        s = re.sub("\s\s+", " ", s)

                        bib_data = parse_string(s,"bibtex")
                        for entry in bib_data.entries.values():
                            #print entry.key
                            #print entry.fields.keys()
                            for value in entry.fields.keys():
                                print value ,"=", bib_data.entries[entry.key].fields[value]

                    except:
                        print("No se pudo parsear el bibtec")
                    
                    print ("Publicación parseada con exito")
                print ("Bloque parseado con exito")
            print ("Página parseada con exito")

        except:
            print ("No se pudo parsear "+response.url)
