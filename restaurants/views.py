import json
from django.http import Http404
from django.shortcuts import render
from .utils import get_restaurants, get_reviews

def restaurants(request):
    data = get_restaurants()
    
    context = {
        "restaurants": json.dumps(data), 
    }

    return render(request, "restaurants/restaurants.html", context)

def restaurant(request, id):
    restaurants_data = get_restaurants()
    reviews_data = get_reviews()

    restaurant = next((r for r in restaurants_data if r["id"] == id), None)
    
    if not restaurant:
        raise Http404("Restaurant not found")

    reviews = [r for r in reviews_data if r["restaurantId"] == id]
    
    context = {
        "restaurant": json.dumps(restaurant),
        "reviews": json.dumps(reviews)
    }

    return render(request, "restaurant/restaurant.html", context)
    