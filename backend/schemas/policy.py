from pydantic import BaseModel
from datetime import datetime

class PolicyOut(BaseModel):
    id: int
    filename: str
    size: int
    uploaded_at: datetime

    model_config = {
        "from_attributes": True
    }