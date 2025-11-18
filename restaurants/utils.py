import json
from pathlib import Path

RESTAURANTS_DATA_FILE = Path(__file__).resolve().parent.parent / "data/restaurants.json"
REVIEWS_DATA_FILE = Path(__file__).resolve().parent.parent / "data/reviews.json"

def get_restaurants():
    with open(RESTAURANTS_DATA_FILE, "r", encoding="utf-8") as data:
        return json.load(data)

def get_reviews():
    with open(REVIEWS_DATA_FILE, "r", encoding="utf-8") as data:
        return json.load(data)

def _write_data(data, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def _get_next_review_id(reviews_data):
    if not reviews_data:
        return 1
    return max([r.get('id', 0) for r in reviews_data]) + 1

def recalculate_rating(restaurant_id, restaurants_data, reviews_data):
    restaurant_reviews = [
        r for r in reviews_data if r.get('restaurantId') == restaurant_id
    ]

    restaurant = next((r for r in restaurants_data if r.get("id") == restaurant_id), None)
    
    total_rating = sum(r['rating'] for r in restaurant_reviews)
    count = len(restaurant_reviews)
    new_average = total_rating / count
    new_average_rounded = round(new_average, 2)
    
    restaurant['rating'] = new_average_rounded 
    
    return new_average_rounded

def add_review_to_store(restaurant_id, username, comment, rating):
    restaurants_data = get_restaurants()
    reviews_data = get_reviews()
    
    new_review = {
        "id": _get_next_review_id(reviews_data),
        "restaurantId": restaurant_id,
        "rating": rating,
        "username": username,
        "comment": comment,
    }
    
    reviews_data.append(new_review)
    
    new_average_rating = recalculate_rating(
        restaurant_id, 
        restaurants_data, 
        reviews_data
    )
    
    _write_data(reviews_data, REVIEWS_DATA_FILE)
    _write_data(restaurants_data, RESTAURANTS_DATA_FILE)
    
    return new_review, new_average_rating