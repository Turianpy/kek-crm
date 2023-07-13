from http import HTTPStatus

import pytest
from fixtures.user_fixtures import *  # noqa


@pytest.mark.django_db
class TestAuth:

    create_url = '/api/v1/auth/jwt/create/'
    refresh_url = '/api/v1/auth/jwt/refresh/'

    def test_superuser_can_create_token(self, superuser_client):
        response = superuser_client.post(self.create_url, data={
            'username': 'admin',
            'password': 'adminpass123'
        })
        assert response.status_code == HTTPStatus.OK
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_superuser_can_refresh_token(
        self, superuser_client, superuser_token
    ):
        response = superuser_client.post(self.refresh_url, data={
            'refresh': superuser_token['refresh']
        })
        assert response.status_code == HTTPStatus.OK
        assert 'access' in response.data

    def test_regular_user_can_create_token(self, manager_client, user_manager):
        response = manager_client.post(self.create_url, data={
            'username': user_manager.username,
            'password': 'bigboss123'
        })

        assert response.status_code == HTTPStatus.OK
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_regular_user_can_refresh_token(
        self, manager_client, manager_token
    ):
        response = manager_client.post(self.refresh_url, data={
            'refresh': manager_token['refresh']
        })

        assert response.status_code == HTTPStatus.OK
        assert 'access' in response.data

    def test_user_can_not_create_token_with_wrong_password(
        self, manager_client, user_manager
    ):
        response = manager_client.post(self.create_url, data={
            'username': user_manager.username,
            'password': 'wrongpassword'
        })

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert 'access' not in response.data
        assert 'refresh' not in response.data

    def test_user_can_not_refresh_token_with_wrong_refresh_token(
        self, manager_client
    ):
        response = manager_client.post(self.refresh_url, data={
            'refresh': 'wrongrefresh'
        })

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert 'access' not in response.data
        assert 'refresh' not in response.data
