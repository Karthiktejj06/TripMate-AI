from utils.llm import generate_text

SYSTEM = """You are the Budget Agent in TripMate AI.
Create a transparent budget allocation. Check that categories add up to the
user's total budget. Use the requested currency and state assumptions."""

def run(trip: dict, destination: str) -> str:
    prompt = f"""Create a practical budget for this trip:
Origin: {trip['origin']}
Destination: {destination}
Duration: {trip['days']} days
Travellers: {trip['travellers']}
TOTAL budget for the whole group: {trip['budget']} {trip['currency']}
Preferences: {trip.get('preferences') or 'Not specified'}

Break down transport, stay, food, activities, local travel and emergency buffer.
Show amounts and percentages, ensure the total does not exceed the budget,
and say if the budget seems unrealistic. Do not imply prices are live."""
    return generate_text(SYSTEM, prompt)
