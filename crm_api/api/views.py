from customers.models import Customer
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from interactions.models import ChatLog, EmailLog, Interaction
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from users.models import User

from .permissions import (CustomerPermission, InteractionPermission, IsAdmin,
                          LogsPermission, UserPermission)
from .serializers import (ChatLogCreateSerializer, ChatLogSerializer,
                          CustomerSerializer,
                          CustomerWithInteractionsSerializer,
                          EmailLogSerializer, GroupSerializer,
                          InteractionCreateSerializer, InteractionSerializer,
                          PermissionSerializer, UserCreateSerializer,
                          UserSerializer)


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated & CustomerPermission]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CustomerWithInteractionsSerializer
        return CustomerSerializer


class InteractionViewSet(ModelViewSet):
    queryset = Interaction.objects.all()
    serializer_class = InteractionSerializer
    permission_classes = [IsAuthenticated & InteractionPermission]

    def get_serializer_class(self):
        if self.action == 'create':
            return InteractionCreateSerializer
        return InteractionSerializer

    def create(self, request, *args, **kwargs):
        if not request.data.get('user'):
            request.data['user'] = request.user.id
        return super().create(request, *args, **kwargs)


class ChatLogViewSet(ModelViewSet):
    queryset = ChatLog.objects.all()
    serializer_class = ChatLogSerializer
    permission_classes = [IsAuthenticated & LogsPermission]

    def get_serializer_class(self):
        if self.action == 'create':
            return ChatLogCreateSerializer
        return ChatLogSerializer


class EmailLogViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated & LogsPermission]
    queryset = EmailLog.objects.all()
    serializer_class = EmailLogSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated & UserPermission]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            validate_password(serializer.validated_data['password'])
        except ValidationError as e:
            return Response(
                {'error': e.messages},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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


class GroupViewSet(ModelViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    permission_classes = [IsAuthenticated & IsAdmin]


class PermissionViewSet(ModelViewSet):
    serializer_class = PermissionSerializer
    queryset = Permission.objects.all()
    permission_classes = [IsAuthenticated & IsAdmin]
