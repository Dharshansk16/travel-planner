import json
import os

class FlightService:
    def __init__(self):
        data_path = os.path.join(
            os.path.dirname(__file__), '..', 'data', 'flights.json'
        )
        with open(os.path.normpath(data_path), 'r') as f:
            self.flight_data = json.load(f)

    def search_flights(self, source, destination, date=None, budget=None):
        city_map = {
            "bengaluru": "Bangalore",
            "bangalore": "Bangalore",
            "bombay":    "Mumbai",
            "mumbai":    "Mumbai",
        }
        source_norm = city_map.get(
            source.lower(), source.title()) if source else source
        dest_norm   = city_map.get(
            destination.lower(), destination.title()) if destination else destination

        res = [f for f in self.flight_data
               if f['source'].lower()      == source_norm.lower()
               and f['destination'].lower() == dest_norm.lower()]

        if budget is not None:
            res = [f for f in res if f['price'] <= budget]

        res.sort(key=lambda x: x['price'])
        return res