from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse

from weather_app.forms import CityForm
from weather_app.weather_api import get_weather_json_from_api


def home(request):
    form = CityForm()
    return render(request, "home.html", context={"city_form": form})


def api(request):
    city = request.POST["city"]
    context = {"city": city}
    try:
        response = get_weather_json_from_api(city)
        context.update({"current": response["Текущая"], "hourly": response["Почасовой прогноз"]})

    except AttributeError:
        messages.error(request=request, message=f"Город {city} не найден, попробуйте ещё раз.")
        return redirect(reverse(home))

    return render(request, "weather_forecast.html", context)
