import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from users.models import Role


@pytest.fixture
def user_superuser(django_user_model, role_factory):
    user = django_user_model.objects.create_superuser(
        username='testuser',
        email='superuser@example.com',
        password='testpass123',
        role=role_factory.create(name='admin', permissions=['admin'])
    )
    return user


@pytest.fixture
def user_agent(django_user_model, role_factory):
    user = django_user_model.objects.create_user(
        username='testuser',
        email='agent@example.com',
        password='testpass123',
        role=role_factory.create(name='agent', permissions=[
            'create interactions', 'view interactions',
            'create customers', 'view customers',
            'create logs'
        ])
    )
    return user


@pytest.fixture
def superuser_token(user_superuser):
    token = AccessToken.for_user(user_superuser)
    return {
        'access': str(token)
    }


@pytest.fixture
def superuser_client(superuser_token):
    client = APIClient()
    client.credentials(
        HTTP_AUTHORIZATION='Bearer ' + superuser_token['access']
    )
    return client


@pytest.fixture
def agent_token(user_agent):
    token = AccessToken.for_user(user_agent)
    return {
        'access': str(token)
    }


@pytest.fixture
def agent_client(agent_token):
    client = APIClient()
    client.credentials(
        HTTP_AUTHORIZATION='Bearer ' + agent_token['access']
    )
    return client
