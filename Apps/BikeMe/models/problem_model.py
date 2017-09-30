from django.db import models
from Apps.BikeMe.models.user_model import *

class Problem(models.Model):
	
    user             = models.ForeignKey(User, on_delete=models.CASCADE, related_name='problems')
    description 	 = models.TextField()
    date             = models.CharField(max_length=100)

    class Meta:
        ordering = ('date',)