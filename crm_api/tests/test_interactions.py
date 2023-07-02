import pytest

from interactions.models import Interaction
from fixtures.user_fixtures import *

from http import HTTPStatus


@pytest.mark.django_db
class TestInteraction:

    list_url = '/api/v1/interactions/'
    detail_url = '/api/v1/interactions/{}/'

    def test_interaction_create(self, agent_client, user_agent, customer_factory):
        c = customer_factory.create()
        data = {
            'customer': c.id,
            'type': 'chat',
            'notes': 'test notes'
        }
        response = agent_client.post(self.list_url, data=data, format='json')

        assert response.status_code == HTTPStatus.CREATED
        assert Interaction.objects.count() == 1
        assert Interaction.objects.get().customer == c
        assert Interaction.objects.get().user == user_agent

    def test_interaction_list(self, agent_client, interaction_factory):
        interaction_factory.create_batch(5)
        response = agent_client.get(self.list_url)

        assert response.status_code == HTTPStatus.OK
        assert len(response.data['results']) == 5

    def test_interaction_retrieve(self, agent_client, user_agent, interaction_factory, superuser_client):
        i = interaction_factory.create()
        print(superuser_client.get(self.detail_url.format(i.id)))
        print(user_agent.has_perm('interactions.view_interaction'))
        response = agent_client.get(self.detail_url.format(i.id))

        assert response.status_code == HTTPStatus.OK
        assert response.data['id'] == i.id
