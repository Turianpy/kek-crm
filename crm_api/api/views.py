from customers.models import Customer
from interactions.models import ChatLog, EmailLog, Interaction
from permissions import (CustomerPermission, InteractionPermission,
                         LogsPermission, UserPermission, IsAdmin)
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from users.models import User, Role

from .serializers import (ChatLogCreateSerializer, ChatLogSerializer,
                          CustomerSerializer, EmailLogSerializer,
                          InteractionCreateSerializer, InteractionSerializer,
                          UserSerializer, RoleSerializer)


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [CustomerPermission, IsAuthenticated]


class InteractionViewSet(ModelViewSet):
    queryset = Interaction.objects.all()
    serializer_class = InteractionSerializer
    permission_classes = [InteractionPermission, IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return InteractionCreateSerializer
        return InteractionSerializer


class ChatLogViewSet(ModelViewSet):
    queryset = ChatLog.objects.all()
    serializer_class = ChatLogSerializer
    permission_classes = [LogsPermission, IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return ChatLogCreateSerializer
        return ChatLogSerializer


class EmailLogViewSet(ModelViewSet):
    permission_classes = [LogsPermission, IsAuthenticated]
    queryset = EmailLog.objects.all()
    serializer_class = EmailLogSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [UserPermission, IsAuthenticated]

    @action(detail=False, methods=['get'])
    def user_by_email(self, request):
        email = request.query_params.get('email')
        user = User.objects.get(email=email)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def user_by_phone(self, request):
        phone = request.query_params.get('phone')
        user = User.objects.get(phone_number=phone)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class RoleViewSet(viewsets.ModelViewSet):
    serializer_class = RoleSerializer
    queryset = Role.objects.all()
    permission_classes = [IsAuthenticated, IsAdmin]
