from http import HTTPStatus

import pytest
from fixtures.user_fixtures import *  # noqa
from interactions.models import Interaction
from utils import check_pagination


@pytest.mark.django_db
class TestInteraction:

    list_url = '/api/v1/interactions/'
    detail_url = '/api/v1/interactions/{}/'
    chats_url = '/api/v1/logs/chats/'
    emails_url = '/api/v1/logs/emails/'

    def test_interaction_create(
            self, agent_client,
            user_agent, customer_factory
    ):
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

    def test_interaction_create_invalid(self, agent_client, customer_factory):
        c = customer_factory.create()
        data = {
            'customer': c.id,
            'type': 'invalid',
            'notes': 'test notes'
        }
        response = agent_client.post(self.list_url, data=data, format='json')

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert Interaction.objects.count() == 0

    def test_interaction_create_missing_fields(
            self, agent_client,
            customer_factory
    ):
        c = customer_factory.create()
        data = {
            'customer': c.id,
            'type': 'chat',
        }
        response = agent_client.post(self.list_url, data=data, format='json')

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert Interaction.objects.count() == 0

    def test_interaction_list(self, agent_client, interaction_factory):
        interaction_factory.create_batch(5)
        response = agent_client.get(self.list_url)

        check_pagination(response)
        assert response.status_code == HTTPStatus.OK
        assert len(response.data['results']) == 5

    def test_interaction_retrieve(
            self, agent_client,
            user_agent, interaction_factory,
            superuser_client
    ):
        i = interaction_factory.create()
        print(superuser_client.get(self.detail_url.format(i.id)))
        print(user_agent.has_perm('interactions.view_interaction'))
        response = agent_client.get(self.detail_url.format(i.id))

        assert response.status_code == HTTPStatus.OK
        assert response.data['id'] == i.id

    def test_interaction_update(self, admin_client, interaction_factory):
        i = interaction_factory.create()
        data = {
            'notes': 'updated notes'
        }
        response = admin_client.patch(
            self.detail_url.format(i.id),
            data=data, format='json'
        )

        assert response.status_code == HTTPStatus.OK
        assert Interaction.objects.get().notes == 'updated notes'

    def test_interaction_update_invalid(
            self, admin_client,
            interaction_factory
    ):
        i = interaction_factory.create()
        data = {
            'type': 'invalid'
        }
        response = admin_client.patch(
            self.detail_url.format(i.id),
            data=data, format='json'
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert Interaction.objects.get().type != 'invalid'

    def test_chatlog_create(
            self, agent_client,
            customer_factory, message_factory
    ):
        c = customer_factory.create()
        data = {
            'type': 'chat',
            'notes': 'test notes',
            'customer': c.id
        }
        agent_client.post(self.list_url, data=data, format='json')
        i = Interaction.objects.get()
        msgs = message_factory.build_batch(5)
        data = {
            'interaction': i.id,
            'messages': [
                {
                    'timestamp': m.timestamp,
                    'sender': m.sender,
                    'content': m.content
                } for m in msgs],
            'started_at': msgs[0].timestamp,
            'ended_at': msgs[-1].timestamp
        }

        response = agent_client.post(self.chats_url, data=data, format='json')
        assert response.status_code == HTTPStatus.CREATED
        data['messages'] = []
        response = agent_client.post(self.chats_url, data=data, format='json')
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_email_log_create(
            self, agent_client,
            customer_factory,
            user_factory,
            email_factory
    ):
        c = customer_factory.create()
        u = user_factory.create_batch(3)
        i = Interaction.objects.create(user=u[0], customer=c, type='email')

        emails_data = [
            {
                'sender': e.sender,
                'receiver': e.receiver,
                'subject': e.subject,
                'body': e.body,
                'sent_at': e.sent_at
            } for e in email_factory.build_batch(5)]

        data = {
            'interaction': i.id,
            'participants': [u.email for u in u] + [c.email],
            'emails': emails_data
        }
        response = agent_client.post(self.emails_url, data=data, format='json')
        assert response.status_code == HTTPStatus.CREATED
        data['emails'] = []
        response = agent_client.post(self.emails_url, data=data, format='json')
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_chatlog_update(
            self, admin_client,
            chat_log_factory
    ):
        c = chat_log_factory.create()
        response = admin_client.patch(
            self.chats_url + str(c.id) + '/',
            data={}, format='json'
        )
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
