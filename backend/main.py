import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

app = FastAPI(title="IncidentMind API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY")
HINDSIGHT_BASE_URL = os.getenv(
    "HINDSIGHT_BASE_URL",
    "https://api.hindsight.vectorize.io"
)
HINDSIGHT_BANK_ID = os.getenv(
    "HINDSIGHT_BANK_ID",
    "incidentmind"
)

client = None

if HINDSIGHT_API_KEY:
    client = Hindsight(
        base_url=HINDSIGHT_BASE_URL,
        api_key=HINDSIGHT_API_KEY
    )


@app.get("/")
def home():
    return {
        "project": "IncidentMind",
        "status": "running",
        "memory": "Hindsight"
    }


@app.post("/analyze")
def analyze_incident(incident: dict):

    description = incident.get("description", "").strip()

    if not description:
        return {
            "status": "error",
            "message": "Please provide an incident description."
        }

    if client is None:
        return {
            "status": "error",
            "message": "Hindsight API key is not configured."
        }

    try:
        # Store the current incident in Hindsight
        client.retain(
            bank_id=HINDSIGHT_BANK_ID,
            content=f"Production incident: {description}"
        )

        # Search for similar incidents from memory
        result = client.recall(
            bank_id=HINDSIGHT_BANK_ID,
            query=description,
            limit=5
        )

        memories = []

        for memory in result.results:
            memories.append({
                "type": memory.type,
                "text": memory.text
            })

        return {
            "status": "success",
            "incident": description,
            "similar_incidents": memories,
            "message": "Incident stored and similar incidents recalled from Hindsight."
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
