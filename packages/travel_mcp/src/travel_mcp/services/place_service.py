import json

class PlaceService:
    def __init__(self):
        with open('travel_mcp/data/places.json', 'r') as f:
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