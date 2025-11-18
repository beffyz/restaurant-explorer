import json
from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt 
from .utils import get_restaurants, get_reviews, add_review_to_store

def restaurants(request):
    data = get_restaurants()
    
    context = {
        "restaurants": json.dumps(data), 
    }

    return render(request, "restaurants/restaurants.html", context)

@csrf_exempt
def restaurant(request, id):
    restaurant_id = int(id)

    if request.method == 'POST':
        try:
            if not request.body:
                return JsonResponse({'success': False, 'error': 'Request body is empty.'}, status=400)
            
            data = json.loads(request.body) 

            username = data.get('username')
            comment = data.get('comment')
            rating = int(data.get('rating'))
            
            if not (username and comment and rating):
                return JsonResponse({'success': False, 'error': 'Missing required fields.'}, status=400)

            new_review_data, new_average_rating = add_review_to_store(
                restaurant_id, username, comment, rating
            )

            return JsonResponse({
                'success': True,
                'new_review': new_review_data,
                'new_average_rating': new_average_rating
            })
        
        except Exception as e:
            return JsonResponse({
                'success': False, 
                'error': f'Server processing error: {type(e).__name__}: {str(e)}'
            }, status=500)
    
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

@csrf_exempt
def add_review_api(request, restaurant_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            comment = data.get('comment')
            rating = int(data.get('rating'))
            
            restaurant_id = int(restaurant_id)

            if not (username and comment and rating):
                return JsonResponse({'success': False, 'error': 'Missing required fields.'}, status=400)

            # This function adds the review and recalculates the average rating.
            new_review_data, new_average_rating = add_review_to_store(
                restaurant_id, username, comment, rating
            )

            return JsonResponse({
                'success': True,
                'new_review': new_review_data,
                'new_average_rating': new_average_rating
            })
        
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'Invalid data format: {e}'}, status=400)

    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)
    