from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from pydantic import BaseModel, Field
from typing import List, Dict, Any

class RiskAssessment(BaseModel):
    risk_score: int = Field(description="Risk score from 1-10, where 10 is highest risk")
    company_description: str = Field(description="Brief description of the company")
    case_description: str = Field(description="Summary of the insurance case")
    recommendation: str = Field(description="Recommendation on whether to accept the insurance offer")

class RiskAssessor:
    def __init__(self, model_name="gpt-4.1"):
        self.llm = ChatOpenAI(model=model_name)
        
        self.risk_template = ChatPromptTemplate.from_template("""
        You are a maritime insurance risk assessor. Based on the following information, 
        provide a risk assessment with a risk score from 1-10 (10 being highest risk),
        a brief company description, a case summary, and a recommendation.
        
        Company Information:
        {company_info}
        
        Vessel Information:
        {vessel_info}
        
        Insurance Offer:
        {insurance_offer}
        
        Company History:
        {company_history}
        
        Vessel History:
        {vessel_history}
        
        Provide your assessment in a structured format with the following fields:
        - Risk Score (1-10)
        - Company Description (2-3 sentences)
        - Case Description (2-3 sentences)
        - Recommendation (Accept/Reject/Request More Information)
        """)
        
        # Create a chain that automatically parses the output into the RiskAssessment model
        self.risk_chain = (
            {"company_info": RunnablePassthrough(),
             "vessel_info": RunnablePassthrough(),
             "insurance_offer": RunnablePassthrough(),
             "company_history": RunnablePassthrough(),
             "vessel_history": RunnablePassthrough()}
            | self.risk_template
            | self.llm.with_structured_output(RiskAssessment)
        )
    
    def generate_assessment(self, 
                           company_info: Dict, 
                           vessel_info: Dict, 
                           insurance_offer: Dict,
                           company_history: Dict,
                           vessel_history: Dict) -> RiskAssessment:
        """Generate a risk assessment based on all available information"""
        
        # The chain now directly returns a RiskAssessment object
        return self.risk_chain.invoke({
            "company_info": str(company_info),
            "vessel_info": str(vessel_info),
            "insurance_offer": str(insurance_offer),
            "company_history": str(company_history),
            "vessel_history": str(vessel_history)
        })