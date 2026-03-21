class OptimizeNode:

    def process(self, state):
        flights = sorted(state.get("flight", []), key=lambda x: x.get("cost", 0))
        hotels = sorted(state.get("hotels", []), key=lambda x: x.get("cost", 0))

        budget = state.get("budget", 0)

        for f in flights:
            for h in hotels:
                total = f.get("cost", 0) + h.get("cost", 0)

                if total <= budget:
                    state["selected_flight"] = f
                    state["selected_hotel"] = h
                    state["total_cost"] = total
                    state["within_budget"] = True
                    return state

        # fallback → cheapest combo
        if flights and hotels:
            state["selected_flight"] = flights[0]
            state["selected_hotel"] = hotels[0]
            state["total_cost"] = flights[0]["cost"] + hotels[0]["cost"]
            state["within_budget"] = False

        return state