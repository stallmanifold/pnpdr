import uuid
from django.db import models


class Dice(models.Model):
    sides = models.PositiveIntegerField()


class Roll(models.Model):
    roll = models.PositiveIntegerField()


class DiceSequence(models.Model):
    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=True, unique=True)
    seq_name = models.CharField(max_length=256)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User',  related_name='dice_sequence', on_delete=models.CASCADE)
    sequence = models.ManyToManyField(Dice)


class RollSequence(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='roll_sequence', on_delete=models.CASCADE)
    roll_sequence = models.ManyToManyField(Roll)
    dice_sequence = models.ForeignKey(DiceSequence, related_name='+', on_delete=models.PROTECT)

    class Meta:
        ordering = ('created',)

