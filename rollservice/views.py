from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import renderers
from rest_framework.reverse import reverse
from rest_framework import permissions

from rollservice.models import DiceSequence
from rollservice.models import RollSequence
from rollservice.serializers import DiceSequenceSerializer
from rollservice.serializers import DiceSequenceByUUIDSerializer
from rollservice.serializers import RollSequenceSerializer
from rollservice.serializers import UserSerializer
from rollservice.permissions import IsOwnerOrReadOnly


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'message': 'REST API routes',
        'users': reverse('user-list', request=request, format=format),
        'dice sequences': reverse('dice-seq', request=request, format=format),
        'rolls': reverse('roll-seq', request=request, format=format),
    })

class DiceSequenceData:
    def __init__(self, uuid, owner, seq_name, dice_sequence):
        self.uuid = uuid
        self.owner = owner
        self.seq_name = seq_name
        self.dice_sequence = dice_sequence


class DiceSequenceByUUID(generics.RetrieveAPIView):
    queryset = DiceSequence.objects.all()
    serializer_class = DiceSequenceByUUIDSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    lookup_field = 'uuid'

    def get(self, request, uuid, format=None):
        entry = self.get_queryset().get(uuid__exact=uuid)
        owner = entry.owner
        seq_name = entry.seq_name
        dice_sequence = [dice.sides for dice in entry.sequence.all()]
        data = DiceSequenceData(uuid, owner, seq_name, dice_sequence)
        serializer = DiceSequenceByUUIDSerializer(data)

        return Response(serializer.data)


class DiceSequenceList(generics.ListCreateAPIView):
    queryset = DiceSequence.objects.all()
    serializer_class = DiceSequenceSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class RollSequenceList(generics.ListAPIView):
    queryset = RollSequence.objects.all()
    serializer_class = RollSequenceSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

