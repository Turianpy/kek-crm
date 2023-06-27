from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        agent = Group.objects.create(name='agent')
        manager = Group.objects.create(name='manager')
        admin = Group.objects.create(name='admin')

        admin_perms = perms = Permission.objects.all()
        agent_perms = manager_perms = Permission.objects.none()
        for m in ['interaction', 'customer', 'chatlog', 'emaillog', 'message']:
            agent_perms = agent_perms | perms.filter(codename__endswith=m)
            manager_perms = manager_perms | agent_perms

        manager_perms = manager_perms | perms.filter(codename__endswith='user')

        for p in ['change', 'delete']:
            agent_perms = agent_perms.exclude(codename__startswith=p)
        manager_perms = manager_perms.exclude(
            codename__startswith='delete', codename__endswith='user'
        )

        agent.permissions.add(*agent_perms)
        manager.permissions.add(*manager_perms)
        admin.permissions.add(*admin_perms)

        self.stdout.write(self.style.SUCCESS(
            'Successfully created admin, agent & manager groups '
            'and assigned permissions'
            ))
