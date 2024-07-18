from geopy.geocoders import Nominatim
import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry

BASE_FORECAST_URL = "https://open-meteo.com"
API_URL = "https://api.open-meteo.com/v1/forecast"


def get_location_by_city(city: str) -> tuple:
    """Получить координаты города по его названию."""
    geolocator = Nominatim(user_agent="sanamamail451@gmail.com")
    return geolocator.geocode(city)


cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)


def get_weather_json_from_api(city: str) -> dict:
    """Получить прогноз погоды из открытого АПИ open-meteo.com."""
    location = get_location_by_city(city)
    params = {"latitude": round(location.latitude, 2),
              "longitude": round(location.longitude, 2),
              "current": ["temperature_2m", "relative_humidity_2m", "precipitation", "cloud_cover", "pressure_msl",
                          "wind_speed_10m", "wind_direction_10m"],
              "hourly": ["temperature_2m"],
              "timezone": "Europe/Moscow",
              "forecast_days": 2,
              }

    responses = openmeteo.weather_api(API_URL, params=params)
    response = responses[0]
    print(f"Координаты {response.Latitude()}°С/Ш {response.Longitude()}°В/Д")
    print(f"Высота {response.Elevation()} м")
    print(f"Часовой пояс {response.Timezone()} {response.TimezoneAbbreviation()}")
    print(f"Cмещение часового пояса в секундах от GMT+0 {response.UtcOffsetSeconds()} сек")

    current = response.Current()

    current_temperature_2m = current.Variables(0).Value()
    current_relative_humidity_2m = current.Variables(1).Value()
    current_precipitation = current.Variables(2).Value()
    current_cloud_cover = current.Variables(3).Value()
    current_pressure_msl = current.Variables(4).Value()
    current_wind_speed_10m = current.Variables(5).Value()
    current_wind_direction_10m = current.Variables(6).Value()

    hourly = response.Hourly()

    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

    hourly_dataframe = pd.DataFrame(
        data={
            "Время": pd.date_range(
                start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=hourly.Interval()),
                inclusive="left",
            ).tz_convert(response.Timezone().decode()).strftime("%H:%M %d.%m"),
            "Температура": hourly_temperature_2m.astype(int).astype(str) + " °C"
        }
    )

    hourly_dataframe = hourly_dataframe.drop(index=[i for i in range(0, len(hourly_dataframe.index), 2)])

    return {
        "Текущая": {
            "Температура": str(round(current_temperature_2m)) + " °C",
            "Относительная влажность": str(round(current_relative_humidity_2m)) + " %",
            "Осадки": str(current_precipitation) + " мм",
            "Облачность": str(round(current_cloud_cover)) + " %",
            "Атмосферное давление": str(round(current_pressure_msl * 0.75)) + " мм.рт.ст.",
            "Скорость ветра": str(round(current_wind_speed_10m * 0.277778)) + " м/с",
            "Направление ветра": str(round(current_wind_direction_10m)) + " °",
        },
        "Почасовой прогноз": hourly_dataframe.transpose().to_html(header=False)
    }
