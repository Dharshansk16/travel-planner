class FilterNode:
    def process(self, state):
        places     = state.get("places", [])
        hotels     = state.get("hotels", [])
        flights    = state.get("flight", [])
        weather    = state.get("weather")
        min_rating = state.get("rating") or 0

        # Filter places
        filtered_places = []
        seen = set()
        for p in places:
            name = p.get("name")
            if name in seen:
                continue
            seen.add(name)
            if p.get("rating", 5) < min_rating:
                continue
            filtered_places.append(p)
        filtered_places.sort(key=lambda x: -x.get("rating", 0))

        # Filter hotels
        filtered_hotels = sorted(hotels, key=lambda x: -x.get("rating", 0))

        # Filter flights
        filtered_flights = sorted(flights, key=lambda x: x.get("price", 0))

        state["final_data"] = {
            "destination": state.get("dest"),
            "source":      state.get("source", "Bangalore"),
            "duration":    state.get("duration", 1),
            "places":      filtered_places[:5],
            "hotels":      filtered_hotels[:3],
            "flight":      filtered_flights[0] if filtered_flights else {},
            "weather":     weather,
            "budget":      state.get("budget"),
            "total_cost":  state.get("total_cost", 0)
        }
        return state