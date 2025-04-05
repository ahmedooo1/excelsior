from fastapi import FastAPI, HTTPException
from dto import RepairDTO
from models import Repair
from repositories import InMemoryRepairRepository
from typing import List
import requests

app = FastAPI(
    title="Repair Service API",
    description="API for managing repairs",
    version="1.0.0"
)

repair_repository = InMemoryRepairRepository()
USER_SERVICE_URL = "http://user-service:8001"
PROVIDER_SERVICE_URL = "http://provider-service:8005"

def verify_user_exists(user_id: str) -> bool:
    response = requests.get(f"{USER_SERVICE_URL}/api/users/{user_id}")
    return response.status_code == 200

def verify_provider_exists(provider_id: str) -> bool:
    response = requests.get(f"{PROVIDER_SERVICE_URL}/api/providers/{provider_id}")
    return response.status_code == 200

@app.post("/api/repairs", response_model=RepairDTO)
def create_repair(repair: RepairDTO):
    if not verify_user_exists(repair.user_id):
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_provider_exists(repair.provider_id):
        raise HTTPException(status_code=404, detail="Provider not found")
    
    new_repair = Repair(
        repair_id=repair.repair_id,
        provider_id=repair.provider_id,
        user_id=repair.user_id,
        description=repair.description,
        status=repair.status
    )
    return repair_repository.create_repair(new_repair)

@app.get("/api/repairs/{repair_id}", response_model=RepairDTO)
def get_repair(repair_id: str):
    repair = repair_repository.get_repair_by_id(repair_id)
    if not repair:
        raise HTTPException(status_code=404, detail="Repair not found")
    return repair

@app.put("/api/repairs/{repair_id}", response_model=RepairDTO)
def update_repair(repair_id: str, repair: RepairDTO):
    existing_repair = repair_repository.get_repair_by_id(repair_id)
    if not existing_repair:
        raise HTTPException(status_code=404, detail="Repair not found")
    
    updated_repair = Repair(
        repair_id=repair.repair_id,
        provider_id=repair.provider_id,
        user_id=repair.user_id,
        description=repair.description,
        status=repair.status
    )
    return repair_repository.update_repair(repair_id, updated_repair)

@app.get("/api/users/{user_id}/repairs", response_model=List[RepairDTO])
def get_user_repairs(user_id: str):
    if not verify_user_exists(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return repair_repository.get_repairs_by_user_id(user_id)

@app.get("/api/providers/{provider_id}/repairs", response_model=List[RepairDTO])
def get_provider_repairs(provider_id: str):
    if not verify_provider_exists(provider_id):
        raise HTTPException(status_code=404, detail="Provider not found")
    return repair_repository.get_repairs_by_provider_id(provider_id)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8006)