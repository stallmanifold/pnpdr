from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics

from rollservice.models import DiceSequence
from rollservice.models import RollSequence
from rollservice.serializers import DiceSequenceSerializer
from rollservice.serializers import RollSequenceSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'message': 'REST API routes',
    })


class DiceSequenceList(generics.ListCreateAPIView):
    queryset = DiceSequence.objects.all()
    serializer_class = DiceSequenceSerializer


class RollSequenceList(generics.ListAPIView):
    queryset = RollSequence.objects.all()
    serializer_class = RollSequenceSerializer

