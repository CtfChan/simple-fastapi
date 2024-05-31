from pydantic import BaseModel
from enum import Enum

class StateEnum(str, Enum):
    pending = 'PENDING'
    reached_out = 'REACHED_OUT'

class LeadSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    resume_url: str
    state: StateEnum = StateEnum.pending

 