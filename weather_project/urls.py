from django.contrib import admin
from django.urls import path, include
from weather_app import urls as weather_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include(weather_urls)),
]
