from django.core.management import BaseCommand
from tests.factories import (ChatLogFactory, CustomerFactory, EmailFactory,
                             InteractionFactory, MessageFactory, RoleFactory,
                             UserFactory, generate_base64_audio)


class Command(BaseCommand):
    help = 'Fill the database with dummy data'

    def handle(self, *args, **options):
        # Create roles
        admin_role = RoleFactory(name='admin', permissions='admin')
        agent_role = RoleFactory(
            name='agent', permissions=[
                'create interactions', 'view interactions',
                'create customers', 'view customers',
                'create logs'
            ])
        manager_role = RoleFactory(
            name='manager', permissions=[
                'create interactions', 'view interactions',
                'create customers', 'view customers',
                'create logs', 'view logs'
            ]
        )

        # Create users
        UserFactory.create_batch(5, role=agent_role)
        UserFactory.create_batch(2, role=manager_role)
        UserFactory.create_batch(1, role=admin_role)

        # Create customers
        c = CustomerFactory.create_batch(10)

        # Create interactions
        for x in c:
            InteractionFactory.create_batch(3, customer=x)
