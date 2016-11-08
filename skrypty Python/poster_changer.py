# -*- coding: UTF-8 -*-
import MySQLdb
import login
import re
import theMovieDB
import urllib2
import urllib
import Image


def main():
	db = MySQLdb.connect(host=login.GetHost(), user=login.GetUser(), passwd=login.GetPassword(), db=login.GetDataBase(), charset = "utf8", use_unicode = True)
	cur = db.cursor()
	cur_1 = db.cursor()
	cur.execute("select id_pozycja, tytul_org, rok_produkcji, plakat, (select count(id_pozycja) from Pozycja where rok_produkcji !='2000-01-01' and tytul_org!='brak' and plakat != 'no_poster1.jpg') from Pozycja where tytul_org != 'brak' and rok_produkcji!='2000-01-01' and plakat!='no_poster1.jpg' and id_pozycja > 452 order by id_pozycja limit 0,200;")
	cnt_1 = 1
	for row in cur:
		id_pozycja = row[0]
		tytul_org = row[1]
		
		rok_produkcji = row[2]
		rok = str(rok_produkcji)[0:4]
		plakat = row[3]
		cnt = row[4]
		print id_pozycja
		cnt_1 = cnt_1 + 1
		movieID = theMovieDB.FindMovie(tytul_org, rok)
		all_data = theMovieDB.GetAllData_photo(movieID)
		
		poster = None
		if all_data != None:
			poster = theMovieDB.GetPoster(all_data)

		if(poster != None):
			print 'dodaje plakat dla filmu: ' + str(tytul_org)

			mini_poster_name = 'p_' + str(id_pozycja) + '_mini.jpg'
			download_photo(poster, mini_poster_name)

			im2 = Image.open(mini_poster_name)
			im2 = im2.resize((160, 240), Image.ANTIALIAS)
			im2.save(mini_poster_name, 'JPEG', quality=100)
			cur_1.execute("update Pozycja set plakat = '" + re.escape(poster) + "', plakat_mini = 'images/plakaty/" + mini_poster_name + "' where id_pozycja=" + str(id_pozycja) + ";")	
			cur_1.execute("commit")

def download_photo(url,comicName):
	_file = urllib2.urlopen(url)
	output = open(comicName,'wb')
	output.write(_file.read())
	output.close()

main()
