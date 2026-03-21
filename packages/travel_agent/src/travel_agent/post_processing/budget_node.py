class BudgetNode:

    def process(self, state):
        flights = state.get("flight", [])
        hotels = state.get("hotels", [])

        if not flights or not hotels:
            state["within_budget"] = False
            return state

        flight_cost = flights[0].get("cost", 0)
        hotel_cost = hotels[0].get("cost", 0)

        total = flight_cost + hotel_cost

        state["total_cost"] = total
        state["within_budget"] = total <= (state.get("budget") or 0)

        return state