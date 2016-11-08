# -*- coding: UTF-8 -*-
import urllib2
import urllib
import chardet
import MySQLdb
import codecs
import json
import Image
import re
import theMovieDB
import imdb
import login

def main():
    count_S = 0
    count_F = 0
    movies = db_connect("select id_pozycja from Pozycja where okladka = 'images/plakaty/no_poster.jpg';", False)
    
    print 'Rozpoczynam wyszukiwanie plakatów...'
    licz = 1
    for movie in movies:
        print licz
        licz = licz + 1
        photo_name = 'no_foto1.jpg'
        movie_id = movie[0]
        movie_title = movie[1].encode('utf8', 'ignore')
        movie_original_title = imdb.get_org_title(movie_title)
        if movie_original_title == None:
            movie_original_title = movie_title 
        movie_original_title_link = movie_original_title.replace(' ','%20')
        movieId = theMovieDB.FindMovie(movie_original_title_link)
        photo_url = None
        if movieId != None:
            photo_url = theMovieDB.GetPoster(movieId)
            
        if photo_url != None:
            count_S = count_S + 1
            photo_name = 'poster_' + str(movie_id)+'.jpg'
            download_photo(photo_url, photo_name)
            im1 = Image.open(photo_name)
            im1.save(photo_name, 'JPEG', quality=quality_val)
        db_connect("update Pozycja set okladka = 'images/plakaty/" + photo_name + "' where id_pozycja=" + str(movie_id) + ';', True)  
    count_F = len(movies) - count_S
    print 'Udalo się znalezc plakaty dla ' + str(count_S) + ' pozycji.'
    print 'Nie udalo sie znalezc plakatów dla ' + str(count_F) + ' pozycji.'

def download_photo(url,comicName):
    image=urllib.URLopener()
    image.retrieve(url,comicName)
    image.close()

def db_connect(query, isInsert):
    db = MySQLdb.connect(host=login.GetHost(), user=login.GetUser(), passwd=login.GetPassword(), db=login.GetDataBase(), charset = "utf8", use_unicode = True) 
    cur = db.cursor() 

    cur.execute(query)
    if isInsert:
        cur.execute("commit")
    return_list = []
    for row in cur.fetchall() :
        return_list.append(row)
    return return_list