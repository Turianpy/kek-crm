from http import HTTPStatus

import pytest
from customers.models import Customer
from fixtures.user_fixtures import *  # noqa


@pytest.mark.django_db
class TestCustomers:

    list_url = '/api/v1/customers/'
    detail_url = '/api/v1/customers/{}/'

    def test_customer_create(self, agent_client):
        data = {
            'first_name': 'test',
            'last_name': 'test',
            'email': 'customer@test.com',
            'phone_number': '+1234567890',
        }
        response = agent_client.post(self.list_url, data=data, format='json')
        assert response.status_code == HTTPStatus.CREATED
        assert Customer.objects.count() == 1