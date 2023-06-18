from customers.models import Customer
from interactions.models import ChatLog, EmailLog, Image, Interaction
from rest_framework.viewsets import ModelViewSet

from .serializers import (ChatLogSerializer, ChatLogCreateSerializer, CustomerSerializer,
                          EmailLogSerializer, InteractionCreateSerializer,
                          InteractionSerializer)


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class InteractionViewSet(ModelViewSet):
    queryset = Interaction.objects.all()
    serializer_class = InteractionSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return InteractionCreateSerializer
        return InteractionSerializer


class ChatLogViewSet(ModelViewSet):
    queryset = ChatLog.objects.all()
    serializer_class = ChatLogSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return ChatLogCreateSerializer
        return ChatLogSerializer


class EmailLogViewSet(ModelViewSet):
    queryset = EmailLog.objects.all()
    serializer_class = EmailLogSerializer
