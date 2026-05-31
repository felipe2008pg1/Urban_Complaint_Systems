from pydantic import BaseModel

class ReportCreate(BaseModel):

    title: str
    description: str
    category: str
    latitude: float
    longitude: float