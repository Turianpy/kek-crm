import base64

from interactions.models import Interaction, ChatLog, Message, Image, EmailLog
from customers.models import Customer
from rest_framework import serializers as s

from django.core.files.base import ContentFile


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
        fields = '__all__'


class ChatLogSerializer(s.ModelSerializer):
    message = MessageSerializer(many=True)

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
    chatlog = ChatLogSerializer()
    emaillog = EmailLogSerializer()
    image = ImageSerializer()

    class Meta:
        model = Interaction
        fields = '__all__'
