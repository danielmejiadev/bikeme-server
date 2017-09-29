from rest_framework import serializers
from Apps.BikeMe.models.point_model import *

#route only used when show points but no when create or update
class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = ('id','latitude','longitude', 'route')
        extra_kwargs = {
                'route': {
                    "read_only": True,
                 }
            }