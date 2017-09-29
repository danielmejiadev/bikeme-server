from django.db import models
from Apps.BikeMe.models.user_model import *

class Workout(models.Model):
    uid                   = models.CharField(max_length=250, primary_key=True)
    name                  = models.CharField(max_length=250)
    user                  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workouts')
    durationSeconds       = models.IntegerField()
    beginDate             = models.CharField(max_length=100)
    comment               = models.TextField(default="")
    routeLatLngList       = models.TextField()
    totalDistanceMeters   = models.IntegerField()
    averageSpeedKm        = models.IntegerField()
    averageAltitudeMeters = models.IntegerField()
    typeRoute             = models.IntegerField()

    class Meta:
        ordering = ('beginDate',)