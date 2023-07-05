import base64

from customers.models import Customer
from django.contrib.auth import get_user_model, models
from django.core.files.base import ContentFile
from interactions.models import (ChatLog, Email, EmailLog, Image, Interaction,
                                 Message)
from rest_framework import serializers as s
from rest_framework.exceptions import ValidationError

User = get_user_model()


class UserSerializer(s.ModelSerializer):

    interactions = s.SerializerMethodField()

    class Meta:
        model = User
        exclude = (
            'password', 'is_superuser', 'date_joined'
        )

    def get_interactions(self, instance):
        return InteractionShortSerializer(
            instance.interactions.all()[:10],
            many=True).data


class UserCreateSerializer(s.ModelSerializer):

    first_name = s.CharField(max_length=30, required=True)
    last_name = s.CharField(max_length=30, required=True)
    email = s.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            'username', 'password', 'phone_number',
            'first_name', 'last_name', 'email'
        ]

    def create(self, validated_data):
        pw = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(pw)
        user.save()
        return user

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop('password')
        return ret


class UserShortSerializer(s.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username']


class PermissionSerializer(s.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = models.Permission


class GroupCreateSerializer(s.ModelSerializer):

    permissions = s.PrimaryKeyRelatedField(
        queryset=models.Permission.objects.all(), many=True
    )

    class Meta:
        fields = '__all__'
        model = models.Group


class GroupSerializer(s.ModelSerializer):

    permissions = PermissionSerializer(many=True)

    class Meta:
        fields = '__all__'
        model = models.Group


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


class CustomerWithInteractionsSerializer(s.ModelSerializer):
    interactions = s.SerializerMethodField()

    class Meta:
        model = Customer
        fields = '__all__'

    def get_interactions(self, instance):
        return list(
            instance.interactions.all().values_list('id', flat=True)[:10]
        )


class CustomerShortSerializer(s.ModelSerializer):

    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'email']


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
        if not messages_data:
            raise ValidationError('required field')
        chatlog = ChatLog.objects.create(**validated_data)
        for message_data in messages_data:
            Message.objects.create(chat=chatlog, **message_data)
        return chatlog

    def update(self, instance, validated_data):
        if validated_data.get('messages'):
            raise ValidationError('cannot update messages')
        return super().update(instance, validated_data)


class ChatLogSerializer(s.ModelSerializer):

    messages = MessageSerializer(many=True)

    class Meta:
        model = ChatLog
        fields = '__all__'


class EmailSerializer(s.ModelSerializer):
    class Meta:
        model = Email
        exclude = ('log', )


class EmailLogSerializer(s.ModelSerializer):
    emails = EmailSerializer(many=True)
    participants = s.SerializerMethodField()

    class Meta:
        model = EmailLog
        fields = '__all__'

    def get_participants(self, instance):
        users, customers = [], []
        for p in instance.participants:
            if User.objects.filter(email=p).exists():
                users.append(
                    UserShortSerializer(User.objects.get(email=p)).data
                )
            else:
                customers.append(
                    CustomerShortSerializer(Customer.objects.get(email=p)).data
                )
        return {'users': users, 'customers': customers}


class EmailLogCreateSerializer(s.ModelSerializer):
    emails = EmailSerializer(many=True)

    class Meta:
        model = EmailLog
        fields = '__all__'

    def create(self, validated_data):
        emails_data = validated_data.pop('emails')
        if not emails_data:
            raise ValidationError('required field')
        email_log = EmailLog.objects.create(**validated_data)
        for data in emails_data:
            Email.objects.create(log=email_log, **data)
        return email_log


class ImageSerializer(s.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Image
        fields = ('image', 'interaction')


class InteractionShortSerializer(s.ModelSerializer):

    customer = s.PrimaryKeyRelatedField(queryset=Customer.objects.all())

    class Meta:
        model = Interaction
        fields = ['id', 'customer', 'type', 'date', 'notes']


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
    recording = Base64RecordingField(required=False)

    class Meta:
        model = Interaction
        fields = ('type', 'customer', 'notes', 'user', 'recording')
