from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class Vessel(BaseModel):
    name: str
    imo_number: str
    
class Company(BaseModel):
    name: str
    company_id: Optional[str] = None
    vessels: List[Vessel] = []
    
class Incident(BaseModel):
    date: str
    description: str
    severity: str
    
class Claim(BaseModel):
    date: str
    amount: float
    status: str
    description: str
    
class History(BaseModel):
    incidents: List[Incident] = []
    claims: List[Claim] = []
    
class InsuranceDetails(BaseModel):
    coverage_percentage: float
    premium_amount: Optional[float] = None
    coverage_type: str
    
class RiskAssessment(BaseModel):
    risk_score: int = Field(ge=1, le=10)
    company_description: str
    case_description: str
    recommendation: str
    
class DatabaseEntry(BaseModel):
    """Final model for database entry"""
    company: Company
    vessels: List[Vessel]
    insurance: InsuranceDetails
    company_history: History
    vessel_histories: Dict[str, History]  # IMO number -> History
    assessment: RiskAssessment