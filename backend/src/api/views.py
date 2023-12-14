from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import *
from .serializers import *

class MoviesList(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

movies = MoviesList.as_view()


class MovieDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

movie = MovieDetail.as_view()


class GenresList(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

genres = GenresList.as_view()


class GenresDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

genre = GenresDetail.as_view()


class CastList(generics.ListCreateAPIView):
    queryset = Cast.objects.all()
    serializer_class = CastSerializer

all_cast = CastList.as_view()


class CastDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cast.objects.all()
    serializer_class = CastSerializer

cast = CastDetail.as_view()