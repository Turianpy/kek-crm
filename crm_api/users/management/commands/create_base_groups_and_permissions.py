from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        agent = Group.objects.create(name='agent')
        manager = Group.objects.create(name='manager')
        admin = Group.objects.create(name='admin')

        perms = {
            'view_interactions': 'Can view interactions',
            'create_interactions': 'Can create interactions',
            'view_customers': 'Can view customers',
            'create_customers': 'Can create customers',
            'view_logs': 'Can view logs',
            'create_logs': 'Can create logs',
            'view_users': 'Can view users',
            'create_users': 'Can create users',
            'admin': 'admin'
        }

        for k, v in perms.items():
            Permission.objects.create(codename=k, name=v)

        agent_perms = Permission.objects.filter(
            codename__in=[
                'view_interactions',
                'create_interactions',
                'view_customers',
                'create_customers',
                'create_logs'
            ])
        manager_perms = Permission.objects.filter(
            codename__not_in=[
                'create_users',
            ]
        )
        admin_perms = Permission.objects.get(codename='admin')

        agent.permissions.add(*agent_perms)
        manager.permissions.add(*manager_perms)
        admin.permissions.add(*admin_perms)

        self.stdout.write(self.style.SUCCESS(
            'Successfully created admin, agent & manager groups '
            'and their respective permissions'
            ))
