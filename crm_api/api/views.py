from customers.models import Customer
from interactions.models import ChatLog, EmailLog, Image, Interaction
from rest_framework.viewsets import ModelViewSet

from .serializers import (ChatLogSerializer, CustomerSerializer,
                          EmailLogSerializer, ImageSerializer,
                          InteractionSerializer)


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class InteractionViewSet(ModelViewSet):
    queryset = Interaction.objects.all()
    serializer_class = InteractionSerializer


class ChatLogViewSet(ModelViewSet):
    queryset = ChatLog.objects.all()
    serializer_class = ChatLogSerializer


class EmailLogViewSet(ModelViewSet):
    queryset = EmailLog.objects.all()
    serializer_class = EmailLogSerializer
