import pytest
import requests
from django.http import JsonResponse

from django.test import Client

from weather_app.weather_api import (get_location_by_city,
                                     BASE_FORECAST_URL)


class TestWeatherAPI:
    """Тест взаимодействия с АПИ прогноза погоды"""

    def test_get_base_forecast_url_returns_html_200(self, client: Client):
        """Тест: возвращает json и код состояния 200."""
        response = client.get(BASE_FORECAST_URL)

        assert response.status_code == 200
        assert response["content-type"] == "text/html; charset=utf-8"

    def test_geopy_return_coordinates_by_city(self):
        location = get_location_by_city("Санкт-Петербург")
        assert location.longitude, location.latitude == (59.938732, 30.316229)

    def test_get_forecast_url_with_returns_json_200(self):
        """Тест: возвращает json и код состояния 200."""
        location = get_location_by_city("Санкт-Петербург")
        query_string = {
            "latitude": round(location.latitude, 2),
            "longitude": round(location.longitude, 2),
        }
        response = requests.get("https://api.open-meteo.com/v1/forecast", params=query_string)
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json; charset=utf-8"


@pytest.mark.django_db
class TestCountAPI:
    """Тест АПИ счётчика, запрашиваемых прогнозов для различных городов"""

    def test_get_city_request_count_api_first_time_returns_json_with_error_200(self, client: Client):
        """Тест: возвращает json (error) и код 200, если прогноз для города запрашивается впервые."""
        response = client.get("/api/count/Санкт-Петербург")
        assert response.status_code == 200
        assert isinstance(response, JsonResponse)
        assert "error" in response.content.decode()

    def test_get_city_request_count_api_returns_json_200(self, client: Client):
        """Тест: возвращает json (count) и код состояния 200."""
        client.post("/api/", data={"city": "Санкт-Петербург"})
        client.post("/api/", data={"city": "Санкт-Петербург"})
        response = client.get("/api/count/Санкт-Петербург")
        assert isinstance(response, JsonResponse)
        assert response.content.decode() == '{"count": 2}'
