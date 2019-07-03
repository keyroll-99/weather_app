from django.shortcuts import render
import requests
from .models import Weather
from .froms import WatherForm
import json
# Create your views here.


def index(request):
    context = {}
    weather_form = WatherForm(request.POST or None)
    if weather_form.is_valid():
        if request.user.is_authenticated:
            new_city = weather_form.save(commit=False)
            new_city.user = request.user
            if len(Weather.objects.filter(user=new_city.user, city=new_city.city)) == 0:
                new_city.save()

            weather_form = WatherForm
        else:
            city = weather_form['city'].value()

            url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid=3be45b9713bec8b1e52ba427fdffb48b&units=metric".format(city)
            r = requests.get(url).json()
            weather_data = []
            if r['cod'] != '404':
                temp = r['main']['temp']
                wind = r['wind']['speed']
                des = r['weather'][0]['description']
                icon = r['weather'][0]['icon']
                city_weather = {
                    'city': city,
                    'temperature': temp,
                    'wind': wind,
                    'description': des,
                    'icon': icon
                }
                weather_data = [city_weather]
            else:
                weather_data.append("city doesn't exist in our database")

            context['weather'] = weather_data

    context['form'] = weather_form
    if request.user.is_authenticated:
        cities = Weather.objects.filter(user=request.user)
        if len(cities) > 0:
            weather_data = []
            for city in cities:
                url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid=3be45b9713bec8b1e52ba427fdffb48b&units=metric".format(city.city)
                r = requests.get(url).json()
                # print(r)
                if r['cod'] != "404":
                    temp = r['main']['temp']
                    wind =r['wind']['speed']
                    des = r['weather'][0]['description']
                    icon = r['weather'][0]['icon']
                    city_weather = {
                        'city': city.city,
                        'temperature': temp,
                        'wind': wind,
                        'description':des ,
                        'icon': icon

                    }
                    weather_data.append(city_weather)
                else:
                    Weather.objects.filter(pk=city.pk).delete()
        try:
            context['weather'] = weather_data
        except:
            context['wather'] = []
    # print(context)
    return render(request, 'index.html', context)
