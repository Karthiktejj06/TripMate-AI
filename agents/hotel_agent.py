from utils.llm import generate_text

SYSTEM = """You are the Hotel Agent in TripMate AI.
Suggest accommodation areas and realistic hotel categories based on the trip.
Never claim to have checked live room availability. Label all prices as estimates."""

def run(trip: dict, destination: str) -> str:
    prompt = f"""Plan accommodation for:
Destination: {destination}
Duration: {trip['days']} nights (assume nights = days - 1 where appropriate)
Travellers: {trip['travellers']}
Total trip budget: {trip['budget']} {trip['currency']}
Preferences: {trip.get('preferences') or 'Not specified'}

Recommend 2-3 suitable areas or accommodation types, approximate nightly cost
ranges in {trip['currency']} if reasonably estimable, and practical booking tips.
Do not fabricate hotel names or live availability."""
    return generate_text(SYSTEM, prompt)
