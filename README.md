USO:    scrapy crawl bibtec --nolog
Para cambiar la url de inicio del crawler, hay que cambiar el campo start_urls en el archivo bibtec.py de la carpeta spiders.
Debe ser un índice de autores (ejemplo: https://dblp.uni-trier.de/pers?prefix=Re)

Requerimientos:
Python 2.7
scrapy (pip install scrapy) (que requiere de más librerías: https://stackoverflow.com/questions/22556965/how-to-install-scrapy-on-ubuntu)
pybtex (pip install pybtex)