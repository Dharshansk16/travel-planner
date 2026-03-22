import json
import os

class PlaceService:
    def __init__(self):
        data_path = os.path.join(
            os.path.dirname(__file__), '..', 'data', 'places.json'
        )
        with open(os.path.normpath(data_path), 'r') as f:
            self.places_data = json.load(f)

    def search_places(self, city, category=None, budget=None):
    # Normalize common name variations
        city_map = {
            "bengaluru": "Bangalore",
            "bangalore": "Bangalore",
            "bombay":    "Mumbai",
            "mumbai":    "Mumbai",
            "calcutta":  "Kolkata",
            "madras":    "Chennai",
        }
        city_normalized = city_map.get(city.lower(), city.title())

        res = [p for p in self.places_data
            if p['city'].lower() == city_normalized.lower()]
        if category:
            res = [p for p in res
                if p['category'].lower() == category.lower()]
        if budget is not None:
            res = [p for p in res if p['cost'] <= budget]
        return res