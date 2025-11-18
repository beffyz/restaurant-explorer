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