from rest_framework import serializers

from .models import Role, User


class UserSerializer(serializers.Serializer):

    class Meta:
        fields = '__all__'
        model = User


class RoleSerializer(serializers.Serializer):

    class Meta:
        fields = '__all__'
        model = Role
