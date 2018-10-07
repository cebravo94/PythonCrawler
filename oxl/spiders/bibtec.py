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
    allowed_domains = ["dblp.uni-trier.de","dblp.org"]
    start_urls = [
        'https://dblp.org/pers'
    ]
    dont_filter=True

    rules = {
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//*[@id="browse-person-output"]/div/div/ul/li')),   #xpaths de los menus de personas
            callback="parse_item", 
            follow=True),
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//*[@id="browse-person-output"]/p[1]/a[2]'))) #boton next para personas
        
    }

    def parse_item(self, response):

        url = (str)(response.url)
        try:
            print("\nSe intenta parsear "+response.url)
            hxs = HtmlXPathSelector(response)
            bloques = '//*[@id="publ-section"]'
            nbloques = hxs.select(bloques)
            n = len(nbloques)
            for i in range(1,n+1):
                paths = bloques+'/div['+str(i)+']/div/ul/li'
                print("Se parsea el bloque "+paths)
                pubs = hxs.select(paths)
                o  = len(pubs)
                for j in range(1, o+1):
                    print("")
                    try:
                        print("Se parsea el bloque "+paths+'['+str(j)+']')
                        titulo = (str)(response.xpath(paths+'['+str(j)+']/div/span[@class="title"]').extract())
                        titulo = titulo.split(">")[1]
                        titulo = titulo.split("<")[0]
                        print("El título es "+titulo)
                        pathbibtec = paths+'['+str(j)+']/nav/ul/li[2]/div/ul/li[1]/a'
                        pathauthors = paths+'['+str(j)+']/div[2]/span/a'
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
                            tipo = s.split("{")[0]
                            tipo = tipo.replace("@","")
                            print tipo
                            bib_data = parse_string(s,"bibtex")
                            nombrearchivo = urlbib.split("/")[-2]+"-"+urlbib.split("/")[-1]
                            print(nombrearchivo)
                            f = open(nombrearchivo+".ttl","w+")
                            f.write("@prefix owl: <http://www.w3.org/2002/07/owl#> .\n")
                            f.write("@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n")
                            f.write("@prefix ns0: <https://websemantica.icc/rdf/dblp-schema#> .\n")

                            f.close()
                            for entry in bib_data.entries.values():
                                #print entry.key
                                #print entry.fields.keys()
                                for value in entry.fields.keys():
                                    print value ,"=", bib_data.entries[entry.key].fields[value]
                        except:
                            print("No se pudo parsear el bibtec")
                    except:
                        print ("No es un bloque valido")

                    
                    print ("Publicación parseada con exito")
                print ("Bloque parseado con exito")
            print ("Página parseada con exito")

        except:
            print ("No se pudo parsear "+response.url)
