class GenerateNode:

    def process(self, state):
        data = state.get("final_data", {})

        if not data.get("places"):
            state["final_answer"] = "😔 No good travel options found."
            return state

        answer = f"""
🌴 Trip Plan to {data['destination']}

💰 Budget: ₹{data['budget']}
💸 Total Cost: ₹{data['total_cost']}

✈️ Flight:
{data['flight']}

🏨 Hotel:
{data['hotel']}

📍 Places to Visit:
"""

        for place in data["places"]:
            answer += f"- {place['name']} ⭐{place['rating']}\n"

        answer += f"\n☀️ Weather: {data['weather']}\n"
        answer += "\nEnjoy your trip! 🎉"

        state["final_answer"] = answer
        return state