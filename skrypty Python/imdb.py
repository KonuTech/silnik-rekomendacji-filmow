# -*- coding: UTF-8 -*-
import urllib2
import urllib
import chardet
import re
def get_page(url):
    try:
        url = url.replace(" ","%")
        result = urllib2.urlopen(url)
        rawdata = result.read()
        return rawdata
    except urllib2.URLError, e:
        return None



def get_org_title(title):
    link = ''
    title = title.lower()
    title = title.replace('"', "'")
    title = title.replace(' ','+')
    title = title.replace("'","")
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
    title = title.replace("&quot;","")
    title = title.replace(':','')
    page = get_page('http://www.imdb.com/find?q=' + title + '&s=titles')
    
    link = ''
    if page != None:
        link = GetLink(page)
    
    if link == '':
        return '', None, '', ''

    content_page = get_page(link)

    if  content_page == None:
        return '', None, '', ''
    # runtime = GetRuntime(content_page)
    # genres = GetGenres(content_page)
    # description = GetDescription(content_page)
    # director = GetDirector(content_page)
    vote_average = GetVoteAverage(content_page)
    # countries = GetCountries(content_page)


    cast = []
    if content_page != None:
        cast = GetCast(content_page)
        release_date = GetReleaseDate(content_page)
    if page == None:
        return '', None, vote_average, ''
    if 'class="result_text' not in page:
        if 'class="title-extra"' in page:
            
            start = page.find('<span class="nobr">') + 19
            page = page[start:]
            start = page.find('>') + 1
            release_date = page[start:start+4]

            start = page.find('title-extra') + 13
            page = page[start:]
            end = page.find('<')
            title = page[:end].strip()
            if title != 'ml>':
                # return title.replace('"',''), runtime, genres, description, director, vote_average, countries, cast, release_date
                return title.replace('"',''), cast, vote_average, release_date
        else:
            
            start = page.find('<span class="nobr">') + 19
            page = page[start:]
            start = page.find('>') + 1
            release_date = page[start:start+4]

            start = page.find('itemprop="name"') + 16
            page = page[start:]
            end = page.find('<')
            title = page[:end].strip()
            if title != 'ml>':
                return title.replace('"',''), cast, vote_average, release_date
    else:   
        start=page.find('class="result_text"')
        page = page[start:]
        start = page.find('<a href="') + 9
        page = page[start:]
        end = page.find('"')
        page = get_page('http://www.imdb.com'+page[:end])
        if page == None:
            return '', None, '', ''
        if 'class="title-extra"' in page:   
            page_1 = str(page)
            start = page_1.find('<span class="nobr">') + 19
            page_1 = page_1[start:]
            start = page_1.find('>') + 1
            release_date = page_1[start:start+4]

            start = page.find('title-extra') + 29
            page = page[start:]
            end = page.find('<')
            title = page[:end].strip()
            
            if title != 'ml>':
                return title.replace('"',''), cast, vote_average, release_date
        else:
            
            page_1 = str(page)
            start = page_1.find('<span class="nobr">') + 19
            page_1 = page_1[start:]
            start = page_1.find('>') + 1
            release_date = page_1[start:start+4]

            start = page.find('itemprop="name"') + 16
            page = page[start:]
            end = page.find('<')
            title = page[:end].strip()
            
            
            if title != 'ml>':
                return title.replace('"',''), cast, vote_average, release_date
    return '', None, vote_average, ''

def GetLink(site):
    if 'No results found for' not in site and '</a>Titles' in site:
        start = site.find('class="result_text">') + 20
        site = site[start:]
        start = site.find('href="') + 6
        site = site[start:]
        end = site.find('"')
        link = site[:end]
        return 'http://imdb.com' + link
    else:
        return ''

def GetRuntime(site):
    if 'itemprop="duration"' in site:
        start = site.find('<time') + 5
        site = site[start:]
        start = site.find('>') + 1
        site = site[start:]
        end = site.find('</time>')
        return site[:end].strip()
    else:
        return ''

def GetGenres(site):
    if 'itemprop="genre"':
        genres = []
        while True: 
            if 'itemprop" itemprop="genre">' in site:
                genre, end = GetGenre(site)
                genres.append(genre)
                site = site[end:]
            else: 
                return genres 
    else:
        return ''

def GetGenre(site):
    start = site.find('itemprop" itemprop="genre">') + 27
    final_end = site.find('itemprop" itemprop="genre">') + 27
    site = site[start:]
    end = site.find('</span>')
    genre = site[:end]
    return genre.strip(), final_end

def GetDescription(site):
    if 'itemprop="description">' in site:
        start = site.find('itemprop="description">') + 23
        site = site[start:]
        end = site.find('</p>')
        return site[:end].strip()
    else:
        return ''


def GetDirector(site):
    if 'itemprop="director"' in site:
        start = site.find('itemprop="director"') + 19
        site = site[start:]
        start = site.find('class="itemprop" itemprop="name">') + 33
        site = site[start:]
        end = site.find('<')
        return site[: end].strip() 
    else:
        return ''

def GetVoteAverage(site):
    if 'itemprop="ratingValue">' in site:
        start = site.find('itemprop="ratingValue">') + 23
        site = site[start:]
        end = site.find('</span>')
        vote_average = site[:end].strip()
        if vote_average == '':
            return '5'
        else:
            return vote_average
    else:
        return '5'

def GetCountries(site):
    if 'class="inline">Country' in site:
        start = site.find('class="inline">Country') + 22
        site = site[start:]
        end = site.find('</div>')
        site = site[:end]
        countries = []
        while True:
            if "itemprop='url'>" in site:
                country, end = GetCountry(site)
                site = site[end:]
                countries.append(country)
            else:
                break
        return countries
    else:
        return []

def GetCountry(site):
    start = site.find("itemprop='url'>") + 15
    final_end = site.find("itemprop='url'>") + 15
    site = site[start:]
    end = site.find('</a>')
    return site[:end], final_end

def GetCast(site):
    if 'itemprop="actor"' in site:
        start = site.find('itemprop="actor"')
        site = site[start:]
        end = site.find('</tbody>')
        site = site[:end]
        cast = []

        licz = 0
        while True:
            if 'itemprop="actor"' in site:
                end, role = GetRole(site)
                cast.append(role)
                site = site[end:]
                licz = licz + 1
                if licz == 7:
                    break
            else:
                break
        return cast
    else:
        return []

def GetRole(site):
    role = []
    start = site.find('itemprop="name">') + 16
    final_end = site.find('itemprop="name">') + 16
    site = site[start:]
    start = site.find('</span>')
    role.append(site[:start].strip())

    start = site.find('<div>') + 5
    site = site[start:]
    start = site.find('</div>')
    role_tmp = site[:start].strip()
    if '>' in role_tmp:
        start = role_tmp.find('>') + 1
        role_tmp = role_tmp[start:]
        end = role_tmp.find('<')
        role_tmp = role_tmp[:end].strip()

    role_tmp = re.sub("\s\s+" , " ", role_tmp)
    role.append(role_tmp)

    return final_end, role 

def GetReleaseDate(site):
    if 'itemprop="datePublished" content="' in site:
        start = site.find('itemprop="datePublished" content="') + 34
        site = site[start:]
        end = site.find('"')
        return site[:end].strip()
    else:
        return ''

# print get_org_title('Mambo, Lula i piraci')