from rest_framework import serializers
from admin_app.models import Movie
from admin_app.models import Watchlist
from admin_app.models import WatchHistory

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'




class WatchlistSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)

    class Meta:
        model = Watchlist
        fields = ['id', 'movie']
        

class WatchHistorySerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)

    class Meta:
        model = WatchHistory
        fields = ['id', 'movie', 'watched_at']