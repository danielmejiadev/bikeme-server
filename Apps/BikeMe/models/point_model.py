from django.db import models
import uuid
from Apps.BikeMe.models.route_model import Route

class Point(models.Model):
	route       = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='points')
	latitude    = models.FloatField()
	longitude   = models.FloatField()

	class Meta:
		ordering = ('route','id')
