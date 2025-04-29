from pydantic import BaseModel, Field
from typing import List, Optional, Dict

# New models for the updated structure
class Validity(BaseModel):
    """Validity period for an agreement"""
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class Agreement(BaseModel):
    """Insurance agreement details"""
    id: Optional[str] = None
    name: Optional[str] = None
    validity: Validity = Field(default_factory=Validity)
    products: List[str] = []
    our_share: Optional[str] = None
    installments: Optional[int] = None
    conditions: Optional[str] = None

class Premium(BaseModel):
    """Premium information"""
    gross_premium: Optional[float] = None
    brokerage_percent: Optional[float] = None
    net_premium: Optional[float] = None

class LossRatio(BaseModel):
    """Loss ratio information"""
    value_percent: Optional[float] = None
    claims: Optional[float] = None
    premium: Optional[float] = None

class VesselClaimHistory(BaseModel):
    claim_vessel_name: str = Field(description="Name of the vessel involved in the claim")
    claim_vessel_imo: str = Field(description="IMO number of the vessel involved in the claim")
    claim_date: str = Field(description="Date of the claim")
    claim_amount: float = Field(description="Claim amount in standard resolution")
    claim_description: str = Field(description="Description of the claim")

class RiskInfo(BaseModel):
    claim_history: Optional[List[VesselClaimHistory]] = Field(description="List of claims related to the vessel")
    technical_condition: Optional[int] = Field(description="Technical condition risk score (1-10)")
    operational_quality: Optional[int] = Field(description="Operational quality risk score (1-10)")
    crew_quality: Optional[int] = Field(description="Crew quality risk score (1-10)")
    management_quality: Optional[int] = Field(description="Management quality risk score (1-10)")
    claims_history: Optional[int] = Field(description="Claims history risk score (1-10)")
    financial_stability: Optional[int] = Field(description="Financial stability risk score (1-10)")
    risk_score: Optional[int] = Field(description="Overall risk score (1-10)")
class Reinsurance(BaseModel):
    """Reinsurance information"""
    net_tty: Optional[float] = None
    net_fac: Optional[float] = None
    net_retention: Optional[float] = None
    commission: Optional[float] = None

class Contact(BaseModel):
    """Contact information"""
    name: Optional[str] = None
    role: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

# New DatabaseEntry
class DatabaseEntry(BaseModel):
    """Final model for database entry"""
    agreement: Agreement = Field(default_factory=Agreement)
    premium: Premium = Field(default_factory=Premium)
    loss_ratio: LossRatio = Field(default_factory=LossRatio)
    risk: RiskInfo = Field(default_factory=RiskInfo)
    objects: List[Dict] = []  # Objects associated with this entry
    reinsurance: Reinsurance = Field(default_factory=Reinsurance)
    contacts: List[Contact] = []

    # Additional fields requested by the user
    overall_risk_score: Optional[int] = None  # Overall risk score from 1-10
    request_summary: Optional[str] = None  # Summary of the underwriting request
    recommendation: Optional[str] = None   # AI recommendation regarding the case
    points_of_attention: List[str] = []  # Points to pay attention to when reviewing


class Assessment(BaseModel):
    request_summary: str = Field(description="Summary of the underwriting request")
    recommendation: str = Field(description="AI recommendation regarding the case")
    overall_risk_score: int = Field(description="Overall risk score from 1-10")
    points_of_attention: List[str] = Field(description="List of points to pay attention to when reviewing")
