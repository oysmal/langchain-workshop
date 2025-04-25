from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class RiskAssessment(BaseModel):
    risk_score: int = Field(description="Overall risk score from 1-10, where 10 is highest risk")
    values_by_id: Dict[str, int] = Field(description="Risk values by category ID", default_factory=dict)
    company_description: str = Field(description="Brief description of the company")
    case_description: str = Field(description="Summary of the insurance case")
    recommendation: str = Field(description="Recommendation on whether to accept the insurance offer")
    loss_ratio_percent: int = Field(description="Loss ratio percentage", default=0)

class RiskAssessor:
    def __init__(self, model_name="gpt-4.1"):
        self.llm = ChatOpenAI(model=model_name)
        
        self.risk_template = ChatPromptTemplate.from_template("""
        You are a maritime insurance risk assessor. Based on the following information, 
        provide a detailed risk assessment.
        
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
        - Overall Risk Score (1-10, where 10 is highest risk)
        - Risk values for specific categories:
          - 04: Technical condition (1-10)
          - 08: Operational quality (1-10)
          - 12: Crew quality (1-10)
          - 14: Management quality (1-10)
          - 16: Claims history (1-10)
          - 18: Financial stability (1-10)
        - Loss Ratio Percentage (0-100)
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
        assessment = self.risk_chain.invoke({
            "company_info": str(company_info),
            "vessel_info": str(vessel_info),
            "insurance_offer": str(insurance_offer),
            "company_history": str(company_history),
            "vessel_history": str(vessel_history)
        })
        
        # Ensure the values_by_id dictionary has the correct format
        if not hasattr(assessment, 'values_by_id') or not assessment.values_by_id:
            assessment.values_by_id = {
                "04": min(max(int(assessment.risk_score * 0.8), 1), 10),  # Technical condition
                "08": min(max(int(assessment.risk_score * 0.9), 1), 10),  # Operational quality
                "12": min(max(int(assessment.risk_score * 1.0), 1), 10),  # Crew quality
                "14": min(max(int(assessment.risk_score * 1.1), 1), 10),  # Management quality
                "16": min(max(int(assessment.risk_score * 1.2), 1), 10),  # Claims history
                "18": min(max(int(assessment.risk_score * 0.7), 1), 10)   # Financial stability
            }
        
        # Ensure the loss_ratio_percent is set
        if not hasattr(assessment, 'loss_ratio_percent') or assessment.loss_ratio_percent is None:
            # Default to a value based on risk score
            assessment.loss_ratio_percent = min(assessment.risk_score * 10, 100)
        
        return assessment