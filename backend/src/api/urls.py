from django.urls import path

from . import views

urlpatterns = [
    path('movies/', views.movies, name='api-movies'),
    path('movies/<int:pk>', views.movie, name='api-movie'),
    path('genres/', views.genres, name='api-genres'),
    path('genres/<int:pk>', views.genre, name='api-genre'),
    path('cast/', views.all_cast, name='api-all_cast'),
    path('cast/<int:pk>', views.cast, name='api-cast')
]