# -*- coding: UTF-8 -*-
import urllib2
import chardet
import re

def GetLink(title, year):
	title = title.lower()
    # title = title.replace(' ','+')
    # title = title.replace("'","")
	title = title.replace("ż","z")
	title = title.replace("ó","o")
	title = title.replace("ź","z")
	title = title.replace("ł","l")
	title = title.replace("ś","s")
	title = title.replace("ć","c")
	title = title.replace("ą","a")
	title = title.replace("ę","e")
	title = title.replace("Ś","s")
	title = title.replace("Ł","l")
	title = title.replace("ń","n")
	title = title.replace("Ć","c")

	year_site = ''
	site = get_page('http://www.portalfilmowy.pl/baza_filmowa?c_page=1&sf2=1&sf=1&s=' + title)
	link = ''
	while 'class="movie_db_list_title"' in site and year != year_site:
		link = ''
		start = site.find('class="movie_db_list_title"')
		site = site[start:]
		start = site.find('<a href="') + 9
		site = site[start:]
		end = site.find('"')
		link = str(site[:end])

		start = site.find('</a> | <a href="b')
		year_site = site[start-4:start]
	if link != '' and year_site == year:
		return 'http://portalfilmowy.pl/' + link
	else:
		return None

def GetDescription(site):
	if 'justify;" class="movie_record_lead">' in site:
		start = site.find('justify;" class="movie_record_lead">') + 36
		site = site[start:]
		end = site.find('</div>')
		description = site[:end]
		description = description.replace('<br />', ' ')
		description = Shorter(description)
		return description.strip()
	else:
		return ''

def get_page(url):
	try:
		url = url.replace(" ","%")
		result = urllib2.urlopen(url)
		rawdata = result.read()
		encoding = chardet.detect(rawdata)
		return rawdata
	except urllib2.URLError, e:
		handleError(e)

def Shorter(string):
	if len(string) > 625:
		string = string[0:625]
		end = string.rfind('. ') + 1
		string = string[:end]
	return string