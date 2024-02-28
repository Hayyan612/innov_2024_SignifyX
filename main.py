import requests
import json
import warnings
import urllib.request
import bs4 as bs
import pickle
import numpy as np
 
warnings.filterwarnings('ignore') 

model = pickle.load(open('nlp_model.pkl', 'rb'))
transformer = pickle.load(open('transform.pkl', 'rb'))

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhODExOGM1Y2M1ZWM3MjA2ZWIyYmQ5Y2I5NjE1NGE2NiIsInN1YiI6IjY1ZGQ5OGU1MmFjNDk5MDE3ZGNiNGJiZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.rlNyTaRD7OyK5m8gxfO28WYAI45HBbb3sSUjUiSOMhI"
}

def helper(genre):

    genre = genre

    url_genre = f"http://api.themoviedb.org/3/discover/movie?with_genres={genre}&page=1"

    response = requests.get(url_genre, headers=headers)

    res = json.loads(response.text)

    results = res['results']

    dicti = {}


    for i in results:

        id = i['id']
        url_details = f"https://api.themoviedb.org/3/movie/{id}?language=en-US"
        responsed = requests.get(url_details, headers=headers)

        resd = json.loads(responsed.text)
        imdb_id = resd['imdb_id']


        sauce = urllib.request.urlopen('https://www.imdb.com/title/{}/reviews?ref_=tt_ov_rt'.format(imdb_id)).read()
        soup = bs.BeautifulSoup(sauce,'lxml')
        soup_result = soup.find_all("div",{"class":"text show-more__control"})



        reviews_list = [] # list of reviews
        reviews_status = [] # list of comments (good or bad)
        for reviews in soup_result:
            if reviews.string:
                reviews_list.append(reviews.string)
                # passing the review to our model
                movie_review_list = np.array([reviews.string])
                movie_vector = transformer.transform(movie_review_list)
                pred = model.predict(movie_vector)
                reviews_status.append('Good' if pred else 'Bad')
        i['score'] = reviews_status.count('Good')

    results = sorted(results, key=lambda d: d['score'], reverse=True) 


    return results


def get_popular():

    url = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1"

    response = requests.get(url, headers=headers)

    res = json.loads(response.text)

    results = res['results']

    return results

def get_now_playing():

    url = "https://api.themoviedb.org/3/movie/now_playing?language=en-US&page=1"

    response = requests.get(url, headers=headers)

    res = json.loads(response.text)

    results = res['results']

    return results