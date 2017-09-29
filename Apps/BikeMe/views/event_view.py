from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Apps.BikeMe.serializers.guest_serializer import *
import numpy as np


#Used for when user change state of guest in the event
@api_view(['POST'])
def createGuests(request):
    if request.method == 'POST':
        serializer = GuestSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)