from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from pydantic import BaseModel, Field
from typing import List, Optional, TypeVar, Any
from langchain_core.documents import Document

from src.models import Agreement, Premium, LossRatio, Reinsurance, Contact, VesselClaimHistory

# Base schemas for combined extraction models
class CompanyInfo(BaseModel):
    company_name: str = Field(description="The name of the shipping company")
    company_id: Optional[str] = Field(description="Company identifier if available")

class VesselInfo(BaseModel):
    vessel_name: str = Field(description="The name of the vessel")
    imo_number: str = Field(description="The IMO number of the vessel")

class InsuranceOffer(BaseModel):
    coverage_percentage: float = Field(description="Percentage of total insurance being offered")
    premium_amount: Optional[float] = Field(description="The premium amount if specified")
    coverage_type: str = Field(description="Type of insurance coverage")

    # Models for grouped extraction
class EntityData(BaseModel):
    company_info: Optional[CompanyInfo] = Field(description="Company information")
    vessel_info: Optional[List[VesselInfo]] = Field(description="Vessel information")
    contact_info: Optional[List[Contact]] = Field(description="Contact information")
    claim_history: Optional[List[VesselClaimHistory]] = Field(description="List of claims related to the vessels")

class FinancialData(BaseModel):
    premium_info: Optional[Premium] = Field(description="Premium information")
    loss_ratio_info: Optional[LossRatio] = Field(description="Loss ratio information")

class InsuranceData(BaseModel):
    agreement_info: Optional[Agreement] = Field(description="Agreement information")
    reinsurance_info: Optional[Reinsurance] = Field(description="Reinsurance information")
    insurance_offer: Optional[InsuranceOffer] = Field(description="Insurance offer details")

class InformationExtractor:
    def __init__(self, model_name="gpt-4.1"):
        self.llm = ChatOpenAI(model=model_name)

    T = TypeVar('T', bound=BaseModel)

    def _ensure_pydantic_model(self, result: Any, model_class: type[T]) -> T:
        """Ensure the result is a Pydantic model of the specified class

        Args:
            result: The result to convert if necessary
            model_class: The Pydantic model class

        Returns:
            An instance of the specified Pydantic model class
        """
        if isinstance(result, dict):
            return model_class.model_validate(result)
        return result

    def extract_entity_data(self, documents: List[Document]) -> EntityData:
        """Extract entity information including company, vessel, contact, and objects

        Args:
            documents: List of LangChain document objects

        Returns:
            Extracted entity data
        """
        text_content = "\n\n".join([doc.page_content for doc in documents])
        # TODO: Implement the extraction chain.
        # You must create a prompt template and use the llm with structured output of the correct type
        # in order to extract the information. 
        results = None
        return self._ensure_pydantic_model(results, EntityData)

    def extract_financial_data(self, documents: List[Document]) -> FinancialData:
        """Extract financial information including premium and loss ratio

        Args:
            documents: List of LangChain document objects

        Returns:
            Extracted financial data
        """
        text_content = "\n\n".join([doc.page_content for doc in documents])
        # TODO: Implement the extraction chain.
        # You must create a prompt template and use the llm with structured output of the correct type
        # in order to extract the information. 
        results = None
        return self._ensure_pydantic_model(results, EntityData)

    def extract_insurance_data(self, documents: List[Document]) -> InsuranceData:
        """Extract insurance information including agreement, reinsurance, and offer

        Args:
            documents: List of LangChain document objects

        Returns:
            Extracted insurance information
        """
        text_content = "\n\n".join([doc.page_content for doc in documents])
        # TODO: Implement the extraction chain.
        # You must create a prompt template and use the llm with structured output of the correct type
        # in order to extract the information. 
        results = None
        return self._ensure_pydantic_model(results, EntityData)
