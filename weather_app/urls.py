from django.urls import path
from weather_app import views

urlpatterns = [
    path("", views.home, name="home"),
    path("api/", views.api, name="api"),
    path("api/count/<str:city>", views.city_request_count, name="city-request-count"),
    path("autocomplete/", views.autocomplete, name="autocomplete")
]
