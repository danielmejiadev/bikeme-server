from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Apps.BikeMe.models.user_model import *
from Apps.BikeMe.serializers.user_serializer import *
from Apps.BikeMe.serializers.workout_serializer import *

@api_view(['POST'])
def createUser(request):
    if request.method == 'POST':
        try:
            user = User.objects.get(uid=request.data.get("uid"))
        except User.DoesNotExist:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def updateUser(request,pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)    
    if request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def createWorkouts(request):
    if request.method == 'POST':
        serializer = WorkoutSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

