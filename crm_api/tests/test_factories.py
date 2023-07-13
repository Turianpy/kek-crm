import pytest
from interactions.models import (INTERACTION_TYPES, ChatLog, Customer,
                                 EmailLog, Interaction, Message)


@pytest.mark.django_db
class TestFactories:

    def test_user_create(self, user_factory, django_user_model):
        u = user_factory.create()
        assert django_user_model.objects.count() == 1
        assert u.groups.count() == 1

    def test_interaction_and_subfactories(self, interaction_factory):
        interactions = [
            interaction_factory.create(type=t[0]) for t in INTERACTION_TYPES
        ]

        assert Interaction.objects.count() == len(INTERACTION_TYPES)
        for i in interactions:
            if i.type == 'chat':
                assert ChatLog.objects.count() == 1
                assert Message.objects.count() == 5
            elif i.type == 'email':
                assert EmailLog.objects.count() == 1
            else:
                assert i.recording is not None
                assert i.recording.closed
                assert i.recording.size > 0
            assert i.customer is not None
            assert i.user is not None

    def test_customer_create(self, customer_factory):
        customer_factory.create_batch(5)
        assert Customer.objects.count() == 5
