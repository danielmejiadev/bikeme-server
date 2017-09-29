from rest_framework import serializers
from Apps.BikeMe.serializers.guest_serializer import *


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('uid', 'name', 'route', 'date')