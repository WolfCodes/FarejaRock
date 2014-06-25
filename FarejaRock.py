# -*- coding: utf-8 -*-
__author__ = 'Rodrigo Gomes'


#require https://github.com/Dirble/streamscrobbler-python
#agradecimento em especial a Håkan Nylén por disponibilizar
#o algoritmo streamscrobbler-python para extração de metadados

import urllib, time, os, urlparse,sys
from bs4 import BeautifulSoup

from streamscrobbler import streamscrobbler

streamscrobbler = streamscrobbler()

class Fareja():
   
    def __init__(self):
        self.aux = []
        self.musica = list()
        self.query_url = 'http://emp3world.com/search/%(query)s_mp3_download.html'
        self.links = list() 

    def radio(self, stream):
        self.stream = stream
        stationinfo = streamscrobbler.getServerInfo(self.stream)
        try:
            self.musica = str(dict(stationinfo.get("metadata"))['song'])
            if self.musica != '89 Radio Rock - We rock Sampa since 1985!':
                print "RADIO ROCK Tocando: %s" % self.musica
            else:
                print "Sem Musica -- Os Radialistas estão conversando Aguarde..."
        except:
            print "O sistema não conseguiu pegar o nome da musica"
        
        if self.musica != self.aux and self.musica != '89 Radio Rock - We rock Sampa since 1985!' and self.musica is not None:
            self.aux = self.musica
            self.procura(self.musica)
    
    def procura(self, query):
        self.links = []
        print "Procurando Links Diretos de %s na Web" % query
        query = (query.strip().lower())
        request = urllib.urlopen(self.query_url % { 'query': query })
        data = request.read()
        text = data.decode('utf-8')
        soup = BeautifulSoup(text)
        for tag in soup.findAll('a', href=True):
            tag['href'] = urlparse.urljoin(self.query_url, tag['href'])
            if tag['href'].endswith(".mp3"):
                self.links.append(tag['href'])
        print "%i links para download" % len(self.links)
        
        if len(self.links)==0:
            print 'ERRO Sem Links diretos para download! Reiniciando...'
            f1.radio(self.stream)  
            
        elif os.path.exists(query+".mp3"):
            time.sleep(10)
            f1.radio(self.stream)  
        else:
            print "baixando: %s Aguarde." % query
            urllib.urlretrieve(self.links[0],query+".mp3")

            
        
radios = ['http://www.webnow.com.br/streaming/autoplaylist/v1/radiorock.aac.pls']
fareja = Fareja()

while True:
    for i in radios:
        fareja.radio(i)
    