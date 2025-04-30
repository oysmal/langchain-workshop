# Import mock data for demonstration
from src.data.mock_data import VESSEL_HISTORY, COMPANY_HISTORY

class VesselHistoryClient():
    name: str = "vessel_history_lookup"
    description: str = "Look up incident history and claims for a vessel by IMO number"

    def get(self, imo_number: str):
        """Look up vessel history from mock data"""
        if imo_number in VESSEL_HISTORY:
            return VESSEL_HISTORY[imo_number]
        return {"incidents": [], "claims": [], "message": "No history found for this IMO number"}

class CompanyHistoryClient():
    name: str = "company_history_lookup"
    description: str = "Look up history and claims for a shipping company"

    def get(self, company_name: str):
        """Look up company history from mock data"""
        # Try case-insensitive match
        for company in COMPANY_HISTORY:
            if company_name.lower() in company.lower():
                return COMPANY_HISTORY[company]
        return {"incidents": [], "claims": [], "message": "No history found for this company"}
