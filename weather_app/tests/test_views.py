import pytest
from django.http import HttpResponse

from django.test import Client
from pytest_django.asserts import assertTemplateUsed


def test_home_page_returns_correct_html(client: Client):
    """Тест: домашняя страница возвращает правильный html"""
    response = client.get("/")
    assertTemplateUsed(response, "home.html")


@pytest.mark.django_db
class TestForecastView:
    """Тест отображения прогноза погоды"""

    def test_uses_weather_template(self, client: Client):
        """Тест: используется шаблон прогноза погоды."""
        response = client.post("/api/", data={"city": "Санкт-Петербург"})
        assertTemplateUsed(response, "weather_forecast.html")

    def test_returns_correct_json(self, client: Client):
        """Тест: прогноз погоды содержится в контексте ответа."""
        response: HttpResponse = client.post("/api/", data={"city": "Санкт-Петербург"})
        assert response.context["city"] == "Санкт-Петербург"
        assert "Атмосферное давление" in response.context["current"]
        assert "Температура" in response.context["hourly"]
