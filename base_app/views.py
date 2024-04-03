from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import CustomUser, Movie, Rating
from .serializers import CustomUserSerializer, MovieSerializer, RatingSerializer
from django.db.models import Avg
from rest_framework.decorators import api_view,action
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm



#for api view
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    

    @action(detail=True, methods=['post'])
    def rate_movie(self, request, pk=None):
        if 'rating' in request.data:
            movie = Movie.objects.get(id=pk)
            rating = request.data['rating']
            user = request.user
            try:
                rating_obj = Rating.objects.get(user=user.id, movie=movie.id)
                rating_obj.rating = rating
                rating_obj.save()
                serializer = RatingSerializer(rating_obj, many=False)
                response = {'message': 'Rating updated', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            except:
                rating_obj = Rating.objects.create(user=user, movie=movie, rating=rating)
                serializer = RatingSerializer(rating_obj, many=False)
                response = {'message': 'Rating created', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
        else:
            response = {'message': 'You need to provide a rating'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        


@api_view(['GET'])
def movie_detail(request, pk):
    try:
        movie = Movie.objects.get(pk=pk)
    except Movie.DoesNotExist:
        return Response({"message": "Movie does not exist"}, status=404)

    ratings = Rating.objects.filter(movie=movie)
    average_rating = ratings.aggregate(Avg('rating'))['rating__avg']

    serializer = MovieSerializer(movie)
    data = serializer.data
    data['average_rating'] = average_rating

    return Response(data)