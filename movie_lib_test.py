from movie_lib import *
import csv
import operator


user_row = ['196','24','M','technician','85711']
other_user_row = ['197','24','M','technician','85711']
movie_row = ['28','Apollo 13 (1995)','01-Jan-1995','','http://us.imdb.com/M/title-exact?Apollo%2013%20(1995)',
'0','1','0','0','0','0','0','0','1','0','0','0','0','0','0','0','1','0','0']
rating_row = ['196', '28', '5', '881250949']
other_rating_row = ['197', '28', '4', '881250949']
user = User(user_row)
other_user = User(other_user_row)
movie = Movie(movie_row)
rating = Rating(rating_row)
other_rating = Rating(other_rating_row)
ratings = [rating, other_rating]
movies = [movie]
users = [user, other_user]
database = DataBase(ratings, movies, users)


def test_create_user_with_attributes():
    assert user.id == '196'
    assert user.age == 24
    assert user.gender == 'M'


def test_create_movie_with_attributes():
    assert movie.id == '28'
    assert movie.title == 'Apollo 13'
    assert movie.genre == [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]


def test_create_rating_with_attributes():
    assert rating.userid == '196'
    assert rating.movieid == '28'
    assert rating.value == 5


def test_create_DataBase():
    assert database.ratings == ratings
    assert database.movies == movies
    assert database.users == users
    assert database.ratingslib == {'28': ratings}
    assert database.totalratings == {'28': 2}
    assert database.avgratings == {'28': 4.5}


def test_find_ratings_for_movie_by_id():
    assert database.get_ratings('28') == ratings


def test_find_average_rating_for_movie_by_id():
    assert database.get_avg_rating('28') == 4.5


def test_find_movie_title_by_movie_id():
    assert database.get_title('28') == 'Apollo 13'


def test_find_all_ratings_for_a_user():
    assert database.get_user_ratings('196') == [rating]


def test_read_ratings_data():
    ratings = read_ratings_data()
    assert all([isinstance(rating, Rating) for rating in ratings])


def test_read_movies_data():
    movies = read_movies_data()
    assert all([isinstance(movie, Movie) for movie in movies])


def test_read_users_data():
    users = read_users_data()
    assert all([isinstance(user, User) for user in users])


def test_top_n_movies():
    assert database.top_n_movies(1, 1) == [(movie, 4.5)]


def test_top_n_recomm():
    assert database.top_n_recomm(user.id, 1, 1) == []
    assert database.top_n_recomm('195', 1, 1) == [(movie, 4.5)]


def test_viewing_hist():
    assert database.rating_hist('196') == ['28']


def test_hist_intersection():
    assert database.hist_intersection('196','197') == ([rating], [other_rating])


def test_similarity_vectors():
    assert database.similarity_vectors('196', '197') == ([5], [4])


def test_similarity_coefficient():
    assert database.similarity_coefficient('196', '197') == euclidean_distance([5],[4])

def test_simoeffs():
    assert user.simcoeffs == {other_user.id: euclidean_distance([5], [4])}
