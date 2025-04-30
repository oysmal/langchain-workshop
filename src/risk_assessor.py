from typing import Dict
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from src.models import Assessment
from src.workflow_state import WorkflowState

class Assessor:
    def __init__(self, model_name="gpt-4.1"):
        self.llm = ChatOpenAI(model=model_name)

        # TODO: Add the prompt template here, accepting all the available information we have from state
        # TODO: Construct the chain and ensure the output is structure to be of type Assessment

        self.chain = self.prompt | self.llm.with_structured_output(Assessment)

    def assess_case(self, state: WorkflowState) -> Dict[str, Assessment]:
        """Assess the case and generate insights"""

        # TODO: Fill out the input data for the chain
        input_data = {
            "company_info": state["entity_data"].company_info,
            "vessel_info": [vessel.model_dump() for vessel in state["entity_data"].vessel_info],
        }

        assessment = self.chain.invoke(input_data)
        return {"assessment": assessment} # Matches the workflow state
