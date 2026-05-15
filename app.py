from fastapi import FastAPI, HTTPException

from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware

import random
 
app = FastAPI(title="Predictive Maintenance API")
 


app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)
 
# -----------------------------

# Models

# -----------------------------

class SensorInput(BaseModel):

    machine_id: str

    temperature: float

    vibration: float

    pressure: float
 
class CostInput(BaseModel):

    machine_id: str

    failure_type: str
 
# -----------------------------

# Sample Machine Data

# -----------------------------

machines = [

    {"machine_id": "MC1", "machine_name": "Extruder", "status": "Healthy", "health_score": 92},

    {"machine_id": "MC2", "machine_name": "Gear Box", "status": "Warning", "health_score": 68},
    {"machine_id": "MC3", "machine_name": "Mortor", "status": "Healthy", "health_score": 90},
    {"machine_id": "MC3", "machine_name": "Screw Conveyor", "status": "Healthy", "health_score": 90},

]
 
# -----------------------------

# Get all machines

# -----------------------------

@app.get("/api/v1/machines")

def get_machines():

    return machines
 
# -----------------------------

# Get single machine

# -----------------------------

@app.get("/api/v1/machines/{machine_id}")

def get_machine(machine_id: str):

    for machine in machines:

        if machine["machine_id"] == machine_id:

            return machine


@app.post("/api/v1/predictions/failure")

def predict_failure(data: SensorInput):
 
    score = (data.temperature * 0.3) + (data.vibration * 20) + (data.pressure * 0.2)
 
    if score > 120:

        risk = "High"

        days = 5

    elif score > 80:

        risk = "Medium"

        days = 15

    else:

        risk = "Low"

        days = 30
 
    return {

        "machine_id": data.machine_id,

        "failure_risk": risk,

        "probability": round(random.uniform(0.65, 0.95), 2),

        "days_remaining": days

    }
 
# -----------------------------

# Repair Cost Estimation

# -----------------------------

@app.post("/api/v1/costs/estimate")

def estimate_cost(data: CostInput):
 
    cost_map = {

        "Bearing Damage": 12500,

        "Motor Failure": 25000,

        "Pump Leakage": 8000

    }
 
    return {

        "machine_id": data.machine_id,

        "failure_type": data.failure_type,

        "repair_cost": cost_map.get(data.failure_type, 10000),

        "currency": "INR"

    }
 
# -----------------------------

# Dashboard Summary

# -----------------------------

@app.get("/api/v1/dashboard/summary")

def dashboard_summary():

    return {

        "total_machines": len(machines),

        "healthy": 1,

        "warning": 1,

        "critical": 0

    }
 
# -----------------------------

# Alerts

# -----------------------------

@app.get("/api/v1/alerts")

def alerts():

    return [

        {"machine_id": "MC2", "alert": "High vibration detected"},
        {"machine_id": "MC1", "alert": "Low vibration detected"}

    ]
 