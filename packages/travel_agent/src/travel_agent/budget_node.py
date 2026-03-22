class BudgetNode:
    def process(self, state):
        flights  = state.get("flight", [])
        hotels   = state.get("hotels", [])
        budget   = state.get("budget") or 0
        duration = state.get("duration", 1)

        if not flights and not hotels:
            state["within_budget"] = False
            return state

        best_flight = None
        best_hotel  = None
        best_total  = float("inf")

        # Check all flight + hotel combinations
        for flight in flights:
            flight_cost = flight.get("price", 0)
            for hotel in hotels:
                hotel_cost  = hotel.get("price_per_night", 0) * duration
                total       = flight_cost + hotel_cost
                # Pick cheapest combo that fits within budget
                if total <= budget and total < best_total:
                    best_total  = total
                    best_flight = flight
                    best_hotel  = hotel

        # If nothing fits budget, pick cheapest combo overall
        if not best_flight:
            all_combos = [
                (f, h, f.get("price", 0) + h.get("price_per_night", 0) * duration)
                for f in flights
                for h in hotels
            ]
            all_combos.sort(key=lambda x: x[2])
            if all_combos:
                best_flight, best_hotel, best_total = all_combos[0]

        state["selected_flight"]  = best_flight
        state["selected_hotel"]   = best_hotel
        state["total_cost"]       = best_total
        state["within_budget"]    = best_total <= budget

        return state