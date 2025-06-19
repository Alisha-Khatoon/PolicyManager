from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PolicyOut(BaseModel):
    id: int
    filename: str
    size: int
    uploaded_at: datetime

    model_config = {
        "from_attributes": True
    }

class PolicyDetailOut(BaseModel):
    id: int
    filename: str
    size: int
    uploaded_at: datetime
    content: str
    analysis: dict[str, str]
    ai_review: Optional[str]

    class Config:
        form_mode = True

