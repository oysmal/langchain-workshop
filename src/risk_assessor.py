from typing import Dict
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from src.models import Assessment
from src.workflow_state import WorkflowState

class Assessor:
    def __init__(self, model_name="gpt-4.1"):
        self.llm = ChatOpenAI(model=model_name)

        self.prompt = ChatPromptTemplate.from_template("""
        You are a maritime insurance expert. Based on the following information, provide:

        1. A concise summary of the underwriting request (2-3 sentences)
        2. A clear recommendation regarding the case (Accept/Reject/Request More Information with brief justification)
        3. An overall risk score from 1-10, where 10 is the highest risk
        4. A list of 3-5 specific points that the reviewer should pay attention to when reviewing this case

        Company Information:
        {company_info}

        Vessel Information:
        {vessel_info}

        Insurance Offer:
        {insurance_offer}

        Risk Assessment:
        {assessment}

        Agreement Details:
        {agreement}

        Premium Information:
        {premium}

        Risk Data:
        {risk}

        Format your response as follows:

        {model_schema}        

        """)

        self.chain = self.prompt | self.llm.with_structured_output(Assessment)


    def assess_case(self, state: WorkflowState) -> Dict[str, Assessment]:
        """Assess the case and generate insights"""

        # Extract data with safe defaults
        data = {
            "company_info": state["entity_data"].company_info,
            "vessel_info": [vessel.model_dump() for vessel in state["entity_data"].vessel_info],
            "insurance_offer": state["insurance_data"].insurance_offer,
            "assessment": state.get("assessment", {}),
            "agreement": state.get("agreement_data", {}),
            "premium": state.get("premium_data", {}),
            "risk": state["insurance_data"].risk_info
        }

        # Prepare the input data dictionary with string conversions
        input_data = {
            "company_info": str(data["company_info"]),
            "vessel_info": str(data["vessel_info"]),
            "insurance_offer": str(data["insurance_offer"]),
            "assessment": str(data["assessment"]),
            "agreement": str(data["agreement"]),
            "premium": str(data["premium"]),
            "risk": str(data["risk"]),
            "model_schema": Assessment.schema_json(indent=2)
        }

        assessment = self.chain.invoke(input_data)
        return {"assessment": assessment} # Matches the workflow state
