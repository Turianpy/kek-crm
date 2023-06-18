from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views
from users.views import UserViewSet

app_name = 'api'

v1_router = DefaultRouter()
v1_router.register('customers', views.CustomerViewSet, basename='customers')
v1_router.register(
    'interactions',
    views.InteractionViewSet,
    basename='interactions'
    )
v1_router.register('chats', views.ChatLogViewSet, basename='chats')
v1_router.register('emails', views.EmailLogViewSet, basename='emails')
v1_router.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/', include('djoser.urls')),
    path('v1/auth/', include('djoser.urls.jwt')),
]
