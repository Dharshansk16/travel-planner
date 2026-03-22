import json
<<<<<<< HEAD
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
=======
from pathlib import Path


class FlightService:
    def __init__(self):
        data_file = Path(__file__).resolve().parent.parent / "data" / "flights.json"
        with data_file.open("r", encoding="utf-8") as f:
            self.flight_data = json.load(f)

    def search_flights(self, source, destination, date, budget=None):
        

        res = [
            flight for flight in self.flight_data
            if flight['source'].lower() == source.lower() and
               flight['destination'].lower() == destination.lower() and
             flight['date'] == date.isoformat()
        ]
        if budget is not None:
            res = [flight for flight in res if flight['price'] <= budget]
        return res

>>>>>>> c1cba09d19d71fcbe1eee273856dbeecffc70215
