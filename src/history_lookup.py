# Import mock data for demonstration
from src.data.mock_data import VESSEL_HISTORY, COMPANY_HISTORY
from src.models import CompanyClaimHistory, CompanyHistoryEntry, VesselClaimHistory, Incident, VesselHistoryEntry


class VesselHistoryClient():
    name: str = "vessel_history_lookup"
    description: str = "Look up incident history and claims for a vessel by IMO number"

    def get(self, imo_number: str, vessel_name: str = None):
        """Look up vessel history from mock data"""
        if imo_number in VESSEL_HISTORY:
            data = VESSEL_HISTORY[imo_number]
            incidents = [Incident(**incident) for incident in data.get("incidents", [])]
            claims = []
            for claim in data.get("claims", []):
                claims.append(VesselClaimHistory(
                    claim_vessel_imo=imo_number,
                    claim_vessel_name=vessel_name,
                    claim_amount=claim.get("amount", 0),
                    claim_date=claim.get("date", ""),
                    claim_description=claim.get("description", "")))
            return VesselHistoryEntry(incidents=incidents, claims=claims, message="History found")
        return VesselHistoryEntry(incidents=incidents, claims=claims, message="No history found for this imo number")

class CompanyHistoryClient():
    name: str = "company_history_lookup"
    description: str = "Look up history and claims for a shipping company"

    def get(self, company_name: str):
        """Look up company history from mock data"""
        for company in COMPANY_HISTORY:
            if company_name.lower() in company.lower():
                data = COMPANY_HISTORY[company]
                incidents = [Incident(**incident) for incident in data.get("incidents", [])]
                claims = []
                for claim in data.get("claims", []):
                    claims.append(CompanyClaimHistory(
                        claim_company_name=company,
                        claim_amount=claim.get("amount", 0),
                        claim_date=claim.get("date", ""),
                        claim_description=claim.get("description", "")))
                return CompanyHistoryEntry(incidents=incidents, claims=claims, message="History found")
        return CompanyHistoryEntry(incidents=[], claims=[], message="No history found for this company")
