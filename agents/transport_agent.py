from utils.llm import generate_text

SYSTEM = """You are the Transport Agent in TripMate AI.
Explain practical ways to reach and move around the destination. Distinguish
general guidance from live schedules/fares; do not claim live data."""

def run(trip: dict, destination: str) -> str:
    prompt = f"""Transport plan:
Starting point: {trip['origin']}
Destination: {destination}
Dates: {trip.get('dates') or 'Not specified'}
Travellers: {trip['travellers']}
Budget: {trip['budget']} {trip['currency']}
Preferences: {trip.get('preferences') or 'Not specified'}

Explain likely intercity options, local transport, pros/cons, and ways to save.
Give indicative costs only when sensible and clearly label them as estimates.
Mention that schedules and fares must be checked before booking."""
    return generate_text(SYSTEM, prompt)
