from rest_framework import serializers
from rollservice.models import DiceSequence, RollSequence
from django.contrib.auth.models import User


class DiceSequenceSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    dice_sequence = serializers.PrimaryKeyRelatedField(many=True, queryset=DiceSequence.objects.all())

    class Meta:
        model = DiceSequence
        fields = ('url', 'id', 'owner', 'dice_sequence')


class RollSequenceSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    roll_sequence = serializers.PrimaryKeyRelatedField(many=True, queryset=RollSequence.objects.all())

    class Meta:
        model = RollSequence
        fields = ('url', 'id', 'owner', 'roll_sequence')


class UserSerializer(serializers.ModelSerializer):
    dice_sequence = serializers.PrimaryKeyRelatedField(many=True, queryset=DiceSequence.objects.all())

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'dice_sequence')


class HistorySerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    roll_sequence = serializers.PrimaryKeyRelatedField(many=True, queryset=RollSequence.objects.all())
    dice_sequence = serializers.PrimaryKeyRelatedField(many=True, queryset=DiceSequence.objects.all())

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'dice_sequence', 'roll_sequence')

