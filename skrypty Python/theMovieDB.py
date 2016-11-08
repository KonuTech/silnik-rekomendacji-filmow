# -*- coding: UTF-8 -*-
from urllib2 import Request, urlopen, HTTPError
import json
from pprint import pprint


GenresList = ['Drama','Dramat','Comedy','Komedia','Action','Akcja','Thriller','Thriller','Crime',u'Kryminał','Document','Dokumentalny','War','Wojenny','Adventure','Przygodowy','History','Historyczny', 'Animation','Animacja', 'Family', 'Familijny', 'Fantasy', 'Fantasy', 'Music', 'Musical', 'Romance', 'Romans', 'Sports Film', 'Sportowy', 'Western', 'Western', 'Science Fiction', 'Sci-fi', 'Indie', u'Kino niezależne', 'Horror', 'Horror', 'Documentary', 'Dokumentalny', 'Road Movie', 'Film drogi', 'Film Noir', 'Noir', 'Erotic', 'Erotyczny', 'Holiday', 'Wakacyjny','Suspense',u'Niepewność']
def change_time(czas):
  hours = int(czas) / 60
  minutes = int(czas) - hours * 60
  if hours > 0:
      hours = str(hours) + ' godz. '
  else:
      hours = ''
  return hours + str(minutes) + ' min.'

def FindMovie(s_id):
	headers = {"Accept": "application/json"}
	
	try:
		request = Request("https://api.themoviedb.org/3/find/tt" + s_id + "?external_source=imdb_id&api_key=moj_klucz", headers=headers)
	except ValueError:
		return '404'	
	response_body = urlopen(request).read()
	response_body = response_body.replace('-nan','0')
	response_body = response_body.replace('nan','0')
	data = json.loads(response_body)
	
	if len(data['movie_results']):
		popularity = float(data['movie_results'][0]['popularity'])
		vote_count = float(data['movie_results'][0]['vote_count'])
		if vote_count > 3:
			return data['movie_results'][0]
	return None

# def FindMovie(title, date):
# 	headers = {"Accept": "application/json"}
# 	try:
# 		_title = str(title)
# 		title = title.replace(' ', '+')
# 		title = title.replace('.', '+')
# 	except UnicodeEncodeError, e:
# 		return None

# 	try:
# 		request = Request("http://private-ba33-themoviedb.apiary.io/3/search/movie?api_key=70d907e0f58362eee8ad8f72503d4dc2&query=" + title.strip(), headers=headers)
# 	except ValueError:
# 		return '404'	
# 	response_body = urlopen(request).read()
# 	response_body = response_body.replace('-nan','0')
# 	response_body = response_body.replace('nan','0')
# 	data = json.loads(response_body)
	
# 	movies_count =  len(data['results'])
# 	if movies_count == 0:
# 		return None

# 	movie_id = None

# 	for x in range(0, len(data['results'])):
# 		tmdb_title = data['results'][x]['title']
# 		tmdb_release_year = data['results'][x]['release_date'][0:4]
# 		if tmdb_release_year == date:
# 			movie_id = data['results'][x]['id']
# 			return str(movie_id)

# 	return movie_id



def GetAllData(movieId):
	headers = {"Accept": "application/json"}
	try:
		request = Request("http://api.themoviedb.org/3/movie/" + str(movieId) + "?api_key=70d907e0f58362eee8ad8f72503d4dc2", headers=headers)
	except ValueError:
		return '404'	
	response_body = urlopen(request).read()
	data = json.loads(response_body)
	return data

def GetAllData_cast(movieId):
	headers = {"Accept": "application/json"}
	request = Request("http://api.themoviedb.org/3/movie/" + str(movieId) + "/casts?api_key=70d907e0f58362eee8ad8f72503d4dc2", headers=headers)
	response_body = urlopen(request).read()
	data = json.loads(response_body)
	return data

def GetAllData_photo(movieId):
	headers = {"Accept": "application/json"}
	request = Request("http://private-ba33-themoviedb.apiary.io/3/movie/" + str(movieId) + "/images?api_key=70d907e0f58362eee8ad8f72503d4dc2", headers=headers)
	data = None
	try:
		try:
			print '1'
			response_body = urlopen(request).read()
			data = json.loads(response_body)
		except HTTPError, e:  # Python 2.5 syntax
			return None
			if e.code == 404 or e.code == 504:
				print '2'
				e.msg = 'data not found on remote: %s' % e.msg
			raise
	except HTTPError, e:
		return None
		print e

	return data

def GetVoteAverage(data):
	vote_average = data['vote_average']
	return vote_average

def GetPoster(data):
	posters = data['posters']
	for poster in posters:
		aspect_ratio = poster['aspect_ratio']
		if (aspect_ratio == 0.67) and poster['file_path']!='':
			return 'https://image.tmdb.org/t/p/w780' + poster['file_path']
	return None

def GetReleaseDate(data):
	release_date = data['release_date'].strip()
	if release_date != None and release_date!='':
		return release_date
	else:
		return '2000-01-01'

def GetGenres(data):
	genres_list = []
	return data['genres']

def GetRuntime(data):
	runtime = data['runtime']
	if runtime != None:
		return change_time(runtime)
	else:
		return '0 min.'

def GetTagline(data):
	tagline = data['tagline']
	return tagline

def GetPopularity(data):
	popularity = data['popularity']
	return popularity

def GetDescription(data):
	overview = data['overview']
	return overview

def GetProductionCountries(data):
	data = data['production_countries']
	countries = []
	for country in data:
		countries.append(country['name'])
	return countries

def GetPhoto(data):
	photos = data['backdrops']
	for photo in photos:
		aspect_ratio = photo['aspect_ratio']
		if aspect_ratio == 1.78 and photo['file_path']!='':
			return 'https://image.tmdb.org/t/p/w780' + photo['file_path']
	return None

def GetCast(data):
	full_cast = data['cast']
	cast = []
	count = 0
	for roles in full_cast:
		count = count + 1
		role = []
		role.append(roles['name'])
		role.append(roles['character'])
		cast.append(role)
		if count == 5:
			break
	return cast

def GetDirector(data):
	full_crew = data['crew']
	cast = []
	count = 0
	for people in full_crew:
		role = people['job']
		if role == 'Director':
			director = people['name'].encode('utf8', 'ignore')
			id = people['id']
			return director, id
	return None

def GetKeywords(movieId):
	from urllib2 import Request, urlopen
	headers = {"Accept": "application/json"}
	request = Request("http://private-ba33-themoviedb.apiary.io/3/movie/" + str(movieId) + "/keywords?api_key=70d907e0f58362eee8ad8f72503d4dc2", headers=headers)
	response_body = urlopen(request).read()
	data = json.loads(response_body)
	keywords_data = data['keywords']
	keywords = []
	for keyword in keywords_data:
		keywords.append(keyword['name'].strip())
	return keywords