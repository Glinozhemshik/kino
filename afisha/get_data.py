import datetime, time, json
from .models import *
from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests, re
import dateutil.parser
import iso8601


def del_data(request):
    for item in Cinema.objects.all():
        item.delete()
    for item in Film.objects.all():
        item.delete()
    for item in Seance.objects.all():
        item.delete()
    return HttpResponse('deleted')


def get_data(request):

    response = requests.get(url="https://api.internationalshowtimes.com/v4/showtimes", params={'countries': 'GB', 'fields': 'id,movie_id,cinema_id,start_at','location':'51.51,-0.13', 'distance': '500'}, headers={'X-API-Key': 'iBLYR2MIVfV8uZ3hSMdg2OJVmJpCnSp0'},)
    if response.status_code == 200:
        data = response.json()['showtimes']
        i = 1
        for item in data:
            if item['cinema_id'] == None or item['movie_id'] == None:
                continue

            try:
                film_object = Film.objects.get(movie_id=item['movie_id'])
            except Film.DoesNotExist:
                film_response = requests.get(
                    url="https://api.internationalshowtimes.com/v4/movies/" + str(item['movie_id']), params={},
                    headers={'X-API-Key': 'iBLYR2MIVfV8uZ3hSMdg2OJVmJpCnSp0'}, )
                film_data = film_response.json()
                film = Film()

                try:
                    film.movie_id = item['movie_id']
                    film.name = film_data['movie']['original_title']
                    film.about = film_data['movie']['synopsis']
                    film.poster_url = film_data['movie']['poster_image']['image_files'][6]['url']
                    film.trailer_url = film_data['movie']['trailers'][0]['trailer_files'][0]['url']
                    film.trailer_url = str.replace(film_object.trailer_url, 'watch?v=', 'embed/')
                    film.runtime = int(film_data['movie']['runtime'])
                    film.genres = json.dumps(film_data['movie']['genres'])

                    fil = film_data["movie"]["ratings"]
                    for k in fil:
                        if k == "imdb":
                            for v in fil[k]:
                                if v == "value":
                                    film.reting = fil[k][v]
                except TypeError:
                    print('TypeError')

                film.save()

            try:
                cinema = Cinema.objects.get(cinema_id=item['cinema_id'])
            except Cinema.DoesNotExist:
                cinema_responce = requests.get(
                    url="https://api.internationalshowtimes.com/v4/cinemas/" + item['cinema_id'],
                    headers={'X-API-Key': 'iBLYR2MIVfV8uZ3hSMdg2OJVmJpCnSp0'}, )
                cinema_data = cinema_responce.json()
                cinema = Cinema()
                cinema.cinema_id = item['cinema_id']
                cinema.name = cinema_data['cinema']['name']
                cinema.address = cinema_data['cinema']['location']['address']['display_text']
                cinema.save()
            seance = Seance()
            seance.film = film_object
            seance.cinema = cinema_object
            date = iso8601.parse_date(item['start_at'])
            seance.date = date.date()
            seance.time = date.time()
            seance.save()
            i += 1
        return HttpResponse(response.content)
    else:
        return HttpResponse('request error')
