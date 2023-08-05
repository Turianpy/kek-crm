import pytest


@pytest.fixture
def create_user(user_factory):
    return user_factory.build()


@pytest.fixture
def create_customer(customer_factory):
    return customer_factory.build()


@pytest.fixture
def create_interaction(interaction_factory):
    return interaction_factory.build()


@pytest.fixture
def create_chatlog(chatlog_factory):
    return chatlog_factory.build()


@pytest.fixture
def create_message(message_factory):
    return message_factory.build()


@pytest.fixture
def create_emaillog(emaillog_factory):
    return emaillog_factory.build()
