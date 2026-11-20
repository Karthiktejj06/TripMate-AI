import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from agents.destination_agent import run as destination_run
from agents.hotel_agent import run as hotel_run
from agents.transport_agent import run as transport_run
from agents.budget_agent import run as budget_run
from agents.itinerary_agent import run as itinerary_run
from utils.llm import LLMError

load_dotenv()

app = FastAPI(title="TripMate AI", version="1.0.0",
              description="A multi-agent AI travel planning assistant.")
app.mount("/static", StaticFiles(directory="static"), name="static")

class TripRequest(BaseModel):
    origin: str = Field(min_length=2, max_length=100)
    destination: str = Field(default="", max_length=100)
    dates: str = Field(default="", max_length=100)
    days: int = Field(ge=1, le=30)
    travellers: int = Field(ge=1, le=20)
    budget: float = Field(gt=0, le=100000000)
    currency: str = Field(default="INR", min_length=3, max_length=5)
    preferences: str = Field(default="", max_length=500)

@app.get("/", response_class=HTMLResponse)
def home():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/health")
def health():
    return {"status": "ok", "service": "TripMate AI"}

@app.post("/api/plan")
def create_plan(request: TripRequest):
    trip = request.model_dump()
    try:
        # Agents run in sequence so later agents can use earlier findings.
        destination_notes = destination_run(trip)
        destination = trip["destination"].strip() or _extract_recommendation(destination_notes)
        if not destination:
            destination = "the recommended destination from the destination analysis"
        hotel_notes = hotel_run(trip, destination)
        transport_notes = transport_run(trip, destination)
        budget_notes = budget_run(trip, destination)
        itinerary_notes = itinerary_run(
            trip, destination, destination_notes, hotel_notes,
            transport_notes, budget_notes
        )
        return {
            "destination": destination,
            "agents": [
                {"name": "Destination Agent", "icon": "🧭", "content": destination_notes},
                {"name": "Hotel Agent", "icon": "🏨", "content": hotel_notes},
                {"name": "Transport Agent", "icon": "🚆", "content": transport_notes},
                {"name": "Budget Agent", "icon": "💰", "content": budget_notes},
                {"name": "Itinerary Agent", "icon": "🗓️", "content": itinerary_notes},
            ],
        }
    except LLMError as exc:
        raise HTTPException(status_code=502, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Trip planning failed: {exc}")

def _extract_recommendation(text: str) -> str:
    """Best-effort destination extraction; avoids depending on a fixed LLM format."""
    for line in text.splitlines():
        clean = line.strip().lstrip("#-*0123456789. ")
        low = clean.lower()
        for prefix in ("recommended destination:", "recommendation:", "my recommendation is"):
            if low.startswith(prefix):
                return clean[len(prefix):].strip().strip("*")
    return ""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
