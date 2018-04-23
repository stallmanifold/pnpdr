from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.reverse import reverse

from rollservice.models import DiceSequence
from rollservice.models import RollSequence
from rollservice.serializers import DiceSequenceSerializer
from rollservice.serializers import RollSequenceSerializer
from rollservice.serializers import UserSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'message': 'REST API routes',
        'users': reverse('user-list', request=request, format=format),
    })


class DiceSequenceList(generics.ListCreateAPIView):
    queryset = DiceSequence.objects.all()
    serializer_class = DiceSequenceSerializer


class RollSequenceList(generics.ListAPIView):
    queryset = RollSequence.objects.all()
    serializer_class = RollSequenceSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

