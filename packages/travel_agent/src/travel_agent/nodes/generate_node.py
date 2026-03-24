class GenerateNode:
    def process(self, state):
        data = state.get("final_data", {})

        if not data:
            state["final_answer"] = "Sorry, could not generate a travel plan."
            return state

        dest     = data.get("destination", "your destination")
        duration = data.get("duration", 1)
        budget   = data.get("budget", 0)
        source   = data.get("source", "Bangalore")
        flight   = data.get("flight", {})
        hotels   = data.get("hotels", [])
        places   = data.get("places", [])
        weather  = data.get("weather", "pleasant")

        answer = f"\n{'='*50}\n"
        answer += f"  TRAVEL PLAN: {source} → {dest}\n"
        answer += f"{'='*50}\n\n"
        answer += f"Duration : {duration} day(s)\n"
        answer += f"Budget   : INR {budget:,}\n"
        answer += f"Weather  : {weather}\n\n"

        answer += "--- FLIGHT ---\n"
        if flight:
            answer += (f"  {flight.get('airline','N/A')} | "
                       f"{flight.get('departure_time','')} → "
                       f"{flight.get('arrival_time','')} | "
                       f"INR {flight.get('price',0):,}\n\n")
        else:
            answer += "  No flights found within budget.\n\n"

        answer += "--- HOTELS (Top picks) ---\n"
        if hotels:
            for h in hotels[:2]:
                answer += (f"  {h.get('name','N/A')} | "
                           f"{h.get('location','')} | "
                           f"INR {h.get('price_per_night',0):,}/night | "
                           f"Rating: {h.get('rating',0)}\n")
        else:
            answer += "  No hotels found.\n"
        answer += "\n"

        answer += "--- PLACES TO VISIT ---\n"
        if places:
            for p in places[:5]:
                answer += (f"  {p.get('name','N/A')} | "
                           f"{p.get('category','')} | "
                           f"INR {p.get('cost',0)} | "
                           f"~{p.get('avg_time_spent',0)}hrs | "
                           f"Rating: {p.get('rating','N/A')}\n")
        else:
            answer += "  No places found.\n"

        answer += f"\nHave a wonderful trip to {dest}!\n"

        state["final_answer"] = answer
        state["memory"] = {
            "dest":     dest,
            "budget":   budget,
            "duration": duration,
            "source":   source,
        }
        return state