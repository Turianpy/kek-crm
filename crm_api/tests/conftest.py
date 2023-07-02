import pytest
from django.core.management import call_command
from factories import (BusinessFactory, ChatLogFactory, CustomerFactory,
                       EmailFactory, InteractionFactory, MessageFactory,
                       UserFactory)
from pytest_factoryboy import register
from interactions.models import Interaction
import os
import shutil

register(CustomerFactory)
register(InteractionFactory)
register(ChatLogFactory)
register(MessageFactory)
register(EmailFactory)
register(UserFactory)
register(BusinessFactory)


@pytest.fixture(scope='session', autouse=True)
def setup_groups_and_permissions(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('create_groups')


@pytest.fixture(scope='function', autouse=True)
def cleanup():

    yield

    for interaction in Interaction.objects.all():
        if interaction.recording and os.path.isfile(interaction.recording.path):
            os.remove(interaction.recording.path)
