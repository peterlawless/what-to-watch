import csv
from operator import itemgetter
import math

class User:
    def __init__(self, row):
        self.id = row[0]
        self.age = int(row[1])
        self.gender = row[2]
        self.simcoeffs = {}

class Movie:
    def __init__(self, row):
        self.id = row[0]
        self.title = row[1][:-7]
        self.genre = [int(x) for x in row[5:]]


class Rating:
    def __init__(self, row):
        self.userid = row[0]
        self.movieid = row[1]
        self.value = int(row[2])

    def __eq__(self, other):
        return self.userid == other.userid and self.movieid == other.movieid and self.value == other.value


class DataBase:
    def __init__(self,ratings, movies, users):
        self.ratings = ratings
        self.movies = movies
        self.users = users
        self.ratingslib = {movie.id: self.get_ratings(movie.id) for movie in self.movies}
        self.totalratings = {movie_id: len(self.ratingslib[movie_id]) for movie_id in self.ratingslib}
        self.avgratings = {movie_id: self.get_avg_rating(movie_id) for movie_id in self.ratingslib}
        self.similaritylib = {user.id: self.get_similarities(user) for user in self.users}

    def get_ratings(self, movie_id):
        return [rating for rating in self.ratings if rating.movieid == movie_id]

    def get_avg_rating(self, movie_id):
        return sum([rating.value for rating in self.ratingslib[movie_id]]) / self.totalratings[movie_id]

    def get_title(self, movie_id):
        return [movie.title for movie in self.movies if movie.id == movie_id][0]

    def get_user_ratings(self, user_id):
        return sorted([rating for rating in self.ratings if rating.userid == user_id], key = lambda rating: rating.movieid)

    def user_not_rated(self, user_id, movie_id):
        return all([user_id != rating.userid for rating in self.ratingslib[movie_id]])

    def nplusratings(self, movie_id, n):
        return self.totalratings[movie_id] >= n

    def nplus_usernot(self, user_id, movie_id, n):
        return self.nplusratings(movie_id, n) and self.user_not_rated(user_id, movie_id)

    def top_n_movies(self, n, rmin = 5):
        eligible = [(movie, self.avgratings[movie.id]) for movie in self.movies if self.nplusratings(movie.id, rmin)]
        return sorted(eligible, key = itemgetter(1), reverse = True)[:n]

    def top_n_recomm(self, user_id, n, rmin = 5):
        eligible = [(movie, self.avgratings[movie.id]) for movie in self.movies if self.nplus_usernot(user_id, movie.id, rmin)]
        return sorted(eligible, key = itemgetter(1), reverse = True)[:n]

    def rating_hist(self, user_id):
        return [rating.movieid for rating in self.get_user_ratings(user_id)]

    def hist_intersection(self, usr_one, usr_two):
        usr_one_ratings = [rating for rating in self.get_user_ratings(usr_one) if rating.movieid in self.rating_hist(usr_two)]
        usr_two_ratings = [rating for rating in self.get_user_ratings(usr_two) if rating.movieid in self.rating_hist(usr_one)]
        return usr_one_ratings, usr_two_ratings

    def similarity_vectors(self, usr_one, usr_two):
        usr_one_ratings, usr_two_ratings = self.hist_intersection(usr_one, usr_two)
        usr_one_values = [rating.value for rating in usr_one_ratings]
        usr_two_values = [rating.value for rating in usr_two_ratings]
        return usr_one_values, usr_two_values

    def similarity_coefficient(self, usr_one, usr_two):
        return euclidean_distance(*self.similarity_vectors(usr_one, usr_two))

    def get_similarities(self, usr):
        usr.simcoeffs = {user.id: self.similarity_coefficient(usr.id, user.id) for user in self.users if user.id != usr.id}
        return usr.simcoeffs

def read_ratings_data():
    ratings = []
    with open('./ml-100k/u.data', encoding = 'latin_1') as ratings_file:
        ratings_reader = csv.reader(ratings_file, delimiter = '\t')
        for row in ratings_reader:
            ratings.append(Rating(row))
    return ratings


def read_movies_data():
    movies = []

    with open('./ml-100k/u.item', encoding = 'latin_1') as movies_file:
        movies_reader = csv.reader(movies_file, delimiter = '|')
        for row in movies_reader:
            movies.append(Movie(row))
    return movies


def read_users_data():
    users = []
    with open('./ml-100k/u.user', encoding = 'latin_1') as users_file:
        users_reader = csv.reader(users_file, delimiter = '|')
        for row in users_reader:
            users.append(User(row))
    return users


def euclidean_distance(v, w):
    """Given two lists, give the Euclidean distance between them on a scale
    of 0 to 1. 1 means the two lists are identical.
    """

    # Guard against empty lists.
    if len(v) is 0:
        return 0

    # Note that this is the same as vector subtraction.
    differences = [v[idx] - w[idx] for idx in range(len(v))]
    squares = [diff ** 2 for diff in differences]
    sum_of_squares = sum(squares)

    return 1 / (1 + math.sqrt(sum_of_squares))

def main():
    pass


if __name__ == '__main__':
    main()
