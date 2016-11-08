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
import time

def main():
    count_S = 0
    count_F = 0
    movies = db_connect("select id_pozycja, tytul_org, rok_produkcji from Pozycja where foto = 'images/filmy/no_foto.jpg' and tytul_org!='brak' and rok_produkcji != '2000-01-01'", False)
    
    print 'Rozpoczynam wyszukiwanie zdjęć...'
    licz = 1
    for movie in movies:
        print licz
        licz = licz + 1
        
        photo_name = 'no_foto1.jpg'
        mini_photo_name = 'no_foto_mini1.jpg'

        poster_name = 'no_poster1.jpg'
        mini_poster_name = 'no_poster_mini1.jpg'

        movie_id = movie[0]
        movie_title = movie[1].encode('utf8', 'ignore')
        release_date = movie[2]
        release_date = str(release_date)
        if len(release_date) > 1:
            release_date = release_date[0:4]
        movieId = theMovieDB.FindMovie(movie_title, release_date)
        
        # idFilm = FindMovie('fight club')
        # data = GetAllData_photo(idFilm)
        # print GetPoster(data)

        photo_url = None
        if movieId != None:
            data = theMovieDB.GetAllData_photo(movieId)
            photo_url = theMovieDB.GetPhoto(data)
            poster_url = theMovieDB.GetPoster(data)
            if photo_url != None:
                count_S = count_S + 1
                mini_photo_name = str(movie_id)+'_mini.jpg'
                photo_name =str(movie_id)+'.jpg'

                download_photo(photo_url, photo_name)  
                im2 = Image.open(photo_name)
                print photo_name
                im2 = im2.resize((170, 96), Image.ANTIALIAS)
                im2.save(photo_name, 'JPEG', quality=100)
                
                download_photo(photo_url, mini_photo_name)
                im2 = Image.open(mini_photo_name)
                im2 = im2.resize((123, 69), Image.ANTIALIAS)
                im2.save(mini_photo_name, 'JPEG', quality=100)

            if poster_url != None:
                poster_name = poster_url
                mini_poster_name = 'p_' + str(movie_id) + '_mini.jpg'
                
                download_photo(poster_url, mini_poster_name)
                im2 = Image.open(mini_poster_name)
                im2 = im2.resize((160, 240), Image.ANTIALIAS)
                im2.save(mini_poster_name, 'JPEG', quality=100)

        db_connect("update Pozycja set foto_mini='images/filmy/" + mini_photo_name + "', foto = 'images/filmy/" + photo_name + "', plakat_mini = 'images/plakaty/" + mini_poster_name + "', plakat = '" + poster_name + "' where id_pozycja=" + str(movie_id) + ';', True)  
        time.sleep(3)
    count_F = len(movies) - count_S
    print 'Udalo się znalezc zdjecia dla ' + str(count_S) + ' pozycji.'
    print 'Nie udalo sie znalezc zdjecia dla ' + str(count_F) + ' pozycji.'

def download_photo(url,comicName):
    mp3file = urllib2.urlopen(url)
    output = open(comicName,'wb')
    output.write(mp3file.read())
    output.close()

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

main()