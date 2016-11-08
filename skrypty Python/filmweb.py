# -*- coding: UTF-8 -*-
import urllib2
import chardet
import re

def GetLink(title):
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

	site = get_page('http://www.filmweb.pl/search/film?q=' + title.replace(' ', "+"))
	start = site.find('sep-hr resultsList')
	site = site[start:]
	start = site.find('hdr hdr-medium" href="') + 22
	site = site[start:]
	end = site.find('"')
	return 'http://filmweb.pl' + site[:end]

def GetLinkWithData(title,data):
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

	site = get_page('http://www.filmweb.pl/search/film?q=' + title + '&startYear=' + str(data) + '&endYear=' + str(data) + '&startRate=&endRate=&startCount=&endCount=')
	start = site.find('sep-hr resultsList')
	site = site[start:]
	start = site.find('hdr hdr-medium" href="') + 22
	site = site[start:]
	end = site.find('"')
	return 'http://filmweb.pl' + site[:end]

def GetInformations(link):
	site = get_page(link)
	rating = GetRating(site)
	# description = GetDescription(site)
	# production_countries = GetProductionCountries(site)
	original_title = GetOriginalTitle(site)
	release_year = GetReleaseYear(site)
	# time = GetTime(site)
	# director = GetDirector(site)
	# return rating.strip().replace(',','.'), description, production_countries
	return original_title, release_year, rating

def GetRating(site):
	if 'filmRate' in site:
		start = site.find('filmRate')
		site = site[start:]
		start = site.find('v:average') + 12
		site = site[start:]
		return site[:3]
	else:
		return None

def GetReleaseYear(site):
	start = site.find('class=halfSize>(') + 16
	site = site[start:]
	site = site[:4]
	return site

def GetTime(site):
	start = site.find('icon-small-clock') + 21
	site = site[start:]
	end = site.find('</div>')
	return site[:end].strip()

def GetDirector(site):
	start = site.find('v:directedBy">') + 14
	site = site[start:]
	end = site.find('</a>')
	return site[:end].strip()

def GetDescription(site):
	if 'filmPlot' in site:
		start = site.find('filmPlot') + 12
		site = site[start:]
		end = site.find('</p>')
		site = site[:end]
		return site
	# else:
	# 	start = site.find('<p class=text>')
	# 	site = site[start:]
	# 	start =  site.find('<a href="') + 9
	# 	site = site[start:]
	# 	end = site.find('descs') + 5
	# 	link = 'http://filmweb.pl' + site[:end]
	# 	site = get_page(link)
	# 	start = site.find('<p class=text>') + 14
	# 	site = site[start:]
	# 	end = site.find('</p>')
	# 	description = site[:end]
	# 	licz = 0
	# 	while '<' in description:
	# 		licz = licz + 1
	# 		start = description.find('<')
	# 		end = description.find('>') + 1
	# 		description = description[:start] + description[end:]
	# 	return description
	# return None

def GetOriginalTitle(site):
	if 'text-large caption' in site:
		start = site.find('text-large caption') + 20
		site = site[start:]
		end = site.find('</h2>')
		site = site[:end]
		return site	
	else:
		return None

def GetProductionCountries(site):
	if 'countryId' in site:
		countries = []
		while 'countryId' in site:
			country, end = GetCountry(site)
			site = site[end:]
			countries.append(country)
		return countries
	else:
		return None

def GetCountry(site):
	start = site.find('countryIds') + 10
	final_end = int(start)
	site = site[start:]
	start = site.find('>')
	site = site[start:]
	end = site.find('</a>')
	country = site[:end]
	return country, final_end

def get_page(url):
	try:
		url = url.replace(" ","%")
		result = urllib2.urlopen(url)
		rawdata = result.read()
		encoding = chardet.detect(rawdata)
		return rawdata.decode(encoding['encoding'])
	except urllib2.URLError, e:
		handleError(e)

# link = GetLink('Bękarty wojny')
# print GetInformations(link)