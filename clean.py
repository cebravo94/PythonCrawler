fstopwords = open("stopwords.txt")
stopwords = []
for stopword in fstopwords:
    stopwords.append(stopword.replace('\n', ''))
fstopwords.close()
#print stopwords
fterms = open("terms3.txt")
palabras = []
for term in fterms:
    terminos = term.lower().split(" ")
    for termino in terminos:
        termino = termino.replace('\n', ' ')
        if termino not in stopwords and termino not in palabras:
            palabras.append(termino.lower())
fterms.close()
for concept in palabras:
    print concept