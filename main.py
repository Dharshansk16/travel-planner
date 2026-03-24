import sys
sys.path.insert(0, "packages/travel_agent/src")

from langchain_core.messages import HumanMessage
from travel_agent.agent.graph import app

def run_agent(user_input: str, memory: dict = None):
    return app.invoke({
        "messages":    [HumanMessage(content=user_input)],
        "user_input":  user_input,
        "dest":        None,
        "budget":      None,
        "weather":     None,
        "rating":      None,
        "duration":    None,
        "travel_date": None,
        "source":      None,
        "flight":      [],
        "hotels":      [],
        "places":      [],
        "final_data":  None,
        "final_answer": None,
        "memory":      memory or {},
    })

def get_last_ai_message(result):
    for m in reversed(result.get("messages", [])):
        if hasattr(m, "type") and m.type == "ai":
            return m.content
    return None

def main():
    print("\n" + "="*50)
    print("   TRAVEL PLANNER AI AGENT")
    print("="*50)
    print("Type 'quit' to exit\n")

    memory = {}

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "bye"):
            print("Goodbye! Safe travels!")
            break

        print("\n--- Planning your trip... ---\n")
        result = run_agent(user_input, memory)

        # Keep asking clarifications until we get a final answer
        for _ in range(3):
            answer = result.get("final_answer")
            if answer:
                print(answer)
                memory = {"source": "Bangalore"}
                break

            last_ai = get_last_ai_message(result)
            if last_ai and "ACTION" not in last_ai:
                print(f"Agent: {last_ai}\n")
                clarification = input("You: ").strip()
                if clarification.lower() in ("quit", "exit", "bye"):
                    print("Goodbye! Safe travels!")
                    sys.exit(0)
                combined = f"{user_input}. {clarification}"
                result   = run_agent(combined, memory)
            else:
                break
        else:
            print("Sorry, could not complete the plan. Please try again.")

if __name__ == "__main__":
    main()