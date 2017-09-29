from django.db import models
from Apps.BikeMe.models.route_model import *
import uuid

class Event(models.Model):
	uid             = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name            = models.CharField(max_length=50)
	route           = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='events')
	date            = models.DateTimeField()
	
	class Meta:
		ordering = ('date',)