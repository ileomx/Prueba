# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib2
import urllib
import sys

url ="http://arxiv.org/list/gr-qc/new"
papersList = []
idItems = []
urls = []
files = []
titles = []
authors = []
abstracts = []
download = False
exclude = False

def pAyuda():
	f = open('get-arxiv.man')
	print f.read()
	f.close()

def buscarP(papersList, busqueda, download, exclude):
	palabras = []
	if ',' in palabras:
		palabras = busqueda.split(',')
	else:
		palabras.append(busqueda)

	if exclude:
		for paper in papersList:
			for palabra in palabras:
				if palabra.lower() not in paper['title'].lower() and palabra.lower() not in paper['abstract'].lower():
					print paper['file']+': '+paper['title'].decode('utf-8')
					if download:
						urllib.urlretrieve ('http://arxiv.org'+paper['url'].replace('abs','pdf'), paper['file']+".pdf")
						print '[PDF Downloaded...]'
						urllib.urlretrieve ('http://arxiv.org'+paper['url'].replace('abs','ps'), paper['file']+".ps")
						print '[PS Downloaded...]'
	else:
		for paper in papersList:
			for palabra in palabras:
				if palabra.lower() in paper['title'].lower() or palabra.lower() in paper['abstract'].lower():
					print paper['file']+': '+paper['title'].decode('utf-8')
					if download:
						urllib.urlretrieve ('http://arxiv.org'+paper['url'].replace('abs','pdf'), paper['file']+".pdf")
						print '[PDF Downloaded...]'
						urllib.urlretrieve ('http://arxiv.org'+paper['url'].replace('abs','ps'), paper['file']+".ps")
						print '[PS Downloaded...]'
try:
	f = urllib2.urlopen(url)
	soup = BeautifulSoup(f.read())
	f.close()
except HTTPerror, e:
	print "[Error] "+e.code
except URLerror, e:
	print "[Error] "+e.reason

dlpage = soup.find("div", id="dlpage")
for dt in dlpage.find_all('dt'): 
	for a in dt.find_all('a', {'title': 'Abstract'}):
		files.append(a.text)
		urls.append(a['href'])

for dd in dlpage.find_all('dd'):
	for div in dd.find_all('div', {'class': 'list-title'}):
		titles.append(div.text.replace('\n','').replace('Title: ','').encode('utf-8'))
	for div in dd.find_all('div', {'class': 'list-authors'}):
		authors.append(div.text.replace('\n','').replace('Authors:',''))
	
	if dd.p:
		abstracts.append(dd.p.text)
	else:
		abstracts.append('')

for i in range(len(titles)):
	papersList.append({'file':files[i], 'url':urls[i], 'title':titles[i], 'authors':authors[i], 'abstract':abstracts[i]})



if len(sys.argv) > 1:
	if '-' in sys.argv[1]:
		if 'd' in sys.argv[1]:
			download = True
		
		if 'e' in sys.argv[1]:
			exclude = True

		if sys.argv[2]:
			busqueda = sys.argv[2]
		else:
			pAyuda()
	else:
		busqueda = sys.argv[1]

	buscarP(papersList, busqueda, download, exclude)

else:
	pAyuda()

