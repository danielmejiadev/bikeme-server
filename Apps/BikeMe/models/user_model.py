from django.db import models
from Apps.BikeMe.bikemeutils import BikeMeUtils

def getCurrentDate():
    pass

class User(models.Model):
    uid             = models.CharField(max_length=250, primary_key=True)
    displayName     = models.CharField(max_length=100)
    email           = models.EmailField()
    level           = models.IntegerField(default=0)
    photo           = models.TextField(default="")
    aboutMe         = models.TextField(default="")
    socialNetworks  = models.TextField(default="{"+"}")
    preferenceDays  = models.CharField(default="[]",max_length=100) 
    preferenceHours = models.CharField(default="[]",max_length=100) 
    achievements    = models.TextField(default="[]") 
    updated         = models.CharField(default=BikeMeUtils.getCurrentDateString,max_length=100)
    created   	    = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ('created',)
