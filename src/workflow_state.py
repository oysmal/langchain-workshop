
from typing import Dict, List, TypedDict
from src.information_extractor import EntityData, FinancialData, InsuranceData
from langchain_core.documents import Document

class WorkflowState(TypedDict, total=False):
    pdf_paths: List[str]
    text_paths: List[str]
    excel_paths: List[str]
    documents: List[Document]
    # TODO: Add fields for the entity data, financial data, and insurance data
