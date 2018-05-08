from django.contrib.auth.models import User

from rollservice.models import DiceSequence

import rest_framework.test    as rf_test
import rest_framework.status  as status
import rest_framework.reverse as reverse

import hypothesis.extra.django
import hypothesis.strategies  as strategies


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

    dice_sequence_list = strategies.lists(elements=dice_sequence(), min_size=1)

    @strategies.composite
    def existing_uuid(draw, queryset):
        max_value = len(queryset) - 1
        index = draw(strategies.integers(min_value=0, max_value=max_value))
        
        return queryset[index].uuid
        
    non_existing_uuid = strategies.uuids()
    invalid_uuid = strategies.text(max_size=100)

    @strategies.composite
    def existing_uuid_url(draw, queryset):
        max_value = len(queryset) - 1
        index = draw(strategies.integers(min_value=0, max_value=max_value))
        uuid = queryset[index].uuid
        url = reverse.reverse('dice-seq-by-uuid', args=[uuid])
        
        return url

    @strategies.composite
    def non_existing_uuid_url(draw, queryset, non_existing_uuid=non_existing_uuid):
        uuid = draw(non_existing_uuid)
        url = reverse.reverse('dice-seq-by-uuid', args=[uuid])
        
        return url

    @strategies.composite
    def invalid_uuid_url(draw, invalid_uuid=invalid_uuid):
        uuid = draw(invalid_uuid)
        url_root = reverse.reverse('dice-seq')
        url = url_root + uuid + '/'

        return url


class DiceSequenceByUUIDTests(hypothesis.extra.django.TestCase):
    @classmethod
    def setUpTestData(cls):
        sequences = DiceSeqStrategies.dice_sequence_list.example()
        new_user = DiceSeqStrategies.user.example()
        owner = User.objects.create(**new_user)
        for sequence in sequences:
            dice_sequence = DiceSequence.objects.create(seq_name=sequence['seq_name'], owner=owner)
            dice_sequence.sequence.set(sequence['dice_sequence'])
        
    
    queryset = DiceSequence.objects.all()
    client_class = rf_test.APIClient


    @hypothesis.given(DiceSeqStrategies.existing_uuid_url(queryset=queryset))
    def test_dice_seq_by_uuid_GET_with_existing_uuid_should_return_OK(self, url):
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


    @hypothesis.given(DiceSeqStrategies.non_existing_uuid_url(queryset=queryset))
    def test_dice_seq_by_uuid_GET_with_non_existing_uuid_should_return_NOT_FOUND(self, url):
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    @hypothesis.given(DiceSeqStrategies.invalid_uuid_url())
    def test_dice_seq_by_uuid_GET_with_invalid_uuid_should_return_BAD_REQUEST(self, url):
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    @hypothesis.given(strategies.one_of([
        DiceSeqStrategies.existing_uuid_url(queryset=queryset), 
        DiceSeqStrategies.non_existing_uuid_url(queryset=queryset),
        DiceSeqStrategies.invalid_uuid_url(),
    ]))
    def test_dice_seq_by_uuid_GET_idempotent(self, url):
        response1 = self.client.get(url)
        response2 = self.client.get(url)

        self.assertEqual(response1.status_code, response1.status_code)

