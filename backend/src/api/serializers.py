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
    crew = serializers.PrimaryKeyRelatedField(many=True, queryset=Cast.objects.all())
    tv_show = serializers.PrimaryKeyRelatedField(queryset=Show.objects.all())
    genre = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Genre.objects.all())
    season_num = serializers.SlugRelatedField(source='season',
                                              slug_field="season_num",
                                              read_only=True)
    season_title = serializers.SlugRelatedField(source='season',
                                              slug_field="title",
                                              read_only=True)
    season_id = serializers.PrimaryKeyRelatedField(source="season", queryset=Season.objects.all())
    avg_rating = serializers.ReadOnlyField()
    cover_image = serializers.CharField(allow_blank=True)
    previous_media = serializers.PrimaryKeyRelatedField(allow_null=True, queryset=Show.objects.all())
    next_media = serializers.PrimaryKeyRelatedField(allow_null=True, queryset=Show.objects.all())
    
    class Meta:
        model = Episode
        fields = ['id', 'title', 'genre', 'crew', 'cover_image', 'avg_rating',
                'next_media', 'previous_media', 'duration', 'release_date',
                'tv_show', 'season_num', 'season_title', 'season_id','episode_num']


class ShowSerializer(serializers.ModelSerializer):
    crew = serializers.PrimaryKeyRelatedField(many=True, queryset=Cast.objects.all())
    episodes = serializers.StringRelatedField(many=True, allow_null=True)
    num_seasons = serializers.ReadOnlyField()
    num_episodes = serializers.ReadOnlyField()
    avg_rating = serializers.ReadOnlyField()
    genre = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Genre.objects.all())
    cover_image = serializers.CharField(allow_blank=True)
    previous_media = serializers.PrimaryKeyRelatedField(allow_null=True, queryset=Show.objects.all())
    next_media = serializers.PrimaryKeyRelatedField(allow_null=True, queryset=Show.objects.all())
    
    class Meta:
        model = Show
        fields = ['id', 'title', 'genre', 'crew', 'num_seasons', 'num_episodes', 'episodes',
                  'cover_image', 'avg_rating', 'next_media', 'previous_media', 'release_date']



class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = "__all__"
