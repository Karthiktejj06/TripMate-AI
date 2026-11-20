from utils.llm import generate_text

SYSTEM = """You are the Itinerary Agent in TripMate AI.
Build a clear, practical day-by-day itinerary using the prior agents' findings.
Avoid overpacking days. Include meal/rest breaks and useful travel tips."""

def run(trip: dict, destination: str, destination_notes: str,
        hotel_notes: str, transport_notes: str, budget_notes: str) -> str:
    prompt = f"""Create a {trip['days']}-day itinerary for {destination}.
Travellers: {trip['travellers']}
Dates: {trip.get('dates') or 'Not specified'}
Budget: {trip['budget']} {trip['currency']}
Interests: {trip.get('preferences') or 'Not specified'}

Destination research:
{destination_notes}

Accommodation guidance:
{hotel_notes}

Transport guidance:
{transport_notes}

Budget guidance:
{budget_notes}

Format day by day. For each day include morning, afternoon, evening, meal/rest
suggestions and local movement tips. Finish with a concise checklist and caveat
that opening times, fares and availability should be verified."""
    return generate_text(SYSTEM, prompt)
