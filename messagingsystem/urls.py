from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('messages.urls')),
    path('api/', include('users.urls')),
]

handler404 = 'exceptions.views.error_404'

handler500 = 'exceptions.views.error_500'
