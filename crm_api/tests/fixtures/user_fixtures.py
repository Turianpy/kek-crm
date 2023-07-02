import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.contrib.auth.models import Group


@pytest.fixture
def user_superuser(django_user_model):
    user = django_user_model.objects.create_superuser(
        username='admin',
        email='admin@kekcrm.com',
        password='adminpass123'
    )
    return user

@pytest.fixture
def user_admin(user_factory):
    user = user_factory.create(password='admin123')
    for g in user.groups.all():
        user.groups.remove(g)
    user.groups.add(Group.objects.get(name='admin'))
    user.save()
    return user


@pytest.fixture
def user_manager(user_factory):
    user = user_factory.create(password='bigboss123')
    for g in user.groups.all():
        user.groups.remove(g)
    user.groups.add(Group.objects.get(name='manager'))
    user.save()
    return user


@pytest.fixture
def user_agent(user_factory):
    user = user_factory.create(password='superagent123')
    for g in user.groups.all():
        user.groups.remove(g)
    user.groups.add(Group.objects.get(name='agent'))
    user.save()
    return user


@pytest.fixture
def superuser_token(user_superuser):
    return {
        'access': str(AccessToken.for_user(user_superuser)),
        'refresh': str(RefreshToken.for_user(user_superuser))
    }


@pytest.fixture
def superuser_client(superuser_token):
    client = APIClient()
    client.credentials(
        HTTP_AUTHORIZATION='Bearer ' + superuser_token['access']
    )
    return client


@pytest.fixture
def manager_token(user_manager):
    return {
        'access': str(AccessToken.for_user(user_manager)),
        'refresh': str(RefreshToken.for_user(user_manager))
    }


@pytest.fixture
def manager_client(manager_token):
    client = APIClient()
    client.credentials(
        HTTP_AUTHORIZATION='Bearer ' + manager_token['access']
    )
    return client


@pytest.fixture
def agent_token(user_agent):
    return {
        'access': str(AccessToken.for_user(user_agent)),
        'refresh': str(RefreshToken.for_user(user_agent))
    }


@pytest.fixture
def agent_client(agent_token):
    client = APIClient()
    client.credentials(
        HTTP_AUTHORIZATION='Bearer ' + agent_token['access']
    )
    return client


@pytest.fixture
def admin_token(user_admin):
    return {
        'access': str(AccessToken.for_user(user_admin)),
        'refresh': str(RefreshToken.for_user(user_admin))
    }


@pytest.fixture
def admin_client(admin_token):
    client = APIClient()
    client.credentials(
        HTTP_AUTHORIZATION='Bearer ' + admin_token['access']
    )
    return client
