from django.db import models


class Film(models.Model):
    name = models.CharField("Название", max_length=200, null=True, default=None)
    about = models.CharField("Описание", max_length=1000, null=True, default=None)
    poster_url = models.URLField("Постер", null=True, default=None)
    movie_id = models.IntegerField("ID", default=0)
    trailer_url = models.URLField("Трейлер", null=True, default=None)
    genres = models.CharField("Жанры", max_length=1000, null=True, default=None)
    runtime = models.IntegerField("Продолжительность", default=None, null=True)
    rating = models.CharField("Рейтинг", max_length=50, null=True)


class Cinema(models.Model):
    name = models.CharField("Название", max_length=200, null=True, default=None)
    address = models.CharField("Адресс", max_length=200, null=True, default=None)
    cinema_id = models.IntegerField(default=0)


class Seance(models.Model):
    film = models.ForeignKey(Film, verbose_name="Фильм", on_delete=models.CASCADE, related_name='seances')
    cinema = models.ForeignKey(Cinema, verbose_name="Кинотеатр", on_delete=models.CASCADE, related_name='seances')
    time = models.TimeField("Время", null=True, default=None)
    date = models.DateField("Дата", null=True, default=None)
