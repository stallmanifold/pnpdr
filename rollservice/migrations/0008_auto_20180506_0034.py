# Generated by Django 2.0.4 on 2018-05-06 00:34

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('rollservice', '0007_auto_20180506_0013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dicesequence',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]