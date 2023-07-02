import pytest
from django.core.management import call_command
from django.contrib.auth.models import Permission, Group

from users.models import User
from interactions.models import Interaction, Customer, ChatLog, EmailLog, Message, INTERACTION_TYPES

@pytest.mark.django_db
class TestCommands:
    """
    Since we made a fixture for create_groups command,
    we will not call it here.
    """

    def test_number_of_created_groups(self):
        assert len(Group.objects.all()) == 3

    def test_one_group_per_user(self, django_user_model, user_factory):
        user_factory.create_batch(5)
        for u in django_user_model.objects.all():
            assert u.groups.count() == 1

    def test_fill_db(self):
        call_command('filldb')

        users = User.objects.all()
        assert len(users) == 5

        for u in users:
            assert u.groups.count() == 1
            assert u.groups.get().name in ['manager', 'agent', 'admin']

        customers = Customer.objects.all()
        assert len(customers) == 5

        interactions = Interaction.objects.all()
        assert len(interactions) == 15

        for i in interactions:
            assert i.type in [x[0] for x in INTERACTION_TYPES]
            assert i.customer in customers
            assert i.user in users

        chats = ChatLog.objects.all()
        assert len(chats) == Interaction.objects.filter(type='chat').count()

        emails = EmailLog.objects.all()
        assert len(emails) == Interaction.objects.filter(type='email').count()

        assert Message.objects.count() == chats.count() * 5
