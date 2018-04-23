from rest_framework import serializers
from rollservice import DiceSequence, RollSequence
from django.contrib.auth.models import User


class DiceSequenceSerializer(serializers.HyperlinkedModelSerializer):
    dice_sequence = serializers.PrimaryKeyRelatedField(many=True, queryset=DiceSequence.objects.all())

    class Meta:
        model = rollservice.models.DiceSequence
        fields = ('url', 'id', 'username', 'dice_sequence')


class RollSequenceSerializer(serializers.HyperlinkedModelSerializer):
    roll_sequence = serializers.PrimaryKeyRelatedField(many=True, queryset=RollSequence.objects.all())

    class Meta:
        model = rollservice.models.RollSequence
        fields = ('url', 'id', 'username', 'roll_sequence')


