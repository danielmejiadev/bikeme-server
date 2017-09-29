from rest_framework import serializers
from Apps.BikeMe.serializers.rating_serializer import *
from Apps.BikeMe.serializers.point_serializer import *

#Used when a list of routes is shown
class RouteSerializerToShow(serializers.ModelSerializer):
    points = PointSerializer(many=True) 
    class Meta:
        model = Route
        fields = ('uid', 'creator', 'name', 'description', 'distance', 'level', 'image','departure', 'arrival', 'created', 'points')


#Used when a route is created 
class RouteSerializerCreate(serializers.ModelSerializer):
    ratings = RatingSerializer(many=True)
    points = PointSerializer(many=True) 
    class Meta:
        model = Route
        fields = ('uid', 'creator', 'name', 'description', 'distance', 'level', 'image','departure', 'arrival', 'created', 'points', 'ratings')
        
    def create(self, validated_data):
        routeName = validated_data.get('name')
        routeCreator = validated_data.get('creator')
        routeDescription = validated_data.get('description')
        routeDistance = validated_data.get('distance')
        routeDeparture = validated_data.get('departure')
        routeArrival = validated_data.get('arrival')
        routeLevel =  validated_data.get('level')
        routeImage = validated_data.get('image')
        
        points_data = validated_data.pop('points')
        ratings_data = validated_data.pop('ratings')
        route, created = Route.objects.get_or_create( name=routeName, 
                                                      creator=routeCreator, 
                                                      description=routeDescription, 
                                                      distance=routeDistance, 
                                                      departure=routeDeparture, 
                                                      arrival=routeArrival, 
                                                      level=routeLevel, 
                                                      image=routeImage)
        if created:
            for rating_data in ratings_data:
                user = rating_data.get('user')
                Rating.objects.create(route=route,calification=rating_data.get('calification'),recommendation=rating_data.get('recommendation'),date=rating_data.get('date'),user=user)
            
            for point_data in points_data:
                Point.objects.create(route=route,longitude=point_data.get('longitude'),latitude=point_data.get('latitude'))

        return route
