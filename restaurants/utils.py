import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data.json"

def get_restaurants():
    with open(DATA_FILE, "r", encoding="utf-8") as data:
        return json.load(data)
