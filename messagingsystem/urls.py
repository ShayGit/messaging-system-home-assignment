from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls import url

schema_view = get_schema_view(
    openapi.Info(
        title="Messaging System API",
        default_version='v1',
        description="""A simple Django rest api that is responsible for handling messages between users.
       Using jwt authentication for users.""",
        contact=openapi.Contact(email="shay291@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('messages.urls')),
    path('api/', include('users.urls')),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

handler404 = 'exceptions.views.error_404'

handler500 = 'exceptions.views.error_500'
