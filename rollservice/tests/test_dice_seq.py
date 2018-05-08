from django.contrib.auth.models import User

from rollservice.models import DiceSequence

import rest_framework.test    as rf_test
import rest_framework.status  as status
import rest_framework.reverse as reverse

import hypothesis
import hypothesis.strategies as strategies


class DiceSeqStrategies:
    dice_rolls = strategies.lists(
        elements=strategies.sampled_from([4, 6, 8, 10, 12, 20, 100]), 
        min_size=1
    )

    user = strategies.just(dict(
        username = 'dungeon_master',
        email = 'dungeon_master@testserver.local',
        password = 'password123'
    ))

    @strategies.composite
    def seq_name(draw):
        seq_number = draw(strategies.integers(min_value=1))
        return f'Roll {seq_number}'

    @strategies.composite
    def dice_sequence(draw, seq_name=seq_name(), dice_rolls=dice_rolls):
        seq_name = draw(seq_name)
        dice_sequence = draw(dice_rolls)

        return dict(
            seq_name = seq_name,
            dice_sequence = dice_sequence
        )

    dice_sequence_list = strategies.lists(elements=dice_sequence())


    @strategies.composite
    def existing_uuid(draw, queryset=DiceSequence.objects.all()):
        max_value = len(queryset) - 1
        index = draw(strategies.integers(min_value=0, max_value=max_value))
        uuid = queryset[index].uuid
        
        return dict(uuid = uuid, exists = True, valid_uuid = False)

    @strategies.composite
    def non_existing_uuid(draw):
        return dict(uuid = draw(strategies.uuids()), exists = False, valid_uuid = False)

    @strategies.composite
    def invalid_uuid(draw):
        return dict(
            uuid = draw(strategies.text(max_size=100)), exists = False, valid_uuid = False
        )


class DiceSeqTests(rf_test.APITestCase):
    def setUp(self):
        sequences = DiceSeqStrategies.dice_sequence_list.example()
        new_user = DiceSeqStrategies.user.example()
        owner = User.objects.create(**new_user)
        for sequence in sequences:
            dice_sequence = DiceSequence.objects.create(seq_name=sequence['seq_name'], owner=owner)
            dice_sequence.sequence.set(sequence['dice_sequence'])
        
        self.queryset = DiceSequence.objects.all()


    def test_dice_seq_by_uuid_should_return_successfully(self):
        uuid = DiceSeqStrategies.existing_uuid().example()
        url = reverse.reverse('dice-seq-by-uuid', kwargs={'uuid': uuid['uuid']})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

