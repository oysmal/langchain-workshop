from langchain_openai import ChatOpenAI
from langchain.output_parsers.openai_functions import PydanticOutputFunctionsParser
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from pydantic import BaseModel, Field
from typing import List, Optional

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

class InformationExtractor:
    def __init__(self, model_name="gpt-3.5-turbo"):
        self.llm = ChatOpenAI(model=model_name)
    
    def _create_extraction_chain(self, schema_class):
        """Create an extraction chain for the given schema class"""
        # Define the extraction prompt
        prompt = ChatPromptTemplate.from_template(
            """Extract the following information from the text below:
            
            {format_instructions}
            
            Text: {input}"""
        )
        
        # Create the extraction chain
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