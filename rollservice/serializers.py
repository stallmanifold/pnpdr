from rest_framework import serializers
from rest_framework.reverse import reverse
from rollservice.models import Dice, DiceSequence, RollSequence
from django.contrib.auth.models import User


class DiceSequenceByUUIDSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    dice_sequence = serializers.ReadOnlyField()

    class Meta:
        model = DiceSequence
        fields = ('uuid', 'dice_sequence')

    def get(self, validated_data):
        uuid = validated_data['uuid']
        dice_sequence = DiceSequence.objects.filter(uuid=uuid).first()

        self.uuid = uuid
        self.dice_sequence = dice_sequence

        return self


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
        dice_saved = []
        for value in values:
            dice_saved.append(Dice.objects.create(sides=value))

        dice_sequence = DiceSequence.objects.create(seq_name=seq_name, owner=owner)
        dice_sequence.sequence.set(dice_saved)
        uuid = dice_sequence.uuid

        self.owner = owner
        self.seq_name = seq_name
        self.dice_sequence = values
        self.uuid = uuid

        return self


class RollSequenceSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    roll_sequence = serializers.HyperlinkedIdentityField(many=True, view_name='roll-seq', read_only=True)

    class Meta:
        model = RollSequence
        fields = ('url', 'id', 'owner', 'roll_sequence')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    dice_sequence = serializers.HyperlinkedIdentityField(many=True, view_name='dice-seq', read_only=True)

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

