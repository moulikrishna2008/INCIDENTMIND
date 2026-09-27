import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

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

    return {
        "status": "success",
        "incident": description,
        "memory_bank": HINDSIGHT_BANK_ID,
        "message": "Incident received. Hindsight memory integration is ready."
    }
