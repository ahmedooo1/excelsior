
class Provider:
    def __init__(self, provider_id: str, name: str, services: list, rating: float = 0.0, availability: bool = True):
        self.provider_id = provider_id
        self.name = name
        self.services = services
        self.rating = rating
        self.availability = availability
