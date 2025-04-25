from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List, Dict, Any

class RiskAssessment(BaseModel):
    risk_score: int = Field(description="Risk score from 1-10, where 10 is highest risk")
    company_description: str = Field(description="Brief description of the company")
    case_description: str = Field(description="Summary of the insurance case")
    recommendation: str = Field(description="Recommendation on whether to accept the insurance offer")

class RiskAssessor:
    def __init__(self, model_name="gpt-3.5-turbo"):
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
        
        self.risk_chain = LLMChain(llm=self.llm, prompt=self.risk_template)
    
    def generate_assessment(self, 
                           company_info: Dict, 
                           vessel_info: Dict, 
                           insurance_offer: Dict,
                           company_history: Dict,
                           vessel_history: Dict) -> RiskAssessment:
        """Generate a risk assessment based on all available information"""
        
        result = self.risk_chain.invoke({
            "company_info": str(company_info),
            "vessel_info": str(vessel_info),
            "insurance_offer": str(insurance_offer),
            "company_history": str(company_history),
            "vessel_history": str(vessel_history)
        })
        
        # Parse the LLM output into structured format
        # This is simplified for the tutorial - in a real app, we'd use more robust parsing
        lines = result["text"].strip().split("\n")
        risk_score = int([l for l in lines if "Risk Score" in l][0].split(":")[-1].strip())
        company_desc = [l for l in lines if "Company Description" in l][0].split(":")[-1].strip()
        case_desc = [l for l in lines if "Case Description" in l][0].split(":")[-1].strip()
        recommendation = [l for l in lines if "Recommendation" in l][0].split(":")[-1].strip()
        
        return RiskAssessment(
            risk_score=risk_score,
            company_description=company_desc,
            case_description=case_desc,
            recommendation=recommendation
        )