from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse

from weather_app.models import City
from weather_app.weather_api import get_weather_json_from_api


def home(request):
    return render(request, "home.html")


def api(request):
    city = request.POST["city"]
    context = {"city": city}
    try:
        response = get_weather_json_from_api(city)
        context.update({"current": response["Текущая"], "hourly": response["Почасовой прогноз"]})

        db_city = City.objects.get_or_create(title=city)[0]
        db_city.increment_count()
        db_city.save()

    except AttributeError:
        messages.error(request=request, message=f"Город {city} не найден, попробуйте ещё раз.")
        return redirect(reverse(home))

    return render(request, "weather_forecast.html", context)


def autocomplete(request):
    if "term" in request.GET:
        autocomplete_qs = City.objects.filter(title__icontains=request.GET.get("term"))
        autocomplete_titles = list()
        for city in autocomplete_qs:
            autocomplete_titles.append(city.title)
        return JsonResponse(autocomplete_titles, safe=False)


def city_request_count(request, city):
    if City.objects.filter(title=city).exists():
        count = City.objects.filter(title=city)[0].count
        return JsonResponse({"count": count})
    return JsonResponse({"error": "Прогноз погоды в этом городе пока что никто не запрашивал."})
