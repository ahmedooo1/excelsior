from typing import List, Optional
from models import Repair

class InMemoryRepairRepository:
    def __init__(self):
        self.repairs = {}

    def create_repair(self, repair: Repair) -> Repair:
        self.repairs[repair.repair_id] = repair
        return repair

    def get_repair_by_id(self, repair_id: str) -> Optional[Repair]:
        return self.repairs.get(repair_id)

    def update_repair(self, repair_id: str, repair: Repair) -> Optional[Repair]:
        if repair_id in self.repairs:
            self.repairs[repair_id] = repair
            return repair
        return None

    def list_repairs(self) -> List[Repair]:
        return list(self.repairs.values())

    def get_repairs_by_user_id(self, user_id: str) -> List[Repair]:
        return [repair for repair in self.repairs.values() if repair.user_id == user_id]

    def get_repairs_by_provider_id(self, provider_id: str) -> List[Repair]:
        return [repair for repair in self.repairs.values() if repair.provider_id == provider_id]