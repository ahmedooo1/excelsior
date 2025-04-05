
from fastapi import FastAPI, HTTPException
from dto import ProviderDTO
from models import Provider
from repositories import InMemoryProviderRepository
from typing import List

app = FastAPI(
    title="Provider Service API",
    description="API for managing service providers",
    version="1.0.0"
)
provider_repository = InMemoryProviderRepository()

@app.post("/api/providers", response_model=ProviderDTO)
def create_provider(provider: ProviderDTO):
    new_provider = Provider(
        provider_id=provider.provider_id,
        name=provider.name,
        services=provider.services,
        rating=provider.rating,
        availability=provider.availability
    )
    return provider_repository.create_provider(new_provider)

@app.get("/api/providers/{provider_id}", response_model=ProviderDTO)
def get_provider(provider_id: str):
    provider = provider_repository.get_provider_by_id(provider_id)
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    return provider

@app.put("/api/providers/{provider_id}", response_model=ProviderDTO)
def update_provider(provider_id: str, provider: ProviderDTO):
    updated_provider = Provider(
        provider_id=provider.provider_id,
        name=provider.name,
        services=provider.services,
        rating=provider.rating,
        availability=provider.availability
    )
    result = provider_repository.update_provider(provider_id, updated_provider)
    if not result:
        raise HTTPException(status_code=404, detail="Provider not found")
    return result

@app.get("/api/providers", response_model=List[ProviderDTO])
def list_providers():
    return provider_repository.list_providers()

@app.get("/api/providers/available", response_model=List[ProviderDTO])
def get_available_providers():
    return provider_repository.get_available_providers()

@app.put("/api/providers/{provider_id}/availability")
def update_provider_availability(provider_id: str, availability: bool):
    provider = provider_repository.update_availability(provider_id, availability)
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    return {"message": "Availability updated successfully"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)
