import json
import os

class HotelService:
    def __init__(self):
        data_path = os.path.join(
            os.path.dirname(__file__), '..', 'data', 'hotels.json'
        )
        with open(os.path.normpath(data_path), 'r') as f:
            self.hotels_data = json.load(f)

    def search_hotels(self, city, budget_per_night=None, min_rating=None):
        city_map = {
            "bengaluru": "Bangalore", "bangalore": "Bangalore",
            "bombay": "Mumbai", "mumbai": "Mumbai",
        }
        city = city_map.get(city.lower(), city.title())
        res = [h for h in self.hotels_data
            if h['city'].lower() == city.lower()]
        if budget_per_night is not None:
            res = [h for h in res if h['price_per_night'] <= budget_per_night]
        if min_rating is not None:
            res = [h for h in res if h['rating'] >= min_rating]
        res.sort(key=lambda x: -x['rating'])
        return res