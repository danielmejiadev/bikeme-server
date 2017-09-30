from rest_framework import serializers
from Apps.BikeMe.models.problem_model import *


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ('id', 'user', 'description','date')
     
