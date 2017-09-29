from django.db import models
from Apps.BikeMe.models.route_model import *
from Apps.BikeMe.models.user_model import *

class Rating(models.Model):
    user             = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    route            = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='ratings')
    calification     = models.FloatField()
    recommendation   = models.FloatField()
    date             = models.CharField(max_length=100)

    class Meta:
        ordering = ('route',)
        