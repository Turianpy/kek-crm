import random

from django.core.management import BaseCommand
from tests.factories import CustomerFactory, InteractionFactory, UserFactory


class Command(BaseCommand):
    help = 'Fill the database with dummy data'

    def handle(self, *args, **options):
        users = UserFactory.create_batch(5)
        customers = CustomerFactory.create_batch(5)

        x = [(users[i], customers[i]) for i in range(5)]

        for u, c in x:
            InteractionFactory.create_batch(
                3, user=u,
                customer=c,
                type=random.choice(['chat', 'email', 'phone call'])
            )

        self.stdout.write(
            self.style.SUCCESS('Successfully filled the database')
        )
