"""
URL configuration for movie_rating project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from base_app.views import CustomUserViewSet, MovieViewSet, RatingViewSet,movie_detail
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns


router = routers.DefaultRouter()
router.register('users', CustomUserViewSet, basename='users')
router.register('movies', MovieViewSet, basename='movies')
router.register('ratings', RatingViewSet, basename='ratings')

urlpatterns = [
    #this is for api
    path('api/', include(router.urls)),
    path('api/movies/<int:pk>/', movie_detail, name='movie-detail'),
]

#urlpatterns += staticfiles_urlpatterns()