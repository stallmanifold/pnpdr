from rest_framework import serializers
from rollservice.models import Dice, DiceSequence, RollSequence
from django.contrib.auth.models import User


class DiceSequenceSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    seq_name = serializers.CharField(max_length=256)
    dice_sequence = serializers.ListField(child=serializers.IntegerField())

    def create(self, validated_data):
        seq_name = validated_data.get('seq_name', None)
        owner = validated_data.get('owner', None)

        values = validated_data.get('dice_sequence')
        dice_saved = []
        for value in values:
            dice_saved.append(Dice(sides=value))
        
        dice_list = Dice.objects.bulk_create(dice_saved)
        dice_sequence = DiceSequence.objects.create(seq_name=seq_name, owner=owner)
        dice_sequence.related_set.set(dice_list)

        return dice_sequence


    class Meta:
        model = DiceSequence
        fields = ('url', 'id', 'owner', 'seq_name', 'dice_sequence')


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

