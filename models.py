from pydantic import BaseModel
from typing import Optional

class InputGuardRailOutput(BaseModel):

    is_off_topic: bool
    reason: str

class OutputGuardRailOutput(BaseModel):

    is_violation: bool
    is_professional: bool
    reason: str

class HandoffData(BaseModel):

    to_agent_name: str
    issue_type: str
    issue_description: str
    reason: str

class RestaurantContext(BaseModel):
    customer_id: int
    name: str = "guest"
    current_order: Optional[str] = None

    model_config = {"arbitrary_types_allowed": True}

    def update_name(self, name: str):
        self.name = name  # ← 이름 업데이트 메서드