from rest_framework import serializers
from rollservice.models import DiceSequence, RollSequence
from django.contrib.auth.models import User


class DiceSequenceSerializer(serializers.HyperlinkedModelSerializer):
    dice_sequence = serializers.PrimaryKeyRelatedField(many=True, queryset=DiceSequence.objects.all())

    class Meta:
        model = DiceSequence
        fields = ('url', 'id', 'username', 'dice_sequence')


class RollSequenceSerializer(serializers.HyperlinkedModelSerializer):
    roll_sequence = serializers.PrimaryKeyRelatedField(many=True, queryset=RollSequence.objects.all())

    class Meta:
        model = RollSequence
        fields = ('url', 'id', 'username', 'roll_sequence')


