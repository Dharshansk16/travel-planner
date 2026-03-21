class CombineNode:

    def process(self, state):
        flight = state.get("selected_flight") or state.get("flight", [{}])[0]
        hotel = state.get("selected_hotel") or state.get("hotels", [{}])[0]

        state["final_data"] = {
            "destination": state.get("dest"),
            "flight": flight,
            "hotel": hotel,
            "places": state.get("places", []),
            "weather": state.get("weather"),
            "budget": state.get("budget"),
            "total_cost": state.get("total_cost", 0)
        }

        return state