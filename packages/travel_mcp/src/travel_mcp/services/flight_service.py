import json


class FlightService:
    def __init__(self):
        with open('travel_mcp/data/flights.json', 'r') as f:
            self.flight_data = json.load(f)

    def search_flights(self, source, destination, date, budget=None):
        

        res = [
            flight for flight in self.flight_data
            if flight['source'] == source and
               flight['destination'] == destination and
               flight['date'] == date
        ]
        if budget is not None:
            res = [flight for flight in res if flight['price'] <= budget]
        return res

