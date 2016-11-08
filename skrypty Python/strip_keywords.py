# -*- coding: UTF-8 -*-
import MySQLdb
import login
import re

def main():
	db = MySQLdb.connect(host=login.GetHost(), user=login.GetUser(), passwd=login.GetPassword(), db=login.GetDataBase(), charset = "utf8", use_unicode = True)
	cur = db.cursor()
	cur_1 = db.cursor()
	cur.execute("select id_pozycja, opis from Pozycja;")
	
	for row in cur:
		id_pozycja = row[0]
		opis = row[1]
		print len(opis)
		# print id_pozycja
		opis = Shorter(opis)
		cur_1.execute("update Pozycja set opis = '" + re.escape(opis) + "' where id_pozycja=" + str(id_pozycja) + ";")	
		cur_1.execute("commit")

def Shorter(string):
	if len(string) > 625:
		string = string[0:625]
		end = string.rfind('. ') + 1
		string = string[:end]
	return string


main()


# # -*- coding: UTF-8 -*-
# import MySQLdb
# import login
# import re

# def main():
# 	db = MySQLdb.connect(host=login.GetHost(), user=login.GetUser(), passwd=login.GetPassword(), db=login.GetDataBase(), charset = "utf8", use_unicode = True)
# 	cur = db.cursor()
# 	cur_1 = db.cursor()
# 	cur.execute("select id_pozycja, opis from Pozycja;")
	
# 	for row in cur:
# 		id_pozycja = row[0]
# 		opis = row[1]
# 		print len(opis)
# 		# print id_pozycja
# 		opis = Shorter(opis)
# 		cur_1.execute("update Pozycja set opis = '" + re.escape(opis) + "' where id_pozycja=" + str(id_pozycja) + ";")	
# 		cur_1.execute("commit")

# def Shorter(string):
# 	if len(string) > 625:
# 		string = string[0:625]
# 		end = string.rfind('. ') + 1
# 		string = string[:end]
# 	return string


# main()