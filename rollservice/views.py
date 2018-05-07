import coreapi
import coreschema
import uuid

from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import renderers
from rest_framework.reverse import reverse
from rest_framework import permissions
from rest_framework import status
from rest_framework.schemas import AutoSchema

from rollservice.models import DiceSequence
from rollservice.models import RollSequence
from rollservice.serializers import DiceSequenceData
from rollservice.serializers import DiceSequenceListByUUIDSerializer
from rollservice.serializers import DiceSequenceSerializer
from rollservice.serializers import RollSequenceSerializer
from rollservice.serializers import UserSerializer
from rollservice.permissions import IsOwnerOrReadOnly


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'message': 'REST API Routes',
        'users': reverse('user-list', request=request, format=format),
        'dice sequences': reverse('dice-seq', request=request, format=format),
        'rolls': reverse('roll-seq', request=request, format=format),
    })


class DiceSequenceByUUIDView(generics.RetrieveAPIView):
    queryset = DiceSequence.objects.all()
    serializer_class = DiceSequenceSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    lookup_field = 'uuid'

    def get(self, request, uuid, format=None):
        try:
            entry = self.get_queryset().get(uuid__exact=uuid)
        except DiceSequence.DoesNotExist:
            content = { 'uuid': uuid, 'message': 'Resource does not exist' }
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except:
            content = { 'uuid': uuid, 'message': 'Invalid UUID' }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        owner = entry.owner
        seq_name = entry.seq_name
        dice_sequence = [dice.sides for dice in entry.sequence.all()]
        data = DiceSequenceData(uuid, owner, seq_name, dice_sequence)

        serializer = DiceSequenceSerializer(data, context={'request': request})

        return Response(serializer.data)


class DiceSequenceListByUUIDView(generics.ListAPIView):
    queryset = DiceSequence.objects.all()
    serializer_class = DiceSequenceListByUUIDSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    schema = AutoSchema(manual_fields=[
        coreapi.Field(
            "uuid_list",
            required=True,
            location="form",
            schema=coreschema.Array(
                description=""
            ),
        )
    ])

    def get(self, request, *args, **kwargs):
        try:
            uuid_list = request.data['uuid_list']
        except:
            content = { 'message': 'Missing required parameters', 'missing parameters': ['uuid_list'] }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        uuid_list = [uuid.UUID(entry) for entry in uuid_list]
        entries_found = self.get_queryset().filter(uuid__in=uuid_list)
        uuids_found = [entry.uuid for entry in entries_found]
        uuids_missing = [entry for entry in uuid_list if entry not in uuids_found]
        data = (
            DiceSequenceData(
                entry.uuid, entry.seq_name, entry.owner, [dice.sides for dice in entry.sequence.all()]
            )
            for entry in entries_found
        )
        
        if (uuid_list != []) and (len(uuids_missing) == len(uuid_list)):
            content = { 'message': 'Not Found', 'uuids_missing': uuids_missing }
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        serializer = DiceSequenceSerializer(data, many=True, context={'request': request})

        content = { 'message': 'UUID Search Results', 'uuids_found': serializer.data, 'uuids_missing': uuids_missing }
        return Response(content)


class DiceSequenceListView(generics.ListCreateAPIView):
    queryset = DiceSequence.objects.all()
    serializer_class = DiceSequenceSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class RollSequenceListView(generics.ListAPIView):
    queryset = RollSequence.objects.all()
    serializer_class = RollSequenceSerializer


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

