import base64

from customers.models import Customer
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from interactions.models import ChatLog, EmailLog, Image, Interaction, Message
from rest_framework import serializers as s
from users.models import Role


User = get_user_model()


class UserSerializer(s.ModelSerializer):

    role = s.PrimaryKeyRelatedField(queryset=Role.objects.all())

    class Meta:
        fields = '__all__'
        model = User

    def create(self, validated_data):
        pw = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(pw)
        user.save()
        return user


class RoleSerializer(s.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Role


class Base64RecordingField(s.FileField):

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:audio'):
            format, recordingstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(
                base64.b64decode(recordingstr),
                name='temp.' + ext
            )
        return super().to_internal_value(data)


class Base64ImageField(s.ImageField):

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class CustomerSerializer(s.ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'


class MessageSerializer(s.ModelSerializer):
    class Meta:
        model = Message
        fields = ('timestamp', 'sender', 'content')


class ChatLogCreateSerializer(s.ModelSerializer):
    interaction = s.PrimaryKeyRelatedField(queryset=Interaction.objects.all())
    messages = MessageSerializer(many=True)

    class Meta:
        model = ChatLog
        fields = '__all__'

    def create(self, validated_data):
        messages_data = validated_data.pop('messages')
        chatlog = ChatLog.objects.create(**validated_data)
        for message_data in messages_data:
            Message.objects.create(chat=chatlog, **message_data)
        return chatlog


class ChatLogSerializer(s.ModelSerializer):

    messages = MessageSerializer(many=True)

    class Meta:
        model = ChatLog
        fields = '__all__'


class EmailLogSerializer(s.ModelSerializer):
    class Meta:
        model = EmailLog
        fields = '__all__'


class ImageSerializer(s.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Image
        fields = ('image', 'interaction')


class InteractionSerializer(s.ModelSerializer):

    customer = CustomerSerializer()
    chatlog = s.SerializerMethodField()
    emaillog = s.SerializerMethodField()
    image = ImageSerializer(required=False)
    recording = Base64RecordingField(required=False)

    class Meta:
        model = Interaction
        fields = '__all__'
        requied_fields = ('type', 'customer', 'notes', 'user')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.type == 'chat':
            del representation['emaillog']
            del representation['recording']
        elif instance.type == 'email':
            del representation['chatlog']
            del representation['recording']
        elif instance.type == 'phone call':
            del representation['chatlog']
            del representation['emaillog']
        return representation

    def get_chatlog(self, instance):
        if instance.type == 'chat':
            return ChatLogSerializer(instance.chatlog.all(), many=True).data
        return None

    def get_emaillog(self, instance):
        if instance.type == 'email':
            return EmailLogSerializer(instance.emaillog.all(), many=True).data
        return None


class InteractionCreateSerializer(s.ModelSerializer):

    customer = s.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    user = s.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Interaction
        fields = ('type', 'customer', 'notes', 'user', 'recording')
