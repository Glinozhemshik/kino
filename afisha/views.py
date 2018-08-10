import json
import datetime
from django.shortcuts import render, get_object_or_404
from .models import *



def list_page(request):
	return render(request, 'index.html', {'all': Film.objects.all()})


def film_page_date(request, film_id, date):
	date = datetime.datetime.strptime(date, '%Y-%m-%d')
	context = {}
	film = get_object_or_404(Film, id=film_id)

	context['cinemas'] = []
	for cinema in Cinema.objects.all():
		array = []
		for item in Seance.objects.filter(cinema=cinema, date=date, film=film).order_by('time'):
			array.append(item)
		if len(array) != 0:
			context['cinemas'].append({'cinema': cinema, 'seances': array})

	genres = []
	if film.genres:
		film.genres = str.replace(film.genres,"\'", "\"")
		for item in json.loads(film.genres):
			genres.append(item['name'])
		context['genres'] = genres
	context['runtime'] = film.runtime
	context['date'] = date
	context['film'] = film
	context['dates'] = []
	for i in range(0, 7):
		if film.seances.filter(date=(datetime.date.today() + datetime.timedelta(days=i))).count() > 0:
			context['dates'].append(datetime.date.today() + datetime.timedelta(days=i))

	context['seances'] = Seance.objects.filter(film=film, date=date)
	return render(request, 'afisha/film_page.html', context)


def film_page(request, film_id):
	return film_page_date(request, film_id, str(datetime.date.today()))
