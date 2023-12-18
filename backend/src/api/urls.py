from django.urls import path

from . import views

urlpatterns = [
    path('movies/', views.movies, name='api-movies'),
    path('movies/<int:pk>', views.movie, name='api-movie'),
    path('shows/', views.shows, name='api-shows'),
    path('shows/<int:pk>', views.show, name='api-show'),
    path('shows/<int:pk>/seasons', views.season, name='api-show-seasons'),
    path('episodes/', views.episodes, name='api-episodes'),
    path('episodes/<int:pk>', views.episode, name='api-episode'),
    path('seasons/', views.seasons, name='api-seasons'),
    path('seasons/<int:pk>', views.season, name='api-season'),
    path('movies/<int:pk>/reviews', views.reviews, name='api-reviews'),
    path('movies/<int:pk>/review/<int:review_pk>', views.movie, name='api-review'),
    path('genres/', views.genres, name='api-genres'),
    path('genres/<int:pk>', views.genre, name='api-genre'),
    path('cast/', views.all_cast, name='api-all_cast'),
    path('cast/<int:pk>', views.cast, name='api-cast'),
]