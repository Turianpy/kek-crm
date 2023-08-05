from django_filters import rest_framework as filters
from interactions.models import ChatLog, EmailLog
from users.models import User


class UserFilter(filters.FilterSet):

    supervisor = filters.CharFilter(field_name='supervisor__username')

    class Meta:
        model = User
        fields = ['supervisor']


class LogFilter(filters.FilterSet):
    user = filters.CharFilter(field_name='interaction__user__username')
    customer = filters.CharFilter(field_name='interaction__customer__email')


class ChatLogFilter(LogFilter):
    class Meta:
        model = ChatLog
        fields = [
            'interaction__user__username',
            'interaction__customer__email'
        ]


class EmailLogFilter(LogFilter):
    class Meta:
        model = EmailLog
        fields = [
            'interaction__user__username',
            'interaction__customer__email'
        ]
