from rest_framework import serializers
from Apps.BikeMe.models.challenge_model import *


class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = ('uid', 'typeChallenge', 'condition', 'award')