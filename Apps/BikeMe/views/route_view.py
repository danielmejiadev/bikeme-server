from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Apps.BikeMe.serializers.route_serializer import *
from Apps.BikeMe.serializers.rating_serializer import *
import numpy as np


#Route and status 201 Created when route was created
#Existing Route and Status 202 when route already exist
#List of errros and status 400 when someone error was found
@api_view(['Post'])
def createRoute(request):
    if request.method == 'POST':
        serializer = RouteSerializerCreate(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Return 1 if the route  already exist
#Return 0 if the route do not exist
@api_view(['Post'])
def isRouteValid(request):
    if request.method == 'POST':
        pointsToValidate = np.array([])
        for point in request.data:
            pointsToValidate = np.append(pointsToValidate, Point(latitude=point.get("latitude"), longitude=point.get("longitude")))
        if(Route.exist(pointsToValidate, float(request.GET.get("distance")))):
            return Response(1)
        else:
            return Response(0)


@api_view(['POST'])
def createRatings(request):
    if request.method == 'POST':
        serializer = RatingSerializerCreate(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


