from django.contrib import admin

from .models import ChatLog, Email, EmailLog, Interaction, Message

admin.site.register(Interaction)
admin.site.register(ChatLog)
admin.site.register(EmailLog)
admin.site.register(Message)
admin.site.register(Email)
