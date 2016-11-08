# -*- coding: UTF-8 -*-
import urllib2
import chardet
import MySQLdb
import codecs
import datetime
import gc
import login
import theMovieDB
import imdb
import re
import pf
import HTMLParser

def get_page(url):
    try:
        url = url.replace(" ","%")
        result = urllib2.urlopen(url)
        rawdata = result.read()
        encoding = chardet.detect(rawdata)
        return rawdata.decode(encoding['encoding'])
    except urllib2.URLError, e:
        handleError(e)

def CompleteData():
    start_time  = datetime.datetime.now()
    db = MySQLdb.connect(host=login.GetHost(), user=login.GetUser(), passwd=login.GetPassword(), db=login.GetDataBase(), charset = "utf8", use_unicode = True)
    cur = db.cursor()
    cur.execute("select p.id_pozycja, p.tytul_pl from Pozycja as p where rok_produkcji = '2000-01-01' and id_pozycja > 1040 order by id_pozycja asc;")
    h = HTMLParser.HTMLParser() 
    print ''
    print 'Zaczynam szuka dokładnych informacji na temat mowych filmów...'
    print ''
    licz = 0
    compl_data = 0
    for row in cur:
        licz = licz + 1
        id_pozycja = row[0]
        tytul_pl = row[1].encode('utf-8', 'ignore')
        print str(id_pozycja) + ' <------ id pozycja'
        org_title, cast, vote_average_imdb, rok_produkcji = imdb.get_org_title(tytul_pl)
        movieId = None
        if org_title != '':
            rok_produkcji = rok_produkcji[0:4]
            movieId = theMovieDB.FindMovie(org_title, rok_produkcji)
            tytul_pl = tytul_pl.decode('utf-8')
            org_title = org_title.decode('utf-8')
            org_title = re.escape(org_title)
            
        if org_title != '':
            if movieId != None:
                print 'Znalazlem dane do filmu: ' + tytul_pl + ' / ' + org_title
                all_data = theMovieDB.GetAllData(movieId)
                data_cast = theMovieDB.GetAllData_cast(movieId)
                release_date = theMovieDB.GetReleaseDate(all_data).strip()
                vote_average_tmdb = theMovieDB.GetVoteAverage(all_data)
                countries = theMovieDB.GetProductionCountries(all_data)
                popularity = theMovieDB.GetPopularity(all_data)
                keywords = theMovieDB.GetKeywords(movieId)          
                
                tmp_times_imdb = 50
                tmp_vote_average_tmdb = float(vote_average_tmdb)
                tmp_vote_average_imdb = float(vote_average_imdb)
                tmp_times_tmdb = float(popularity)
                vote_average = (tmp_vote_average_tmdb * tmp_times_tmdb + tmp_vote_average_imdb * tmp_times_imdb) / (tmp_times_tmdb + tmp_times_imdb) 

                description = ''
                link = pf.GetLink(tytul_pl.encode('utf-8'))
                if link != None: 
                    pf_site = get_page(link)
                    description = pf.GetDescription(pf_site)
                description = description
                description = re.escape(description)


                # print org_title
                # print release_date
                # print description
                # print vote_average
                # print popularity
                # print id_pozycja


                # 1. Update pozycji
                # print "update Pozycja set tytul_org='" + org_title + "', rok_produkcji='" + release_date + "', opis='" + description + "', ocena=" + str(vote_average) + ", popularnosc=" + str(popularity) + " where id_pozycja=" + str(id_pozycja) + ";"
                # print "update Pozycja set tytul_org='" + org_title + "', rok_produkcji='" + release_date + "', opis='" + description + "', ocena=" + str(vote_average) + ", popularnosc=" + str(popularity) + " where id_pozycja=" + str(id_pozycja) + ";"
                cur.execute("update Pozycja set tytul_org='" + org_title + "', rok_produkcji='" + release_date + "', opis='" + description + "', ocena=" + str(vote_average) + ", popularnosc=" + str(popularity) + " where id_pozycja=" + str(id_pozycja) + ";")
                cur.execute("commit")
                compl_data = compl_data + 1
                # 2. Powiązanie pozycji z państwem
                for country in countries:
                    cur.execute("insert into Panstwo (nazwa_panstwo) Select * from (select '" + country + "') as tmp where not exists (select nazwa_panstwo from Panstwo where nazwa_panstwo = '" + country + "') limit 0,1;")
                    cur.execute("commit")
                    cur.execute("insert into FK_Panstwo_Pozycja(id_panstwo, id_pozycja) values((select id_panstwo from Panstwo where nazwa_Panstwo='" + country + "'), (select id_pozycja from Pozycja where tytul_pl='" + tytul_pl + "' and tytul_org='" + org_title + "' and rok_produkcji = '" + release_date + "' limit 0,1));")
                    cur.execute("commit")

                # 3. Dodawanie aktorów
                for actor_role in cast:
                    actor_name = actor_role[0].decode('utf-8', 'ignore')
                    role_name = actor_role[1].decode('utf-8', 'ignore')

                    cur.execute("insert into Aktor (nazwa_aktor) Select * from (select '" + re.escape(actor_name) + "') as tmp where not exists (select nazwa_aktor from Aktor where nazwa_Aktor = '" + re.escape(actor_name) + "') limit 0,1;")
                    cur.execute("commit")
                    # print "insert into FK_Aktor_Pozycja(id_aktor, id_pozycja, nazwa_postac) values((select id_aktor from Aktor where nazwa_aktor='" + re.escape(actor_name) + "'), (select id_pozycja from Pozycja where tytul_pl='" + title + "' and tytul_org='" + org_title + "' and czas_trwania = '" + runtime + "' and rok_produkcji = '" + release_date + "' limit 0,1), '" + re.escape(role_name) + "');"
                    cur.execute("insert into FK_Aktor_Pozycja(id_aktor, id_pozycja, nazwa_postac) values((select id_aktor from Aktor where nazwa_aktor='" + re.escape(actor_name) + "'), (select id_pozycja from Pozycja where tytul_pl='" + tytul_pl + "' and tytul_org='" + org_title + "' and rok_produkcji = '" + release_date + "' limit 0,1), '" + re.escape(role_name) + "');")
                    cur.execute("commit")

                # 4. Dodawanie słów kluczowych
                for keyword in keywords:
                    # keyword = h.unescape(keyword.encode('utf8', 'ignore').strip())
                    
                    cur.execute("insert into Keyword (nazwa_keyword) Select * from (select '" + re.escape(keyword) + "') as tmp where not exists (select nazwa_keyword from Keyword where nazwa_keyword = '" + re.escape(keyword) + "') limit 0,1;")
                    cur.execute("commit")
                    
                    cur.execute("insert into FK_Keyword_Pozycja(id_keyword, id_pozycja) values((select id_keyword from Keyword where nazwa_keyword='" + re.escape(keyword) + "'), (select id_pozycja from Pozycja where tytul_pl='" + tytul_pl + "' and tytul_org='" + org_title + "' and rok_produkcji = '" + release_date + "' limit 0,1));")
                    cur.execute("commit")
            else:
                # print '3'
                cur.execute("update Pozycja set tytul_org='" + org_title + "' where id_pozycja=" + str(id_pozycja) + ";")
                cur.execute("commit")
        else:
            # print '4'
            # print "update Pozycja set tytul_org='brak' where id_pozycja=" + str(id_pozycja) + ";" 
            cur.execute("update Pozycja set tytul_org='brak' where id_pozycja=" + str(id_pozycja) + ";")
            cur.execute("commit")
    end_time = datetime.datetime.now()
    print 'Czas trwania procesu: ' + str(end_time - start_time)[2:9]
    print 'Przejrzano ' + str(licz) + ' filmy'
    print 'Zaktualizowano informacje na temat ' + str(licz) + ' filmów'

CompleteData()