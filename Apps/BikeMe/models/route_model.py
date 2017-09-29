from django.db import models
from Apps.BikeMe.models.user_model import *
import uuid
import numpy as np
import math
from numpy.core.umath_tests import inner1d
from pyproj import Geod

class Route(models.Model):
    uid             = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator         = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_routes')
    name            = models.CharField(max_length=20)
    description     = models.CharField(max_length=200)
    distance        = models.FloatField()
    level           = models.IntegerField()
    image           = models.TextField()
    departure       = models.TextField()
    arrival         = models.TextField()
    created         = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ('created',)

    @staticmethod
    def geoDistance(point1,point2):
        wgs84_geod = Geod(ellps='WGS84')
        lat1, lon1 = (point1.latitude, point1.longitude)
        lat2, lon2 = (point2.latitude, point2.longitude)
        az12,az21,distanceInMeters = wgs84_geod.inv(lon1,lat1,lon2,lat2)
        return distanceInMeters

    @staticmethod
    def _c(ca,i,j,pointsRoute1,pointsRoute2):
        if ca[i,j] > -1:
            return ca[i,j]
        elif i == 0 and j == 0:
            ca[i,j] = Route.geoDistance(pointsRoute1[0],pointsRoute2[0])
        elif i > 0 and j == 0:
            ca[i,j] = max(Route._c(ca,i-1,0,pointsRoute1,pointsRoute2),Route.geoDistance(pointsRoute1[i],pointsRoute2[0]))
        elif i == 0 and j > 0:
            ca[i,j] = max(Route._c(ca,0,j-1,pointsRoute1,pointsRoute2),Route.geoDistance(pointsRoute1[0],pointsRoute2[j]))
        elif i > 0 and j > 0:
            ca[i,j] = max(min(Route._c(ca,i-1,j,pointsRoute1,pointsRoute2),Route._c(ca,i-1,j-1,pointsRoute1,pointsRoute2),Route._c(ca,i,j-1,pointsRoute1,pointsRoute2)),Route.geoDistance(pointsRoute1[i],pointsRoute2[j]))
        else:
            ca[i,j] = float("inf")
        return ca[i,j]

    @staticmethod
    def frechetDist(pointsRoute1, pointsRoute2):
        ca = np.ones((len(pointsRoute1),len(pointsRoute2)))
        ca = np.multiply(ca,-1)
        return (Route._c(ca,len(pointsRoute1)-1,len(pointsRoute2)-1,pointsRoute1,pointsRoute2))

  
    @staticmethod
    def exist(pointsToValidate, distanceToValidate):
        for route in Route.objects.all():
            routePoints = route.points.all()
            
            if(Route.similarity(math.fabs(route.distance-distanceToValidate)) >= 0.3):
                pointBeginToValidate=pointsToValidate[0]
                pointBeginRoute=routePoints[0]
                
                if(Route.similarity(Route.geoDistance(pointBeginRoute, pointBeginToValidate)) >=0.75):
                    pointEndToValidate=pointsToValidate[len(pointsToValidate)-1]
                    pointEndRoute=routePoints[len(routePoints)-1]
                    
                    if(Route.similarity(Route.geoDistance(pointEndRoute, pointEndToValidate)) >=0.75):
                        distanceInMeters = Route.frechetDist(pointsToValidate, routePoints)
                        
                        if(Route.similarity(distanceInMeters) >= 0.75):
                            return True

                    else:
                        return False
                else:
                    return False
            else:
                return False
        
        return False

    @staticmethod
    def similarity(value):
        return 1/(1+(value/1000))


