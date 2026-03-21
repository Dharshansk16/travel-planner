import json
from pathlib import Path

class PlaceService:
    def __init__(self):
        data_file = Path(__file__).resolve().parent.parent / "data" / "places.json"
        with data_file.open("r", encoding="utf-8") as f:
            self.places_data = json.load(f)

    def search_places(self, city, category=None, budget=None):
        
        res = [
            place for place in self.places_data
            if place['city'].lower() == city.lower()
        ]

        if category is not None:
            res = [
                place for place in res
                if place['category'].lower() == category.lower()
            ]

        if budget is not None:
            res = [
                place for place in res
                if place['cost'] <= budget
            ]

        return res