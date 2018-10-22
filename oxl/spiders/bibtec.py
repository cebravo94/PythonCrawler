# -*- coding: utf-8 -*-
import time
import scrapy
import urllib
import urllib2
import re
import os
import os.path

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

    def parseauthor(self, url):   #método que crea archivos para los autores
        try:
            f = urllib.urlopen(url) #Abre la URL del bibtec
            s = f.read()
            s = s.split('data-name="')[1]
            s = s.split('">')[0]
            nombrearchivo = url.split("/")[-1]
            if os.path.isfile(nombrearchivo+".ttl")==False:
                f = open(nombrearchivo+".ttl","w+")
                f.write("@prefix voc: <https://websemantica.icc/rdf/vocabulary#> .\n\n")
                f.write("<"+url+">\n")
                f.write('\tvoc:Name "'+s+'" .')
                f.close()
        except:
            "No se pudieron generar los autores"

    def parse_item(self, response):
        camposbibtex = ["address","annote","author","booktitle","chapter","crossref","doi","edition","editor","institution","journal","month","number","organitzation","pages","publisher","school","series","title","type","volume","year"]
        url = (str)(response.url)
        try:
            print("\nSe intenta parsear "+response.url)
            hxs = HtmlXPathSelector(response)
            bloques = '//*[@id="publ-section"]'
            nbloques = hxs.select(bloques)
            n = len(nbloques)
            for i in range(1,n+1):
                paths = bloques+'/div['+str(i)+']/div/ul/li'
                #print("Se parsea el bloque "+paths)
                pubs = hxs.select(paths)
                o  = len(pubs)
                for j in range(1, o+1):
                    print("")
                    try:
                        #print("Se parsea el bloque "+paths+'['+str(j)+']')
                        titulo = (str)(response.xpath(paths+'['+str(j)+']/div/span[@class="title"]').extract())
                        titulo = titulo.split(">")[1]
                        titulo = titulo.split("<")[0]
                        pathbibtec = paths+'['+str(j)+']/nav/ul/li[2]/div/ul/li[1]/a'
                        pathauthors = paths+'['+str(j)+']/div/span/a'
                        #print(pathauthors)
                        urlbib = (str)(response.xpath(pathbibtec).extract())
                        urlbib = urlbib.split('"')[1]
                        try:
                            s = (str)(response.xpath(pathauthors).extract()) #Obtiene las url de los autores
                            s2 = s.split("href")
                            p=len(s2)
                            authors = []
                            authors.append(url)
                            for k in range(0,p):
                                s3 = s2[k]
                                if '"' in s3:
                                    s3 = s3.split('"')[1]
                                    authors.append(s3)
                            setautores = set(authors)
                            result = list(setautores)
                            autores=""
                            for k in range(0, len(result)):
                                self.parseauthor(result[k])
                                autores += "\n\tvoc:HasAuthor <"+result[k]+"> ;"
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
                            #print tipo
                            bib_data = parse_string(s,"bibtex")
                            nombrearchivo = urlbib.split("/")[-2]+"-"+urlbib.split("/")[-1]
                            if os.path.isfile(nombrearchivo+".ttl")==False:
                                f = open(nombrearchivo+".ttl","w+")
                                f.write("@prefix owl: <http://www.w3.org/2002/07/owl#> .\n")
                                f.write("@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n")
                                f.write("@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n")
                                f.write("@prefix voc: <https://websemantica.icc/rdf/vocabulary#> .\n\n")
                                for entry in bib_data.entries.values():
                                    #print entry.key
                                    #print entry.fields.keys()
                                    uri = bib_data.entries[entry.key].fields["biburl"]
                                    uri = uri.replace("bib","html")
                                    f.write("<"+uri+">")
                                    f.write("\n\trdf:type voc:"+tipo.capitalize()+" ;")
                                    f.write(autores)
                                    for value in entry.fields.keys():
                                        #print value ,"=", bib_data.entries[entry.key].fields[value]
                                        if value in camposbibtex:
                                            valor = bib_data.entries[entry.key].fields[value]
                                            valor = valor.replace("{","")
                                            valor = valor.replace("}","")
                                            valor = valor.replace("\\","")
                                            f.write("\n\tvoc:"+value.capitalize()+' "'+valor+'" ;')
                                f.seek(-1, os.SEEK_END)
                                f.truncate()
                                f.write(".")
                                f.close()
                                
                        except:
                            print("No se pudo parsear el bibtec")
                    except:
                        print ("No es un bloque valido")

                    
                    print ("Publicación parseada con exito")
                print ("Bloque parseado con exito")
            print ("Página parseada con exito")

        except:
            print ("No se pudo parsear "+response.url)

