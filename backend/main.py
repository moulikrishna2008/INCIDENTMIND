from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="IncidentMind API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "project": "IncidentMind",
        "message": "AI Incident Response Agent is running"
    }


@app.post("/analyze")
def analyze_incident(incident: dict):
    description = incident.get("description", "")

    return {
        "status": "success",
        "incident": description,
        "message": "Incident received. Hindsight memory analysis will be connected next."
    }
