from rest_framework import serializers
from Apps.BikeMe.models.rating_model import *

#Used when create ratings alone
class RatingSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id','user', 'route', 'calification','recommendation','date')
       
     
    def create(self, validated_data):
        try:
            rating = Rating.objects.get(user=validated_data.get('user'), route=validated_data.get('route'))
        except Rating.DoesNotExist:
            return Rating.objects.create(**validated_data)

        dateRemote = validated_data.get('date')
        calificationRemote = validated_data.get('calification')
        recommendationRemote = validated_data.get('recommendation')

        dateRemoteUpdatedAfterLocal = dateRemote > rating.date
        isRatingLocalRecommendation = (rating.calification == 0 and rating.recommendation > 0)
        isRatingRemoteCalification = ( calificationRemote >= 0 and recommendationRemote == 0)

        if( dateRemoteUpdatedAfterLocal or (isRatingLocalRecommendation and isRatingRemoteCalification) ):
            rating.calification = calificationRemote
            rating.recommendation = recommendationRemote
            rating.date = dateRemote
            rating.save()    
        return rating


#route only used when show ratings but no when create or update
class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id','user', 'route','calification','recommendation','date')
        extra_kwargs = {
                'route': {
                    "read_only": True,
                 }
            }