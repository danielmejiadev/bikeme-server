from rest_framework import serializers
from Apps.BikeMe.models.workout_model import Workout


class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ('uid', 'name', 'user', 'beginDate', 'durationSeconds', 'comment', 'routeLatLngList', 'totalDistanceMeters','averageSpeedKm', 'averageAltitudeMeters', 'typeRoute')
        extra_kwargs = {
                'comment': {
                    "allow_blank": True,
                 }
            }