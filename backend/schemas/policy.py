from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class TokenSchema(BaseModel):
    access_token: str
    token_type: str

class PolicyOut(BaseModel):
    id: int
    filename: str
    uploaded_at: datetime
    category: Optional[str]
    industry: Optional[str]

    class Config:
        from_attributes  = True


class PolicyDetailOut(BaseModel):
    id: int
    filename: str
    size: int
    uploaded_at: datetime
    content: str
    analysis: Dict[str, str]
    ai_review: Optional[str]
    insights: Optional[Dict[str, Any]]
    category: Optional[str]
    industry: Optional[str]  # ✅ recently added

    class Config:
        from_attributes  = True
