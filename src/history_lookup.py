from langchain.tools import BaseTool
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

# Import mock data for demonstration
from src.data.mock_data import VESSEL_HISTORY, COMPANY_HISTORY

class IncidentRecord(BaseModel):
    date: str
    description: str
    severity: str

class ClaimsRecord(BaseModel):
    date: str
    amount: float
    status: str
    description: str

class VesselHistoryInput(BaseModel):
    imo_number: str = Field(description="The IMO number of the vessel to look up")

class CompanyHistoryInput(BaseModel):
    company_name: str = Field(description="The name of the company to look up")

class VesselHistoryTool(BaseTool):
    name: str = "vessel_history_lookup"
    description: str = "Look up incident history and claims for a vessel by IMO number"
    args_schema: type = VesselHistoryInput
    
    def _run(self, imo_number: str):
        """Look up vessel history from mock data"""
        if imo_number in VESSEL_HISTORY:
            return VESSEL_HISTORY[imo_number]
        return {"incidents": [], "claims": [], "message": "No history found for this IMO number"}

class CompanyHistoryTool(BaseTool):
    name: str = "company_history_lookup"
    description: str = "Look up history and claims for a shipping company"
    args_schema: type = CompanyHistoryInput
    
    def _run(self, company_name: str):
        """Look up company history from mock data"""
        # Try case-insensitive match
        for company in COMPANY_HISTORY:
            if company_name.lower() in company.lower():
                return COMPANY_HISTORY[company]
        return {"incidents": [], "claims": [], "message": "No history found for this company"}