from pydantic import BaseModel
from typing import Optional

class InputGuardRailOutput(BaseModel):

    is_off_topic: bool
    reason: str

class HandoffData(BaseModel):

    to_agent_name: str
    issue_type: str
    issue_description: str
    reason: str

class RestaurantContext(BaseModel):
    customer_id: int
    name: str
    current_order: Optional[str] = None

    def add_troubleshooting_step(self, step: str):
        pass