from django.shortcuts import render
from decouple import config
import requests
from pprint import pprint #print yazınca gelen veriyi daha düzenli göstermek için

def home(request):  
    API_KEY = config('API_KEY')  
    city = "Yozgat"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url) #request metodunu kullanaarak bu urlden bilgileri çek
    content = response.json() #json veriyi dictionary e çevirdik
    # pprint(content)
    context = {
        'city' : content['name'],
        'temp' : content['main']['temp'],
        'icon' : content['weather'][0]['icon'],
        'desc' : content['weather'][0]['description'],
    }
    
    print
    return render(request, "weatherapp/home.html", context)
