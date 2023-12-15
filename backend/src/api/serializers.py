from rest_framework import serializers
from api.models import *

class GenreField(serializers.RelatedField):
    def to_representation(self, value):
        return value.name
    
    def to_internal_value(self, data):
        return Genre.objects.get_or_create(name=data)[0]


class CastSerializer(serializers.ModelSerializer):
    cast_type = serializers.ChoiceField(choices=Cast.TYPES)
    class Meta:
        model = Cast
        fields = "__all__"


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    media = serializers.PrimaryKeyRelatedField(queryset=Media.objects.all())
    datetime = serializers.ReadOnlyField()
    edited = serializers.ReadOnlyField()

    class Meta:
        model = Review
        fields = "__all__"


class MovieSerializer(serializers.ModelSerializer):
    crew = serializers.PrimaryKeyRelatedField(many=True, queryset=Cast.objects.all())
    avg_rating = serializers.ReadOnlyField()
    genre = GenreField(many=True, queryset=Genre.objects.all())
    previous_media = serializers.PrimaryKeyRelatedField(allow_null=True, queryset=Movie.objects.all())
    next_media = serializers.PrimaryKeyRelatedField(allow_null=True, queryset=Movie.objects.all())
    cover_image = serializers.CharField(allow_blank=True)
    
    class Meta:
        model = Movie
        fields = ['id', 'title', 'genre', 'cover_image', 'avg_rating',
                'next_media', 'previous_media', 'duration', 'release_date', 'crew']

    def create(self, validated_data):
        cast_data = validated_data.pop("crew")
        genre_data = validated_data.pop("genre")
        movie = Movie.objects.create(**validated_data)
        for c in cast_data:
            cast = Cast.objects.get_or_create(c.pk)
            movie.crew.add(cast)
        for genre in genre_data:
            movie.genre.add(genre)        
        movie.save()
        return movie
        
            

class EpisodeSerializer(serializers.ModelSerializer):
    crew = serializers.StringRelatedField(read_only=True, many=True)
    tv_show = serializers.StringRelatedField(source='show')
    season_num = serializers.SlugRelatedField(source='show',
                                              slug_field="season_num",
                                              queryset=Season.objects.all())
    season_title = serializers.StringRelatedField(source='show', read_only=True)
    avg_rating = serializers.ReadOnlyField()
    class Meta:
        model = Movie
        fields = ['id', 'title', 'genre', 'crew', 'cover_image', 'avg_rating',
                'next_media', 'previous_media', 'duration', 'release_date',
                'tv_show', 'season_num', 'season_title', 'episode_num']

class ShowSerializer(serializers.ModelSerializer):
    crew = serializers.StringRelatedField(read_only=True, many=True)
    episodes = serializers.StringRelatedField()
    season_num = serializers.SlugRelatedField(source='show',
                                              slug_field="season_num",
                                              queryset=Season.objects.all())
    season_title = serializers.StringRelatedField(source='show', read_only=True)
    avg_rating = serializers.ReadOnlyField()
    class Meta:
        model = Show
        fields = ['id', 'title', 'genre', 'crew', 'cover_image', 'avg_rating',
        'next_media', 'previous_media', 'release_date']



