from customers.models import Customer
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from interactions.models import ChatLog, EmailLog, Interaction
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from users.models import User

from .filters import ChatLogFilter, EmailLogFilter, UserFilter
from .permissions import (ChatLogsPermission, CustomerPermission,
                          EmailLogsPermission, InteractionPermission, IsAdmin,
                          UserPermission)
from .serializers import (ChatLogCreateSerializer, ChatLogSerializer,
                          CustomerSerializer,
                          CustomerWithInteractionsSerializer,
                          EmailLogCreateSerializer, EmailLogSerializer,
                          EmailSerializer, GroupCreateSerializer,
                          GroupSerializer, InteractionCreateSerializer,
                          InteractionSerializer, PermissionSerializer,
                          UserCreateSerializer, UserSerializer)


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated & CustomerPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['business__name']
    search_fields = ['email', 'first_name', 'last_name']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CustomerWithInteractionsSerializer
        return CustomerSerializer


class InteractionViewSet(ModelViewSet):
    queryset = Interaction.objects.all()
    serializer_class = InteractionSerializer
    permission_classes = [IsAuthenticated & InteractionPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['type']
    search_fields = ['user__username', 'customer__email']

    def get_serializer_class(self):
        if self.action == 'create':
            return InteractionCreateSerializer
        return InteractionSerializer

    def create(self, request, *args, **kwargs):
        if not request.data.get('user'):
            request.data['user'] = request.user.id
        return super().create(request, *args, **kwargs)

    @action(detail=True, methods=['get'])
    def log(self, request, pk):
        interaction = Interaction.objects.get(id=pk)
        if interaction.type == 'chat':
            return Response(
                ChatLogSerializer(interaction.chatlog.get()).data
            )
        if interaction.type == 'email':
            return Response(
                EmailLogSerializer(interaction.emaillog.get()).data
            )
        file_handle = interaction.recording.open('rb')
        response = FileResponse(file_handle, content_type='audio/wav')
        response['Content-Disposition'] = (
            f'attachment; filename='
            f'"{interaction.recording.name}"'
        )
        return response


class ChatLogViewSet(ModelViewSet):
    queryset = ChatLog.objects.all()
    serializer_class = ChatLogSerializer
    permission_classes = [IsAuthenticated & ChatLogsPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ChatLogFilter
    http_method_names = ['get', 'post', 'delete']

    def get_serializer_class(self):
        if self.action == 'create':
            return ChatLogCreateSerializer
        return ChatLogSerializer


class EmailLogViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated & EmailLogsPermission]
    queryset = EmailLog.objects.all()
    serializer_class = EmailLogSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EmailLogFilter

    def get_serializer_class(self):
        if self.action == 'create':
            return EmailLogCreateSerializer
        return EmailLogSerializer

    @action(detail=True, methods=['post'])
    def add(self, request, pk):
        email = EmailSerializer(data={**request.data, 'log': pk})
        if email.is_valid(raise_exception=True):
            email.save()
            email_log = EmailLog.objects.get(id=pk)
            email_log.emails.add(email.instance)
            email_log.save()
        return Response(
            EmailLogSerializer(instance=email_log).data,
            status=status.HTTP_201_CREATED
        )


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated & UserPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = UserFilter
    search_fields = ['username']

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

    def get_serializer_class(self):
        if self.action == 'create':
            return GroupCreateSerializer
        return GroupSerializer


class PermissionViewSet(ModelViewSet):
    serializer_class = PermissionSerializer
    queryset = Permission.objects.all()
    permission_classes = [IsAuthenticated & IsAdmin]
