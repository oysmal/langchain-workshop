from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class RiskAssessment(BaseModel):
    risk_score: int = Field(description="Overall risk score from 1-10, where 10 is highest risk")
    company_description: str = Field(description="Brief description of the company")
    case_description: str = Field(description="Summary of the insurance case")
    recommendation: str = Field(description="Recommendation on whether to accept the insurance offer")
    loss_ratio_percent: Optional[int] = Field(None, description="Loss ratio percentage")
    values_by_id: Optional[Dict[str, int]] = Field(default_factory=dict, description="Risk values by category ID")

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

        You must provide your assessment with all of the following required fields:
        - risk_score: Overall Risk Score (1-10, where 10 is highest risk)
        - company_description: Brief description of the company (2-3 sentences)
        - case_description: Summary of the insurance case (2-3 sentences)
        - recommendation: Your recommendation (Accept/Reject/Request More Information)
        - loss_ratio_percent: Loss Ratio Percentage (0-100)
        - values_by_id: Risk values for specific categories as a dictionary with these keys:
          "04": Technical condition (1-10)
          "08": Operational quality (1-10)
          "12": Crew quality (1-10)
          "14": Management quality (1-10)
          "16": Claims history (1-10)
          "18": Financial stability (1-10)

        All fields are required, do not omit any fields in your response.
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

        result = self.risk_chain.invoke({
            "company_info": str(company_info),
            "vessel_info": str(vessel_info),
            "insurance_offer": str(insurance_offer),
            "company_history": str(company_history),
            "vessel_history": str(vessel_history)
        })

        # Convert to RiskAssessment if it's a dict
        if isinstance(result, dict):
            assessment = RiskAssessment(**result)
        else:
            assessment = result

        return assessment
