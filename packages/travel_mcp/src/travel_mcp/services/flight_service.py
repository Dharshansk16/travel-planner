import json
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

