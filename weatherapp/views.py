from django.shortcuts import render, redirect, get_object_or_404
from decouple import config
import requests
from weatherapp.models import City
from django.contrib import messages
from pprint import pprint #print yazınca gelen veriyi daha düzenli göstermek için

def home(request):  
    API_KEY = config('API_KEY')  
    u_city = request.GET.get("name") # user city
    

    if u_city:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={u_city}&appid={API_KEY}&units=metric"
        response = requests.get(url) #request metodunu kullanaarak bu urlden bilgileri çek
        if response.ok: #Böyle bir şehir varsa
            content = response.json() #gelen veriyi dict e çevir
            db_city = content['name']
            if City.objects.filter(name=db_city): #Bu isimde bir şehir db de var mı 
                messages.warning(request, 'City already exists!')
            else:
                City.objects.create(name=db_city) #bd de yoksa city i bd ye kaydet
                messages.success(request, 'City created!')
        else:
            messages.error(request, 'There is no city!')
        return redirect('home')
    
    city_data = []
    cities = City.objects.all() #DB deki tüm city leri çek
    for city in cities: #Her bir city için API den veriyi çek, datayı city_data listesine ekle
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=tr&"
        response = requests.get(url)
        content = response.json()
        data = {
            # 'city': content['name'],
            'city': city, #Burada delete işleminde id lazım olacağı için API den değil de DB deki city i kullandık.
            'temp': round(int(content['main']['temp'])),
            'icon' : content['weather'][0]['icon'],
            'desc' : content['weather'][0]['description'],
        }
        city_data.append(data)
        # pprint(city_data)
        
    context = {
        'city_data': city_data,
    }
    
    return render(request, "weatherapp/home.html", context)



def delete_city(request, id):
    city = get_object_or_404(City, id=id)
    city.delete()
    messages.success(request, 'City deleted!')
    return redirect('home')