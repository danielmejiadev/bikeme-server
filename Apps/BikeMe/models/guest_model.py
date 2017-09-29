from django.db import models
from Apps.BikeMe.models.user_model import *
from Apps.BikeMe.models.event_model import *

class Guest(models.Model):
    user             = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invitations')
    event            = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='guests')
    state 			 = models.IntegerField(default=0)
    date             = models.CharField(max_length=100)

    class Meta:
        ordering = ('event',)
