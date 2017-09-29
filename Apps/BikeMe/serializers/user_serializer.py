from rest_framework import serializers
from Apps.BikeMe.models.user_model import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('uid','displayName','photo','email','level','aboutMe','socialNetworks','preferenceDays','preferenceHours', 'achievements', 'updated','created')
        extra_kwargs = {
                'photo': {
                    "allow_blank": True,
                 },
                'aboutMe': {
                    "allow_blank": True,
                 }
            }
        

    def update(self, instance, validated_data):
        if(validated_data.get('updated') > instance.updated):
            instance.displayName = validated_data.get('displayName')
            instance.email = validated_data.get('email')
            instance.level = validated_data.get('level')
            instance.photo = validated_data.get('photo')
            instance.aboutMe = validated_data.get('aboutMe')
            instance.socialNetworks = validated_data.get('socialNetworks')
            instance.preferenceDays = validated_data.get('preferenceDays')
            instance.preferenceHours = validated_data.get('preferenceHours')
            instance.achievements = validated_data.get('achievements')
            instance.updated = validated_data.get('updated')
            instance.save()

        return instance
            