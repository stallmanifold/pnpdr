from rest_framework import serializers
import rollservice.models
from django.contrib.auth.models import User


class DiceSequenceSerializer(serializers.HyperlinkedModelSerializer):
    die_sequence = serializers.PrimaryKeyRelatedField(many=True, queryset=DieSequence.objects.all())

    class Meta:
        model = rollservice.models.DiceSequence
        fields = ('url', 'id', 'username', 'dice_sequence')


class RollSequenceSerializer(serializers.HyperlinkedModelSerializer):
    roll_sequence = serializers.PrimaryKeyRelatedField(many=True, queryset=RollSequence.objects.all())

    class Meta:
        model = rollservice.models.RollSequence
        fields = ('url', 'id', 'username', 'roll_sequence')


