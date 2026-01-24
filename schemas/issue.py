from pydantic import BaseModel
from typing import Optional, List


class Issue(BaseModel):
    id: Optional[int] = None
    issue_type: str
    confidence: float
    status: str
    bbox: Optional[List[int]] = None
    source: str
    lat: Optional[float] = None
    lng: Optional[float] = None
    timestamp: Optional[str] = None
    priority: Optional[str] = None
    assignedTo: Optional[str] = None
    notes: Optional[str] = None
