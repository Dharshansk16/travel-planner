class FilterNode:

    def process(self, state):
        data = state.get("final_data", {})
        places = data.get("places", [])
        weather = data.get("weather")
        min_rating = state.get("rating") or 0

        filtered = []
        seen = set()

        for p in places:
            name = p.get("name")

            if name in seen:
                continue
            seen.add(name)

            if p.get("rating", 0) < min_rating:
                continue

            if weather and p.get("weather") != weather:
                continue

            filtered.append(p)

        # sort best first
        filtered.sort(key=lambda x: (-x.get("rating", 0), x.get("cost", 0)))

        state["final_data"]["places"] = filtered
        return state