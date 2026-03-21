import json
class HotelService:
    def __init__(self):
        with open("travel_mcp/data/hotels.json", "r") as f:
            self.fetched_hotels = json.load(f)
    
    def search_hotel(self, destination: str, budget=None):
        
        res = [
            hotel for hotel in self.fetched_hotels
            if hotel["city"].lower()== destination.lower()
        ]
        if budget is not None:
            res = [hotel for hotel in res if hotel["price"] <= budget]
        return res
