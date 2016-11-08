vote_average_tmdb = 5
vote_average_imdb = 9

popularity = 16
tmp_times_imdb = 50


tmp_vote_average_tmdb = float(vote_average_tmdb)
tmp_vote_average_imdb = float(vote_average_imdb)

tmp_times_tmdb = popularity



vote_average = (tmp_vote_average_tmdb * tmp_times_tmdb + tmp_vote_average_imdb * tmp_times_imdb) / (tmp_times_tmdb + tmp_times_imdb) 
print vote_average