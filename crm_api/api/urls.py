from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'api'


schema_view = get_schema_view(
    openapi.Info(
        title="CRM API",
        default_version='v1',
        description="A simple CRM API",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

v1_router = DefaultRouter()
v1_router.register('customers', views.CustomerViewSet, basename='customers')
v1_router.register(
    'interactions',
    views.InteractionViewSet,
    basename='interactions'
)
v1_router.register('users', views.UserViewSet, basename='users')
v1_router.register('groups', views.GroupViewSet, basename='groups')
v1_router.register(
    'permissions',
    views.PermissionViewSet,
    basename='permissions'
)
v1_logs_router = DefaultRouter()
v1_logs_router.register('chats', views.ChatLogViewSet, basename='chats')
v1_logs_router.register('emails', views.EmailLogViewSet, basename='emails')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/logs/', include(v1_logs_router.urls)),
    path('v1/auth/', include('djoser.urls')),
    path('v1/auth/', include('djoser.urls.jwt')),
    path(
        'v1/docs/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
    re_path(
        r'^v1/docs/(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'
    ),
]
