import json
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from .utils import get_restaurants

def restaurants(request):
    data = get_restaurants()
    
    context = {
        "restaurants": json.dumps(data), 
    }

    return render(request, "restaurants/restaurants.html", context)

def restaurant(request, id):
    data = get_restaurants()

    restaurant = next((r for r in data if r["id"] == id), None)

    if not restaurant:
        raise Http404("Restaurant not found")

    context = {
        "restaurant": json.dumps(restaurant), 
    }

    return render(request, "restaurant/restaurant.html", context)
    