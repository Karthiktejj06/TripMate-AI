from utils.llm import generate_text

SYSTEM = """You are the Destination Agent in TripMate AI.
Recommend suitable destinations based on the user's origin, budget, duration,
traveller count and interests. Be realistic, explain why each destination fits,
and clearly state assumptions. Do not invent live prices or availability."""

def run(trip: dict) -> str:
    prompt = f"""User trip details:
Origin: {trip['origin']}
Travel dates: {trip.get('dates') or 'Not specified'}
Duration: {trip['days']} days
Travellers: {trip['travellers']}
Total budget: {trip['budget']} {trip['currency']}
Interests/preferences: {trip.get('preferences') or 'Not specified'}
Preferred destination (if any): {trip.get('destination') or 'Suggest one'}

Suggest up to 3 destinations, or focus on the preferred destination.
For each: give fit, best experiences, approximate travel considerations,
and a short reason. End with one recommended destination."""
    return generate_text(SYSTEM, prompt)
