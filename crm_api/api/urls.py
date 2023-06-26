from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

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
v1_router.register('users', views.UserViewSet, basename='users')
v1_router.register('groups', views.GroupViewSet, basename='groups')
v1_router.register(
    'permissions',
    views.PermissionViewSet,
    basename='permissions'
)


urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/', include('djoser.urls')),
    path('v1/auth/', include('djoser.urls.jwt')),
]
