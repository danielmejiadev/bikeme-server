from rest_framework import serializers
from Apps.RoutesApp.models import *


class RatingSerializer(serializers.ModelSerializer):
	class Meta:
	   model = Rating
	   fields = ('id', 'user', 'route', 'calification','recomendation')


class RatingForUserSerializer(serializers.ModelSerializer):
	class Meta:
	   model = Rating
	   fields = ('id', 'route', 'calification','recomendation')


class RatingForRouteSerializer(serializers.ModelSerializer):
	class Meta:
	   model = Rating
	   fields = ('id', 'user', 'calification','recomendation')


class UserSerializer(serializers.ModelSerializer):
	ratings = RatingForRouteSerializer(many=True,read_only=True)
	class Meta:
		model = Route
		fields = ('id', 'name', 'description', 'distance', 'level', 'average_ratings', 'ratings')

class UserSerializer(serializers.ModelSerializer):
	ratings = RatingForUserSerializer(many=True,read_only=True)
	class Meta:
		model = User
		fields = ('id', 'name', 'last_name', 'level', 'email', 'password', 'ratings')



