from rest_framework import viewsets
from rest_framework.decorators import action
from .serializers import UserSerializer
from .models import User
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

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
