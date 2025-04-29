from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, TypeVar, Any
from langchain_core.documents import Document

from src.models import RiskCategories

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

class ContactInfo(BaseModel):
    name: Optional[str] = Field(description="Contact name")
    role: Optional[str] = Field(description="Contact role")
    email: Optional[str] = Field(description="Contact email")
    phone: Optional[str] = Field(description="Contact phone number")

class AgreementInfo(BaseModel):
    id: Optional[str] = Field(description="Agreement identifier")
    name: Optional[str] = Field(description="Agreement name")
    start_date: Optional[str] = Field(description="Start date of agreement validity")
    end_date: Optional[str] = Field(description="End date of agreement validity")
    products: Optional[List[str]] = Field(description="List of insurance products")
    our_share: Optional[str] = Field(description="Our share percentage")
    installments: Optional[int] = Field(description="Number of installments")
    conditions: Optional[str] = Field(description="Agreement conditions")

class PremiumInfo(BaseModel):
    gross_premium: Optional[float] = Field(description="Gross premium amount")
    brokerage_percent: Optional[float] = Field(description="Brokerage percentage")
    net_premium: Optional[float] = Field(description="Net premium amount")

class AccountingInfo(BaseModel):
    paid: Optional[float] = Field(description="Amount paid")
    amount_due: Optional[float] = Field(description="Amount due")
    remaining: Optional[float] = Field(description="Remaining amount")
    balance_percent: Optional[float] = Field(description="Balance percentage")

class LossRatioInfo(BaseModel):
    value_percent: Optional[float] = Field(description="Loss ratio percentage value")
    claims: Optional[float] = Field(description="Claims amount")
    premium: Optional[float] = Field(description="Premium amount")

class RiskInfo(BaseModel):
    technical_condition: Optional[int] = Field(description="Technical condition risk score (1-10)")
    operational_quality: Optional[int] = Field(description="Operational quality risk score (1-10)")
    crew_quality: Optional[int] = Field(description="Crew quality risk score (1-10)")
    management_quality: Optional[int] = Field(description="Management quality risk score (1-10)")
    claims_history: Optional[int] = Field(description="Claims history risk score (1-10)")
    financial_stability: Optional[int] = Field(description="Financial stability risk score (1-10)")
    risk_categories: Optional[RiskCategories] = Field(description="Risk values for specific categories")

class ReinsuranceInfo(BaseModel):
    net_tty: Optional[float] = Field(description="Net TTY amount")
    net_fac: Optional[float] = Field(description="Net FAC amount")
    net_retention: Optional[float] = Field(description="Net retention amount")
    commission: Optional[float] = Field(description="Commission percentage")

# Combined schema models for more efficient extraction
class EntityData(BaseModel):
    company_info: Optional[CompanyInfo] = Field(description="Company information")
    vessel_info: Optional[List[VesselInfo]] = Field(description="Vessel information")
    contact_info: Optional[List[ContactInfo]] = Field(description="Contact information")

class FinancialData(BaseModel):
    premium_info: Optional[PremiumInfo] = Field(description="Premium information")
    accounting_info: Optional[AccountingInfo] = Field(description="Accounting information")
    loss_ratio_info: Optional[LossRatioInfo] = Field(description="Loss ratio information")

class InsuranceRiskData(BaseModel):
    agreement_info: Optional[AgreementInfo] = Field(description="Agreement information")
    risk_info: Optional[RiskInfo] = Field(description="Risk assessment information")
    reinsurance_info: Optional[ReinsuranceInfo] = Field(description="Reinsurance information")
    insurance_offer: Optional[InsuranceOffer] = Field(description="Insurance offer details")

class InformationExtractor:
    def __init__(self, model_name="gpt-4.1"):
        self.llm = ChatOpenAI(model=model_name)

    T = TypeVar('T', bound=BaseModel)

    def _create_extraction_chain(self, schema_class: type[T]) -> Any:
        """Create an extraction chain for the given schema class

        Args:
            schema_class: A Pydantic model class to use for extraction

        Returns:
            A runnable chain that extracts information according to the schema and returns an instance of schema_class
        """
        prompt = ChatPromptTemplate.from_template(
            """Extract the following information from the text below. The text may include content from PDF documents,
            text files, and Excel spreadsheets, so please process all formats to find the requested information.

            You must identify the monetary resolution of each amount, e.g. Actual amount (1), 1 Million, 1 Billion.
            When responding you should always provide the full information in standard (actual amount) resolution.
            You must transform the amount if it is not in standard resolution.

            {format_instructions}

            Text: {input}"""
        )

        chain = (
            {"input": RunnablePassthrough(), "format_instructions": lambda _: f"Extract information about {schema_class.__name__}"}
            | prompt
            | self.llm.with_structured_output(schema_class)
        )

        return chain

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
        extraction_chain = self._create_extraction_chain(EntityData)
        text_content = "\n\n".join([doc.page_content for doc in documents])
        results = extraction_chain.invoke(text_content)
        return self._ensure_pydantic_model(results, EntityData)

    def extract_financial_data(self, documents: List[Document]) -> FinancialData:
        """Extract financial information including premium, accounting, and loss ratio

        Args:
            documents: List of LangChain document objects

        Returns:
            Extracted financial data
        """
        extraction_chain = self._create_extraction_chain(FinancialData)
        text_content = "\n\n".join([doc.page_content for doc in documents])
        results = extraction_chain.invoke(text_content)
        return self._ensure_pydantic_model(results, FinancialData)

    def extract_insurance_risk_data(self, documents: List[Document]) -> InsuranceRiskData:
        """Extract insurance and risk information including agreement, risk assessment, reinsurance, and offer

        Args:
            documents: List of LangChain document objects

        Returns:
            Extracted insurance and risk data
        """
        extraction_chain = self._create_extraction_chain(InsuranceRiskData)
        text_content = "\n\n".join([doc.page_content for doc in documents])
        results = extraction_chain.invoke(text_content)
        return self._ensure_pydantic_model(results, InsuranceRiskData)
