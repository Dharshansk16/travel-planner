class FilterNode:
    def process(self, state):
        flights  = state.get("flight", [])
        hotels   = state.get("hotels", [])
        budget   = state.get("budget") or 0
        duration = state.get("duration", 1)
        min_rating = state.get("rating") or 0

      
        f_min = min([f.get("price", 0) for f in flights]) if flights else float('inf')
        h_min = min([h.get("price_per_night", 0) for h in hotels]) if hotels else float('inf')
        
       
        entry_cost = f_min + (h_min * duration)

       
        if entry_cost > budget or not flights or not hotels:
            print(f"[FilterNode] VIOLATION: Entry Cost {entry_cost} exceeds Budget {budget}")
            state["final_data"] = {
                "destination": state.get("dest"),
                "source":      state.get("source", "Bangalore"),
                "duration":    state.get("duration", 1),
                "places":      [],  
                "hotels":      [], 
                "flight":      {},
                "weather":     state.get("weather", "unknown"),
                "budget":      budget,
                "total_cost":  entry_cost if entry_cost != float('inf') else 0
            }
            return state

       
        raw_places = state.get("places", [])
        filtered_places = []
        seen = set()
        for p in raw_places:
            name = p.get("name")
            if name not in seen and p.get("rating", 0) >= min_rating:
                seen.add(name)
                filtered_places.append(p)
        
        filtered_places.sort(key=lambda x: x.get("rating", 0), reverse=True)

       
        filtered_hotels = sorted(hotels, key=lambda x: x.get("rating", 0), reverse=True)

        
        filtered_flights = sorted(flights, key=lambda x: x.get("price", 0))

        state["final_data"] = {
            "destination": state.get("dest"),
            "source":      state.get("source", "Bangalore"),
            "duration":    state.get("duration", 1),
            "places":      filtered_places[:5],
            "hotels":      filtered_hotels[:3],
            "flight":      filtered_flights[0] if filtered_flights else {},
            "weather":     state.get("weather", "unknown"),
            "budget":      budget,
            "total_cost":  entry_cost
        }
        
        print(f"[FilterNode] SUCCESS: Plan created within budget.")
        return state