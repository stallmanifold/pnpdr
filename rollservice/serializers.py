from rest_framework import serializers
from rest_framework.reverse import reverse
from rollservice.models import Dice, DiceSequence, RollSequence
from django.contrib.auth.models import User


class DiceSequenceData:
    def __init__(self, uuid, owner, seq_name, dice_sequence):
        self.uuid = uuid
        self.owner = owner
        self.seq_name = seq_name
        self.dice_sequence = dice_sequence


class DiceSequenceByUUIDSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    owner = serializers.ReadOnlyField(source='owner.username')
    seq_name = serializers.CharField(max_length=256)
    dice_sequence = serializers.ListField(child=serializers.IntegerField())

    class Meta:
        model = DiceSequence
        fields = ('uuid', 'owner', 'seq_name', 'dice_sequence')


class DiceSequenceSerializer(serializers.Serializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    seq_name = serializers.CharField(max_length=256)
    dice_sequence = serializers.ListField(child=serializers.IntegerField())
    uuid = serializers.ReadOnlyField()
    url = serializers.HyperlinkedIdentityField(lookup_field='uuid', view_name='dice-seq-by-uuid')

    class Meta:
        model = DiceSequence
        fields = ('url', 'uuid', 'owner', 'seq_name', 'dice_sequence')


    def create(self, validated_data):
        seq_name = validated_data.get('seq_name', None)
        owner = self.context['request'].user
        values = validated_data.get('dice_sequence')
        dice_saved = [Dice.objects.create(sides=value) for value in values]

        dice_sequence = DiceSequence.objects.create(seq_name=seq_name, owner=owner)
        dice_sequence.sequence.set(dice_saved)
        uuid = dice_sequence.uuid

        return DiceSequenceData(uuid, owner, seq_name, values)


class RollSequenceSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    roll_sequence = serializers.HyperlinkedIdentityField(many=True, view_name='roll-seq', read_only=True)

    class Meta:
        model = RollSequence
        fields = ('url', 'id', 'owner', 'roll_sequence')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    dice_sequence = serializers.HyperlinkedIdentityField(many=True, view_name='dice-seq-by-uuid', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'dice_sequence')


class HistorySerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    roll_sequence = serializers.HyperlinkedIdentityField(many=True, view_name='roll-seq', read_only=True)
    dice_sequence = serializers.HyperlinkedIdentityField(many=True, view_name='dice-seq', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'dice_sequence', 'roll_sequence')

