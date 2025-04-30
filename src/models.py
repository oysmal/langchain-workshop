from pydantic import BaseModel, Field
from typing import List, Optional, Dict

# New models for the updated structure
class Validity(BaseModel):
    """Validity period for an agreement"""
    start_date: Optional[str] = Field(None, description="Start date of the agreement")
    end_date: Optional[str] = Field(None, description="End date of the agreement")

class Agreement(BaseModel):
    """Insurance agreement details"""
    id: Optional[str] = Field(None, description="Agreement identifier")
    name: Optional[str] = Field(None, description="Agreement name")
    validity: Validity = Field(default_factory=Validity)
    products: List[str] = Field(default_factory=list, description="List of insurance products")
    our_share: Optional[str] = Field(None, description="Our share percentage")
    installments: Optional[int] = Field(None, description="Number of installments")
    conditions: Optional[str] = Field(None, description="Agreement conditions")

class Premium(BaseModel):
    """Premium information"""
    gross_premium: Optional[float] = Field(None, description="Gross premium amount")
    brokerage_percent: Optional[float] = Field(None, description="Brokerage percentage")
    net_premium: Optional[float] = Field(None, description="Net premium amount")

class LossRatio(BaseModel):
    """Loss ratio information"""
    value_percent: Optional[float] = Field(None, description="Loss ratio percentage value")
    claims: Optional[float] = Field(None, description="Claims amount")
    premium: Optional[float] = Field(None, description="Premium amount")

class VesselClaimHistory(BaseModel):
    claim_vessel_name: str = Field(description="Name of the vessel involved in the claim")
    claim_vessel_imo: str = Field(description="IMO number of the vessel involved in the claim")
    claim_date: str = Field(description="Date of the claim")
    claim_amount: float = Field(description="Claim amount in standard resolution")
    claim_description: str = Field(description="Description of the claim")

class CompanyClaimHistory(BaseModel):
    claim_company_name: str = Field(description="Name of the company involved in the claim")
    claim_date: str = Field(description="Date of the claim")
    claim_amount: float = Field(description="Claim amount in standard resolution")
    claim_description: str = Field(description="Description of the claim")

class RiskBreakdown(BaseModel):
    technical_condition: Optional[int] = Field(description="Technical condition risk score (1-10)")
    operational_quality: Optional[int] = Field(description="Operational quality risk score (1-10)")
    crew_quality: Optional[int] = Field(description="Crew quality risk score (1-10)")
    management_quality: Optional[int] = Field(description="Management quality risk score (1-10)")
    claims_history: Optional[int] = Field(description="Claims history risk score (1-10)")
    financial_stability: Optional[int] = Field(description="Financial stability risk score (1-10)")

class RiskInfo(BaseModel):
    claim_history: Optional[List[VesselClaimHistory]] = Field(description="List of claims related to the vessel")
    risk_score: Optional[int] = Field(description="Overall risk score (1-10)")
    
class Reinsurance(BaseModel):
    """Reinsurance information"""
    net_tty: Optional[float] = Field(None, description="Net TTY amount")
    net_fac: Optional[float] = Field(None, description="Net FAC amount")
    net_retention: Optional[float] = Field(None, description="Net retention amount")
    commission: Optional[float] = Field(None, description="Commission percentage")

class Contact(BaseModel):
    """Contact information"""
    name: Optional[str] = Field(None, description="Contact name")
    role: Optional[str] = Field(None, description="Contact role")
    email: Optional[str] = Field(None, description="Contact email")
    phone: Optional[str] = Field(None, description="Contact phone number")

class Incident(BaseModel):
    date: str = Field(description="Date of the incident")
    description: str = Field(description="Description of the incident")
    severity: str = Field(description="Severity of the incident (e.g., minor, major, critical)")

class VesselHistoryEntry(BaseModel):
    incidents: List[Incident] = Field(default_factory=list, description="List of incidents related to the vessel")
    claims: List[VesselClaimHistory] = Field(default_factory=list, description="List of claims related to the vessel")
    message: str = Field(default="", description="Message regarding the vessel history lookup")

class CompanyHistoryEntry(BaseModel):
    incidents: List[Incident] = Field(default_factory=list, description="List of incidents related to the company")
    claims: List[CompanyClaimHistory] =  Field(default_factory=list, description="List of claims related to the company")
    message: str = Field(default="", description="Message regarding the company history lookup")

# New DatabaseEntry
class DatabaseEntry(BaseModel):
    """Final model for database entry"""
    agreement: Agreement = Field(default_factory=Agreement)
    premium: Premium = Field(default_factory=Premium)
    loss_ratio: LossRatio = Field(default_factory=LossRatio)
    objects: List[Dict] = []  # Objects associated with this entry
    reinsurance: Reinsurance = Field(default_factory=Reinsurance)
    contacts: List[Contact] = []
    reported_vessel_claims_history: List[VesselClaimHistory] = Field(default_factory=list)  # Reported claims history for vessels
    verified_vessel_claims_history: Dict[str, VesselHistoryEntry] = Field(default_factory=dict)  # Verified claims history for vessels
    company_claims_history: CompanyHistoryEntry = Field(default_factory=CompanyHistoryEntry)  # Claims history for the company

    # Additional fields requested by the user
    overall_risk_score: Optional[int] = None  # Overall risk score from 1-10
    request_summary: Optional[str] = None  # Summary of the underwriting request
    recommendation: Optional[str] = None   # AI recommendation regarding the case
    points_of_attention: List[str] = []  # Points to pay attention to when reviewing
    risk_breakdown: RiskBreakdown = Field(default_factory=RiskBreakdown, description="Detailed risk breakdown")

