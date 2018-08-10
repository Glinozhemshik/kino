from django.urls import path, re_path
from afisha import views, get_data

urlpatterns = [
    path('get_data', get_data.get_data),
    path('del_data', get_data.del_data),
    path('film/<int:film_id>', views.film_page, name='film_url'),
    re_path(r'^film/(?P<film_id>\d+)/(?P<date>\d+\-\d+\-\d+)$', views.film_page_date, name='film_date_url'),
    path('', views.list_page, name='home_url'),
]
