from rest_framework import serializers
from Apps.BikeMe.models.guest_model import *


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ('id','user', 'event', 'state','date')

    def create(self, validated_data):
        try:
            guest = Guest.objects.get(user=validated_data.get('user'), event=validated_data.get('event'))
        except Guest.DoesNotExist:
            return Guest.objects.create(**validated_data)

        if(validated_data.get('date') > guest.date):
            guest.state = validated_data.get('state')
            guest.save()    
        return guest
     