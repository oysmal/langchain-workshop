
from typing import Dict, List, TypedDict
from src.information_extractor import EntityData, FinancialData, InsuranceData
from src.risk_assessor import Assessment
from src.models import CompanyHistoryEntry, DatabaseEntry, VesselHistoryEntry
from langchain_core.documents import Document

class WorkflowState(TypedDict, total=False):
    pdf_paths: List[str]
    text_paths: List[str]
    excel_paths: List[str]
    documents: List[Document]
    entity_data: EntityData
    financial_data: FinancialData
    insurance_data: InsuranceData
    company_history: CompanyHistoryEntry
    vessel_histories: Dict[str, VesselHistoryEntry]
    assessment: Assessment
