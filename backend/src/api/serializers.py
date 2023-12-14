from rest_framework import serializers
from api.models import *

        
class MovieSerializer(serializers.ModelSerializer):
   # crew = serializers.StringRelatedField(many=True)
    avg_rating = serializers.ReadOnlyField()
    genre = serializers.StringRelatedField(many=True)
    class Meta:
        model = Movie
        fields = ['id', 'title', 'genre', 'cover_image', 'avg_rating',
                'next_media', 'previous_media', 'duration', 'release_date']


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


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class CastSerializer(serializers.ModelSerializer):
    cast_type = serializers.ChoiceField(choices=Cast.TYPES)
    class Meta:
        model = Cast
        fields = "__all__"