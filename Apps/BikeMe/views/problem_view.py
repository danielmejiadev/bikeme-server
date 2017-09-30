from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Apps.BikeMe.serializers.problem_serializer import *

@api_view(['POST'])
def createProblems(request):
    if request.method == 'POST':
        serializer = ProblemSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)