from rest_framework import serializers
from .models import CustomUser, Movie, Rating
from django.db.models import Avg

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone']

class MovieSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['id', 'name', 'genre', 'ratings', 'release_date', 'average_rating']

    def get_average_rating(self, obj):
        ratings = Rating.objects.filter(movie=obj)
        return ratings.aggregate(Avg('rating'))['rating__avg']
    


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'