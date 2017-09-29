from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Apps.BikeMe.models.user_model import *
from Apps.BikeMe.models.workout_model import *
from Apps.BikeMe.models.route_model import *
from Apps.BikeMe.models.rating_model import *
from Apps.BikeMe.models.event_model import *
from Apps.BikeMe.models.guest_model import *
from Apps.BikeMe.models.challenge_model import *

from Apps.BikeMe.serializers.user_serializer import *
from Apps.BikeMe.serializers.workout_serializer import *
from Apps.BikeMe.serializers.route_serializer import *
from Apps.BikeMe.serializers.rating_serializer import *
from Apps.BikeMe.serializers.event_serializer import *
from Apps.BikeMe.serializers.guest_serializer import *
from Apps.BikeMe.serializers.challenge_serializer import *
import datetime



@api_view(['GET'])
def getAllData(request):
    if request.method == 'GET':
        users = User.objects.all()
        workouts = Workout.objects.all()
        routes = Route.objects.all()
        ratings = Rating.objects.all()
        events = Event.objects.all()
        guests = Guest.objects.all()
        challenges = Challenge.objects.all()

        serverDate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        serializerUser = UserSerializer(users, many=True)
        serializerWorkout = WorkoutSerializer(workouts,many=True)
        serializerRoute = RouteSerializerToShow(routes, many=True)
        serializerRating = RatingSerializer(ratings, many=True)
        serializerEvent = EventSerializer(events, many=True)
        serializerGuest = GuestSerializer(guests, many=True)
        serializerChallenge = ChallengeSerializer(challenges, many=True)

        
        return Response({
            'users':serializerUser.data, 
            'workouts':serializerWorkout.data, 
            'routes': serializerRoute.data, 
            'ratings': serializerRating.data,
            'events': serializerEvent.data,
            'guests': serializerGuest.data,
            'challenges': serializerChallenge.data,
            'serverDate' : serverDate
            })