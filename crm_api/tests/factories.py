import array
import math
import os
import random
import tempfile
import wave

import factory
import pytz
from customers.models import Business, Customer
from django.contrib.auth.models import Group, Permission
from django.core.files import File
from factory.fuzzy import FuzzyChoice
from faker import Faker
from interactions.models import (INTERACTION_TYPES, ChatLog, Email, EmailLog,
                                 Interaction, Message)
from users.models import User


def generate_audio():
    sample_rate = 44100
    duration = 5
    frequency = 440
    volume = 100
    audio_data = array.array(
        'h',
        (int(volume * math.sin(
            2 * math.pi * frequency * t / sample_rate)
        ) for t in range(sample_rate * duration)))
    file_path = os.path.join(tempfile.gettempdir(), 'test.wav')

    with wave.open(file_path, 'w') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(sample_rate)
        f.writeframes(audio_data)

    return File(open(file_path, 'rb'), name='test.wav')


fake = Faker()


class PermissionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Permission

    codename = factory.LazyAttribute(lambda x: fake.word())
    name = factory.LazyAttribute(lambda x: fake.word())


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group

    name = factory.LazyAttribute(lambda x: fake.word())

    @factory.post_generation
    def add_permissions(self, create, extracted, **kwargs):
        if not create:
            return
        for _ in range(5):
            PermissionFactory.create(group=self)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    employed_since = factory.LazyAttribute(
        lambda x: fake.date_time(tzinfo=pytz.UTC)
    )
    username = factory.LazyAttribute(lambda x: fake.user_name())
    password = factory.LazyAttribute(lambda x: fake.password())
    email = factory.LazyAttribute(lambda x: fake.email())
    phone_number = factory.LazyAttribute(lambda x: fake.phone_number())

    @factory.post_generation
    def add_groups(self, create, extracted, **kwargs):
        if not create:
            return
        self.groups.add(random.choice(Group.objects.all()))

        self.set_password(self.password)
        self.save()


class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer

    first_name = factory.LazyAttribute(lambda x: fake.first_name())
    last_name = factory.LazyAttribute(lambda x: fake.last_name())
    email = factory.LazyAttribute(lambda x: fake.email())
    phone_number = factory.LazyAttribute(lambda x: fake.phone_number())


class InteractionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Interaction

    type = FuzzyChoice([p[0] for p in INTERACTION_TYPES])
    customer = factory.SubFactory(CustomerFactory)
    notes = factory.LazyAttribute(lambda x: fake.text(max_nb_chars=30))
    user = factory.SubFactory(UserFactory)

    @factory.post_generation
    def add_related_log(self, create, extracted, **kwargs):
        if not create:
            return
        if self.type == 'chat':
            ChatLogFactory.create(interaction=self)
        elif self.type == 'email':
            EmailLogFactory.create(interaction=self)
        else:
            self.recording = generate_audio()
            self.save()
            self.recording.close()


class ChatLogFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ChatLog

    interaction = factory.SubFactory(InteractionFactory)
    started_at = factory.LazyAttribute(
        lambda x: fake.date_time(tzinfo=pytz.UTC)
    )
    ended_at = factory.LazyAttribute(lambda x: fake.date_time(tzinfo=pytz.UTC))

    @factory.post_generation
    def add_messages(self, create, extracted, **kwargs):
        if not create:
            return
        for _ in range(5):
            MessageFactory.create(chat=self)


class MessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Message

    timestamp = factory.LazyAttribute(
        lambda x: fake.date_time(tzinfo=pytz.UTC)
    )
    sender = factory.LazyAttribute(lambda x: fake.name())
    content = factory.LazyAttribute(lambda x: fake.text())
    chat = factory.SubFactory(ChatLogFactory)


class EmailLogFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmailLog

    interaction = factory.SubFactory(InteractionFactory)
    participants = factory.LazyAttribute(
        lambda x: [
            u.email for u in random.sample(
                list(User.objects.all()),
                random.randint(1, 3)
            )
        ] + [
            random.choice(list(Customer.objects.all())).email
        ]
    )

    @factory.post_generation
    def add_emails(self, create, extracted, **kwargs):
        if not create:
            return
        for _ in range(5):
            EmailFactory.create(log=self)


class EmailFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Email

    subject = factory.LazyAttribute(lambda x: fake.text(max_nb_chars=30))
    body = factory.LazyAttribute(lambda x: fake.text(max_nb_chars=100))
    log = factory.SubFactory(EmailLogFactory)
    sent_at = factory.LazyAttribute(lambda x: fake.date_time(tzinfo=pytz.UTC))

    @factory.post_generation
    def add_sender_and_receiver(self, create, extracted, **kwargs):
        self.sender, self.receiver = random.sample(
            self.log.participants,
            2
        )
        if create:
            self.save()
        return self


class BusinessFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Business

    name = factory.LazyAttribute(lambda x: fake.company())
    address = factory.LazyAttribute(lambda x: fake.address())
    phone_number = factory.LazyAttribute(lambda x: fake.phone_number())
    email = factory.LazyAttribute(lambda x: fake.email())
