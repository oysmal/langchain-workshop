from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union

# Legacy models - kept for backward compatibility
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

# Legacy DatabaseEntry - kept for backward compatibility
class LegacyDatabaseEntry(BaseModel):
    """Legacy model for database entry"""
    company: Company
    vessels: List[Vessel]
    insurance: InsuranceDetails
    company_history: History
    vessel_histories: Dict[str, History]  # IMO number -> History
    assessment: RiskAssessment

# New models for the updated structure
class Validity(BaseModel):
    """Validity period for an agreement"""
    start_date: str = ""
    end_date: str = ""

class Agreement(BaseModel):
    """Insurance agreement details"""
    id: str = ""
    name: str = ""
    validity: Validity = Field(default_factory=Validity)
    products: List[str] = []
    our_share: str = "0%"
    installments: int = 1
    conditions: str = ""

class Premium(BaseModel):
    """Premium information"""
    gross_premium: int = 0
    brokerage_percent: int = 0
    net_premium: int = 0

class Accounting(BaseModel):
    """Accounting information"""
    paid: int = 0
    amount_due: int = 0
    remaining: int = 0
    balance_percent: int = 0

class LossRatio(BaseModel):
    """Loss ratio information"""
    value_percent: int = 0
    claims: Optional[float] = None
    premium: Optional[float] = None

class Risk(BaseModel):
    """Risk assessment values by category ID"""
    values_by_id: Dict[str, int] = Field(default_factory=dict)

class Reinsurance(BaseModel):
    """Reinsurance information"""
    net_tty: int = 0
    net_fac: Optional[int] = None
    net_retention: int = 0
    commission: Optional[float] = None

class Contact(BaseModel):
    """Contact information"""
    name: str = ""
    role: str = ""
    email: str = ""
    phone: str = ""

# New DatabaseEntry
class DatabaseEntry(BaseModel):
    """Final model for database entry"""
    agreement: Agreement = Field(default_factory=Agreement)
    premium: Premium = Field(default_factory=Premium)
    accounting: Accounting = Field(default_factory=Accounting)
    loss_ratio: LossRatio = Field(default_factory=LossRatio)
    risk: Risk = Field(default_factory=Risk)
    objects: List[str] = []
    reinsurance: Reinsurance = Field(default_factory=Reinsurance)
    contacts: List[Contact] = []
    
    # Additional fields requested by the user
    request_summary: str = ""  # Summary of the underwriting request
    recommendation: str = ""   # AI recommendation regarding the case
    points_of_attention: List[str] = []  # Points to pay attention to when reviewing