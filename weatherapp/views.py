from django.shortcuts import render, redirect
import requests
from .models import *
from .forms import CityForm 
from django.contrib import messages
# Create your views here.

def Home(request):
    url  = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=You Api Key'
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()
            
            if existing_city_count == 0:  
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    messages.error(request, 'city does not exsist!')
            else:
                messages.warning(request, 'city already exsist!')

    form = CityForm()
    cities = City.objects.all()
    weather_data = []

    for city in cities:
        r = requests.get(url.format(city)).json()
        city_weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }
        weather_data.append(city_weather)

    context = {'weather_data' : weather_data, 'form' : form}
    return render(request,'weatherapp/weather.html',context)

def delete_city(request,city_name):
    City.objects.get(name=city_name).delete()
    return redirect("Home")