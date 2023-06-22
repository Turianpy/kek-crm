from factories import (BusinessFactory, ChatLogFactory, CustomerFactory,
                       EmailFactory, InteractionFactory, MessageFactory,
                       RoleFactory, UserFactory)
from pytest_factoryboy import register

register(CustomerFactory)
register(InteractionFactory)
register(ChatLogFactory)
register(MessageFactory)
register(EmailFactory)
register(UserFactory)
register(RoleFactory)
register(BusinessFactory)
