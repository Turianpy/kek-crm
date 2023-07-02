import pytest

from django.contrib.auth.models import Permission
from fixtures.user_fixtures import *

from interactions.models import Interaction


@pytest.mark.django_db
class TestPermissions:

    def test_superuser_has_all_permissions(self, user_superuser):
        for perm in Permission.objects.all():
            assert user_superuser.has_perm(perm.codename)

    def test_admin_has_all_permissions(self, user_admin):
        for perm in Permission.objects.all():
            assert user_admin.has_perm(perm.codename)

    def test_interaction_permissions(self, user_manager, user_agent):
        print(user_agent.groups.all())
        assert user_agent.has_perm('interactions.view_interaction')
        assert user_agent.has_perm('interactions.add_interaction')
        assert not user_agent.has_perm('interactions.change_interaction')
        assert not user_agent.has_perm('interactions.delete_interaction')

        for p in Permission.objects.filter(codename__endswith='interaction'):
            assert user_manager.has_perm('interactions.' + p.codename)

    def test_user_permissions(self, user_manager, user_agent):
        for p in Permission.objects.filter(codename__endswith='user'):
            assert not user_agent.has_perm('users.' + p.codename)
            if p.codename.startswith('delete'):
                assert not user_manager.has_perm('users.' + p.codename)
            else:
                assert user_manager.has_perm('users.' + p.codename)

    def test_customer_permissions(self, user_manager, user_agent):
        for p in Permission.objects.filter(codename__endswith='customer'):
            if p.codename in ['delete_customer', 'change_customer']:
                assert not user_agent.has_perm('customers.' + p.codename)
            else:
                assert user_agent.has_perm('customers.' + p.codename)
            assert user_manager.has_perm('customers.' + p.codename)
