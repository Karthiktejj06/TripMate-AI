# TripMate AI — Multi-Agent Travel Planner

TripMate AI is a Python + FastAPI web application that uses five specialized AI agents powered by Groq to create a travel plan.

## Features

- **Destination Agent:** suggests destinations or analyses the destination entered by the user.
- **Hotel Agent:** recommends suitable areas and accommodation categories.
- **Transport Agent:** explains intercity and local transport options.
- **Budget Agent:** allocates the total trip budget across major categories.
- **Itinerary Agent:** combines the earlier agents' outputs into a day-by-day plan.
- **FastAPI web interface:** enter trip details in a browser and view clearly separated agent results.

## Project structure

```text
TripMate-AI/
├── agents/
│   ├── __init__.py
│   ├── destination_agent.py
│   ├── hotel_agent.py
│   ├── transport_agent.py
│   ├── budget_agent.py
│   └── itinerary_agent.py
├── utils/
│   ├── __init__.py
│   └── llm.py
├── static/
│   └── index.html
├── tests/
│   └── test_validation.py
├── .env.example
├── .gitignore
├── main.py
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.10 or newer
- A Groq API key

## Setup on Windows (PowerShell)

1. Extract the ZIP and open the `TripMate-AI` folder in VS Code.
2. Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. Create your environment file:

```powershell
Copy-Item .env.example .env
```

5. Open `.env` and replace `your_groq_api_key_here` with your Groq API key. Do not share or upload this file.

6. Start the web server:

```powershell
uvicorn main:app --reload
```

7. Open this address in your browser:

```text
http://127.0.0.1:8000
```

API health check: `http://127.0.0.1:8000/health`

## Setup on Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Add your Groq API key to .env
uvicorn main:app --reload
```

## How the system works

```text
User enters trip details in browser
              |
              v
        FastAPI endpoint
              |
              v
       Destination Agent
              |
              v
          Hotel Agent
              |
              v
        Transport Agent
              |
              v
         Budget Agent
              |
              v
        Itinerary Agent
              |
              v
    Results displayed in browser
```

The agents run sequentially. The Itinerary Agent receives the findings of the previous agents and uses them to create a consolidated plan.

## API

`POST /api/plan`

Example JSON body:

```json
{
  "origin": "Hyderabad",
  "destination": "Goa",
  "dates": "12-16 December",
  "days": 4,
  "travellers": 2,
  "budget": 25000,
  "currency": "INR",
  "preferences": "beaches, local food and sightseeing"
}
```

## Important notes

- The application generates recommendations using an LLM; it does not make reservations.
- Prices, travel times, hotel suggestions and schedules are estimates or general guidance, not verified live data.
- Check official sources before booking.
- Keep your Groq API key in `.env`. Never commit `.env` to GitHub.
- The project uses the Groq model configured by `GROQ_MODEL`, defaulting to `openai/gpt-oss-120b`.

## Troubleshooting

**`GROQ_API_KEY is missing`**  
Make sure `.env` exists in the project root and contains a valid key.

**Groq authentication or model error**  
Check that your API key is valid and that the model configured in `.env` is available to your account.

**Port 8000 is already in use**  
Run `uvicorn main:app --reload --port 8001` and open `http://127.0.0.1:8001`.

**Module not found**  
Activate the virtual environment and run `pip install -r requirements.txt` again.
