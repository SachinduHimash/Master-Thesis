from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Convo
from .serializer import ConvoSerializer
from .fuzzySystem import checkValues
from .chatAgent import handle_conversation

# Create your views here.
@api_view(['GET'])
def get_convo(request):
    convo = Convo.objects.all()
    serializedData = ConvoSerializer(convo, many=True).data
    return Response(serializedData)

@api_view(['POST'])
def get_values(request):
    data = request.data
    serializer = ConvoSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        responseData = checkValues(data)
        print (responseData)
        return Response(responseData, status= status.HTTP_200_OK)
    return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def chat_agent(request):
    data = request.data
    serializer = ConvoSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        responseData = handle_conversation(data)
        return Response(responseData, status= status.HTTP_200_OK)
    return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)