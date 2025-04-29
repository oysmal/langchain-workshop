from langchain_openai import ChatOpenAI
from langchain.output_parsers.openai_functions import PydanticOutputFunctionsParser
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from pydantic import BaseModel, Field
from typing import List, Optional, Dict

# Define extraction schemas using Pydantic
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

# New extraction schemas for the updated structure
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
    values_by_id: Optional[Dict[str, int]] = Field(description="Risk values indexed by ID")

class ReinsuranceInfo(BaseModel):
    net_tty: Optional[float] = Field(description="Net TTY amount")
    net_fac: Optional[float] = Field(description="Net FAC amount")
    net_retention: Optional[float] = Field(description="Net retention amount")
    commission: Optional[float] = Field(description="Commission percentage")

class ContactInfo(BaseModel):
    name: Optional[str] = Field(description="Contact name")
    role: Optional[str] = Field(description="Contact role")
    email: Optional[str] = Field(description="Contact email")
    phone: Optional[str] = Field(description="Contact phone number")

class ObjectInfo(BaseModel):
    name: Optional[str] = Field(description="Object name (e.g., company, vessel, etc.)")

class InformationExtractor:
    def __init__(self, model_name="gpt-4.1"):
        self.llm = ChatOpenAI(model=model_name)

    def _create_extraction_chain(self, schema_class):
        """Create an extraction chain for the given schema class"""
        # Define the extraction prompt
        prompt = ChatPromptTemplate.from_template(
            """Extract the following information from the text below. The text may include content from PDF documents,
            text files, and Excel spreadsheets, so please process all formats to find the requested information.

            {format_instructions}

            Text: {input}"""
        )

        chain = (
            {"input": RunnablePassthrough(), "format_instructions": lambda _: f"Extract information about {schema_class.__name__}"}
            | prompt
            | self.llm.with_structured_output(schema_class)
        )

        return chain

    def extract_company_info(self, documents):
        """Extract company information from documents"""
        extraction_chain = self._create_extraction_chain(CompanyInfo)
        text_content = "\n\n".join([doc.page_content for doc in documents])
        results = extraction_chain.invoke(text_content)
        # Return as list to maintain compatibility with the rest of the code
        return [results]

    def extract_vessel_info(self, documents):
        """Extract vessel information including IMO numbers"""
        extraction_chain = self._create_extraction_chain(VesselInfo)
        text_content = "\n\n".join([doc.page_content for doc in documents])

        # For vessel info, we might have multiple vessels, so we'll use a different approach
        # First, extract a single vessel to see if it works
        result = extraction_chain.invoke(text_content)

        # Return as list to maintain compatibility with the rest of the code
        return [result]

    def extract_insurance_offer(self, documents):
        """Extract insurance offer details"""
        extraction_chain = self._create_extraction_chain(InsuranceOffer)
        text_content = "\n\n".join([doc.page_content for doc in documents])
        results = extraction_chain.invoke(text_content)
        # Return as list to maintain compatibility with the rest of the code
        return [results]

    def extract_agreement_info(self, documents):
        """Extract agreement information from documents"""
        extraction_chain = self._create_extraction_chain(AgreementInfo)
        text_content = "\n\n".join([doc.page_content for doc in documents])
        results = extraction_chain.invoke(text_content)
        # Return as list to maintain compatibility with the rest of the code
        return [results]

    def extract_premium_info(self, documents):
        """Extract premium information from documents"""
        extraction_chain = self._create_extraction_chain(PremiumInfo)
        text_content = "\n\n".join([doc.page_content for doc in documents])
        results = extraction_chain.invoke(text_content)
        # Return as list to maintain compatibility with the rest of the code
        return [results]

    def extract_accounting_info(self, documents):
        """Extract accounting information from documents"""
        extraction_chain = self._create_extraction_chain(AccountingInfo)
        text_content = "\n\n".join([doc.page_content for doc in documents])
        results = extraction_chain.invoke(text_content)
        # Return as list to maintain compatibility with the rest of the code
        return [results]

    def extract_loss_ratio_info(self, documents):
        """Extract loss ratio information from documents"""
        extraction_chain = self._create_extraction_chain(LossRatioInfo)
        text_content = "\n\n".join([doc.page_content for doc in documents])
        results = extraction_chain.invoke(text_content)
        # Return as list to maintain compatibility with the rest of the code
        return [results]

    def extract_risk_info(self, documents):
        """Extract risk information from documents"""
        extraction_chain = self._create_extraction_chain(RiskInfo)
        text_content = "\n\n".join([doc.page_content for doc in documents])
        results = extraction_chain.invoke(text_content)
        # Return as list to maintain compatibility with the rest of the code
        return [results]

    def extract_reinsurance_info(self, documents):
        """Extract reinsurance information from documents"""
        extraction_chain = self._create_extraction_chain(ReinsuranceInfo)
        text_content = "\n\n".join([doc.page_content for doc in documents])
        results = extraction_chain.invoke(text_content)
        # Return as list to maintain compatibility with the rest of the code
        return [results]

    def extract_contact_info(self, documents):
        """Extract contact information from documents"""
        extraction_chain = self._create_extraction_chain(ContactInfo)
        text_content = "\n\n".join([doc.page_content for doc in documents])
        results = extraction_chain.invoke(text_content)
        # Return as list to maintain compatibility with the rest of the code
        return [results]

    def extract_objects(self, documents):
        """Extract object information from documents"""
        extraction_chain = self._create_extraction_chain(ObjectInfo)
        text_content = "\n\n".join([doc.page_content for doc in documents])

        # For objects, we might have multiple entries, so we'll use a different approach
        # First, extract a single object to see if it works
        result = extraction_chain.invoke(text_content)

        # Return as list to maintain compatibility with the rest of the code
        return [result]
