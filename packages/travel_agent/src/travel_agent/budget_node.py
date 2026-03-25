class BudgetNode:
    def process(self, state):
        flights  = state.get("flight", [])
        hotels   = state.get("hotels", [])
        budget   = state.get("budget") or 0
        duration = state.get("duration", 1)

        
        if not flights or not hotels:
            state["within_budget"] = False
            state["message"] = "No flights or hotels available for these dates."
            state["places"] = []  
            return state

        best_flight = None
        best_hotel  = None
        best_total  = float("inf")

       
        for flight in flights:
            f_cost = flight.get("price", 0)
            for hotel in hotels:
                h_cost = hotel.get("price_per_night", 0) * duration
                total = f_cost + h_cost
               
                if total <= budget and total < best_total:
                    best_total  = total
                    best_flight = flight
                    best_hotel  = hotel

       
        if not best_flight:
            state["within_budget"] = False
            state["message"] = f"Calculated cost (INR {best_total if best_total != float('inf') else 'N/A'}) exceeds your budget of INR {budget}."
            state["places"] = []  
            return state
        else:
            state["within_budget"]    = True
            state["selected_flight"]  = best_flight
            state["selected_hotel"]   = best_hotel
            state["total_cost"]       = best_total
            state["message"]          = f"Plan found within budget: INR {best_total}."

        return state