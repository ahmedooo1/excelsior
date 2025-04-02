
from typing import List, Optional
from models import Provider

class InMemoryProviderRepository:
    def __init__(self):
        self.providers = {}

    def create_provider(self, provider: Provider) -> Provider:
        self.providers[provider.provider_id] = provider
        return provider

    def get_provider_by_id(self, provider_id: str) -> Optional[Provider]:
        return self.providers.get(provider_id)

    def update_provider(self, provider_id: str, provider: Provider) -> Optional[Provider]:
        if provider_id in self.providers:
            self.providers[provider_id] = provider
            return provider
        return None

    def list_providers(self) -> List[Provider]:
        return list(self.providers.values())

    def get_available_providers(self) -> List[Provider]:
        return [provider for provider in self.providers.values() if provider.availability]

    def update_availability(self, provider_id: str, availability: bool) -> Optional[Provider]:
        if provider_id in self.providers:
            self.providers[provider_id].availability = availability
            return self.providers[provider_id]
        return None
