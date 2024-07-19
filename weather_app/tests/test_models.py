import pytest
from django.test import Client

from weather_app.models import City


@pytest.mark.django_db
class TestCityModel:
    """Тест модели города."""

    def test_title_is_primary_key(self):
        """Тест: название города является первичным ключом."""
        city = City(title="Санкт-Петербург")
        assert city.pk == "Санкт-Петербург"

    def test_count_increments_if_forecast_requested(self, client: Client):
        """Тест: счётчик просмотров увеличивается при запросе прогноза погоды для города."""
        city = City.objects.create(title="Санкт-Петербург")
        assert city.count == 0
        client.post("/api/", data={"city": "Санкт-Петербург"})
        client.post("/api/", data={"city": "Санкт-Петербург"})
        assert City.objects.get(title="Санкт-Петербург").count == 2


