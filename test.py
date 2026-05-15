from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import random
from datetime import datetime

app = FastAPI(title="Predictive Maintenance API")

# -----------------------------
# CORS
# -----------------------------
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

class ConfigInput(BaseModel):
    machine_id: str
    date: str

class UserInput(BaseModel):
    name: str
    designation: str
    phone: str
    role: str

# -----------------------------
# In-memory DB (temporary)
# -----------------------------
machines = [
    {"machine_id": "MC1", "machine_name": "Extruder"},
    {"machine_id": "MC2", "machine_name": "Gear Box"},
    {"machine_id": "MC3", "machine_name": "Motor"},
    {"machine_id": "MC4", "machine_name": "Screw Conveyor"},
]

last_failure_data = {}
last_maintenance_data = {}
next_maintenance_data = {}
predicted_failure_data = {}

users = [
    {
        "name": "Himanshu Kumar",
        "designation": "Maintenance Engineer",
        "phone": "9876543210",
        "role": "Admin"
    },
    {
        "name": " Raj",
        "designation": "Production Supervisor",
        "phone": "9876501234",
        "role": "Manager"
    },
    {
        "name": "Tilak Verma",
        "designation": "Machine Operator",
        "phone": "9123456780",
        "role": "Operator"
    },
    {
        "name": "Ankitha Devi",
        "designation": "Quality Analyst",
        "phone": "9988776655",
        "role": "Viewer"
    },
    {
        "name": "Karthik Sai",
        "designation": "Electrical Technician",
        "phone": "9012345678",
        "role": "Technician"
    }
]

# -----------------------------
# MACHINE APIs
# -----------------------------
@app.get("/api/v1/machines")
def get_machines():
    return machines

@app.get("/api/v1/machines/{machine_id}")
def get_machine(machine_id: str):
    for m in machines:
        if m["machine_id"] == machine_id:
            return m
    raise HTTPException(status_code=404, detail="Machine not found")

# -----------------------------
# SENSOR APIs (FOR GRAPHS)
# -----------------------------
@app.get("/api/v1/sensors/live")
def get_live_sensors(machine_id: str):
    return {
        "machine_id": machine_id,
        "sensors": [
            {"sensor": "Sensor 1", "value": random.randint(50, 100)},
            {"sensor": "Sensor 2", "value": random.randint(40, 90)},
            {"sensor": "Sensor 3", "value": random.randint(30, 80)},
            {"sensor": "Sensor 4", "value": random.randint(20, 70)}
        ]
    }

@app.get("/api/v1/sensors/trend")
def sensor_trend(machine_id: str):
    return {
        "machine_id": machine_id,
        "data": [
            {"sensor": "Sensor 1", "value": 85},
            {"sensor": "Sensor 2", "value": 60},
            {"sensor": "Sensor 3", "value": 30},
            {"sensor": "Sensor 4", "value": 35}
        ]
    }

# -----------------------------
# HEALTH GRAPH
# -----------------------------
@app.get("/api/v1/health/components")
def component_health(machine_id: str):
    return {
        "machine_id": machine_id,
        "components": [
            {"name": "Sensor 1", "health": 94.5},
            {"name": "Sensor 2", "health": 62.1},
            {"name": "Sensor 3", "health": 92.0},
            {"name": "Sensor 4", "health": 24.9}
        ]
    }

# -----------------------------
# AI PREDICTION
# -----------------------------
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
# COST API
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
# DASHBOARD SUMMARY
# -----------------------------
@app.get("/api/v1/dashboard/summary")
def dashboard_summary():

    return {
        "total_machines": len(machines),
        "healthy": 2,
        "warning": 1,
        "critical": 1
    }

# -----------------------------
# ALERTS
# -----------------------------
@app.get("/api/v1/alerts")
def alerts():
    return [
        {"machine_id": "MC2", "alert": "High vibration detected"},
        {"machine_id": "MC1", "alert": "Low vibration detected"}
    ]

# -----------------------------
# CONFIG GET APIs (IMPORTANT)
# -----------------------------
@app.get("/api/v1/config/{machine_id}")
def get_config(machine_id: str):
    return {
        "machine_id": machine_id,
        "last_failure": last_failure_data.get(machine_id),
        "last_maintenance": last_maintenance_data.get(machine_id),
        "next_maintenance": next_maintenance_data.get(machine_id),
        "predicted_failure": predicted_failure_data.get(machine_id)
    }

# -----------------------------
# CONFIG UPDATE APIs
# -----------------------------
@app.post("/api/v1/config/last-failure")
def set_last_failure(data: ConfigInput):
    last_failure_data[data.machine_id] = data.date
    return {"message": "Last failure updated"}

@app.post("/api/v1/config/last-maintenance")
def set_last_maintenance(data: ConfigInput):
    last_maintenance_data[data.machine_id] = data.date
    return {"message": "Last maintenance updated"}

@app.post("/api/v1/config/next-maintenance")
def set_next_maintenance(data: ConfigInput):
    next_maintenance_data[data.machine_id] = data.date
    return {"message": "Next maintenance updated"}

@app.post("/api/v1/config/predicted-failure")
def set_predicted_failure(data: ConfigInput):
    predicted_failure_data[data.machine_id] = data.date
    return {"message": "Predicted failure updated"}

# -----------------------------
# USER MANAGEMENT
# -----------------------------
@app.get("/api/v1/users")
def get_users():
    return users

@app.post("/api/v1/users")
def create_user(user: UserInput):
    users.append(user.dict())
    return {"message": "User created"}

@app.delete("/api/v1/users/{index}")
def delete_user(index: int):
    if index >= len(users):
        raise HTTPException(status_code=404, detail="User not found")
    users.pop(index)
    return {"message": "User deleted"}