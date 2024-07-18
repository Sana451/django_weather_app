from django.urls import path
from weather_app import views

urlpatterns = [
    path("", views.home, name="home"),
    path("api/", views.api, name="api"),
]
