
from typing import Dict, List, TypedDict
from src.information_extractor import EntityData, FinancialData, InsuranceData
from src.models import CompanyHistoryEntry, VesselHistoryEntry
from langchain_core.documents import Document

class WorkflowState(TypedDict, total=False):
    pdf_paths: List[str]
    text_paths: List[str]
    excel_paths: List[str]
    documents: List[Document]
    entity_data: EntityData
    financial_data: FinancialData
    insurance_data: InsuranceData
    # TODO: Add company and vessel histories to state. Hint: VesselHistoryEntry should be the type of the value in a Dict
