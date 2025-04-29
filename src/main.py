from langgraph.graph import StateGraph, END, START
from typing import Dict, List, Any, TypedDict, Optional
from src.document_processor import DocumentProcessor
from src.information_extractor import InformationExtractor
from src.history_lookup import VesselHistoryTool, CompanyHistoryTool
from src.risk_assessor import RiskAssessor
from src.models import (DatabaseEntry, Validity, RiskCategories, AdditionalInsights)
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from src.utils import get_risk_categories, get_vessel_objects, safe_model_dump

def process_documents(state):
    """Process the documents and add them to the state"""
    processor = DocumentProcessor()
    documents = processor.process_documents(
        pdf_paths=state.get("pdf_paths", []),
        text_paths=state.get("text_paths", []),
        excel_paths=state.get("excel_paths", [])
    )
    return {"documents": documents}

def extract_information(state):
    """Extract key information from the documents"""
    extractor = InformationExtractor()

    # Extract data using consolidated extraction methods
    entity_data = extractor.extract_entity_data(state["documents"])
    financial_data = extractor.extract_financial_data(state["documents"])
    insurance_risk_data = extractor.extract_insurance_risk_data(state["documents"])

    # Return all extracted data
    return {
        "entity_data": entity_data,
        "financial_data": financial_data,
        "insurance_risk_data": insurance_risk_data
    }

def lookup_history(state):
    """Look up vessel and company history"""
    vessel_tool = VesselHistoryTool()
    company_tool = CompanyHistoryTool()

    # Get entity data with safe default
    entity_data = state.get("entity_data", {})
    
    # Handle CompanyInfo with safe access
    company_info = entity_data.company_info
    company_name = company_info.company_name if company_info else "Unknown Company"
    company_history = company_tool.run(company_name)

    # Handle vessel info with simplified approach
    vessel_histories = {}
    if entity_data.vessel_info:
        vessel_histories = {
            vessel.imo_number: vessel_tool.run(vessel.imo_number)
            for vessel in entity_data.vessel_info
        }

    return {
        "company_history": company_history,
        "vessel_histories": vessel_histories,
    }

def assess_risk(state):
    """Generate risk assessment with simplified data handling"""
    assessor = RiskAssessor()
    
    # Extract entity data with safe defaults
    entity_data = state.get("entity_data", {})
    insurance_risk_data = state.get("insurance_risk_data", {})
    
    # Get vessel info with simplified approach
    vessel_info = {}
    vessel_history = {}
    if entity_data.vessel_info:
        vessel_info = {v.imo_number: v.model_dump() for v in entity_data.vessel_info}
        vessel_history = {imo: state["vessel_histories"].get(imo, {}) for imo in vessel_info}
    
    # Get company and insurance info with simplified approach
    company_info = safe_model_dump(entity_data.company_info)
    insurance_offer = safe_model_dump(insurance_risk_data.insurance_offer)
    
    # Generate assessment
    assessment = assessor.generate_assessment(
        company_info=company_info,
        vessel_info=vessel_info,
        insurance_offer=insurance_offer,
        company_history=state.get("company_history", {}),
        vessel_history=vessel_history
    )
    
    return {"assessment": assessment}

def generate_additional_insights(state) -> AdditionalInsights:
    """Generate additional insights for the database entry"""
    llm = ChatOpenAI(model="gpt-4.1")

    # Extract data with safe defaults
    data = {
        "company_info": state["entity_data"].company_info,
        "vessel_info": state["entity_data"].vessel_info[0] if state["entity_data"].vessel_info else None,
        "insurance_offer": state["insurance_risk_data"].insurance_offer,
        "assessment": state.get("assessment", {}),
        "agreement": state.get("agreement_data", {}),
        "premium": state.get("premium_data", {}),
        "risk": state.get("risk_data", {})
    }

    # Create a prompt with improved template
    prompt = ChatPromptTemplate.from_template("""
    You are a maritime insurance expert. Based on the following information, provide:

    1. A concise summary of the underwriting request (2-3 sentences)
    2. A clear recommendation regarding the case (Accept/Reject/Request More Information with brief justification)
    3. A list of 3-5 specific points that the reviewer should pay attention to when reviewing this case

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

    REQUEST SUMMARY: [Your summary here]

    RECOMMENDATION: [Your recommendation here]

    POINTS OF ATTENTION:
    - [Point 1]
    - [Point 2]
    - [Point 3]
    - [Point 4 if applicable]
    - [Point 5 if applicable]
    """)

    # Prepare the input data dictionary with string conversions
    input_data = {
        "company_info": str(data["company_info"]),
        "vessel_info": str(data["vessel_info"]),
        "insurance_offer": str(data["insurance_offer"]),
        "assessment": str(data["assessment"]),
        "agreement": str(data["agreement"]),
        "premium": str(data["premium"]),
        "risk": str(data["risk"])
    }

    # Create and run the chain
    chain = prompt | llm.with_structured_output(AdditionalInsights)
    
    # Generate insights
    return chain.invoke(input_data)


def create_db_entry(state):
    """Create the final database entry model using simplified approach"""
    
    # Extract data from state with safe defaults
    entity_data = state.get("entity_data", {})
    financial_data = state.get("financial_data", {})
    insurance_risk_data = state.get("insurance_risk_data", {})
    
    # Create validity object directly from agreement_info
    agreement_info = insurance_risk_data.agreement_info
    validity = Validity(
        start_date=agreement_info.start_date if agreement_info else None,
        end_date=agreement_info.end_date if agreement_info else None
    )
    
    # Create agreement data using model_validate
    agreement_data = {}
    if agreement_info:
        agreement_data = agreement_info.model_dump()
        agreement_data["validity"] = validity.model_dump()
    
    # Create db_entry_data dictionary with all components
    db_entry_data = {
        "agreement": agreement_data,
        "premium": safe_model_dump(financial_data.premium_info),
        "loss_ratio": safe_model_dump(financial_data.loss_ratio_info),
        "risk": {"risk_categories": get_risk_categories(state)},
        "objects": get_vessel_objects(entity_data),
        "reinsurance": safe_model_dump(insurance_risk_data.reinsurance_info),
        "contacts": [contact.model_dump() for contact in entity_data.contact_info] if entity_data.contact_info else [],
    }
    
    # Generate additional insights
    insights = generate_additional_insights(state)
    db_entry_data.update({
        "request_summary": insights.request_summary,
        "recommendation": insights.recommendation,
        "points_of_attention": insights.points_of_attention,
    })
    
    # Create the database entry using model_validate
    db_entry = DatabaseEntry.model_validate(db_entry_data)
    
    return {"db_entry": db_entry}

# Define the state schema with more specific types
class WorkflowState(TypedDict, total=False):
    pdf_paths: List[str]
    text_paths: List[str]
    excel_paths: List[str]
    documents: List[Document]
    entity_data: Any  # Using Any for flexibility with Pydantic models
    financial_data: Any
    insurance_risk_data: Any
    company_history: Dict
    vessel_histories: Dict[str, Dict]
    assessment: Any
    db_entry: DatabaseEntry

def create_workflow():
    """Create the LangGraph workflow"""
    # Create the graph
    workflow = StateGraph(WorkflowState)

    # Add nodes
    workflow.add_node("process_documents", process_documents)
    workflow.add_node("extract_information", extract_information)
    workflow.add_node("lookup_history", lookup_history)
    workflow.add_node("assess_risk", assess_risk)
    workflow.add_node("create_db_entry", create_db_entry)

    # Add edges
    workflow.add_edge(START, "process_documents")
    workflow.add_edge("process_documents", "extract_information")
    workflow.add_edge("extract_information", "lookup_history")
    workflow.add_edge("lookup_history", "assess_risk")
    workflow.add_edge("assess_risk", "create_db_entry")
    workflow.add_edge("create_db_entry", END)

    # Compile the graph
    return workflow.compile()

def main():
    """Run the maritime insurance processing workflow"""
    # Create the workflow
    workflow = create_workflow()

    # Define input paths with absolute paths from project root
    inputs = {
        "pdf_paths": [
            "src/data/Bergen_Shipping_Company_Presentation_Final3.pdf",
            "src/data/Maritime_Insurance_Proposal2.pdf",
        ],
        "excel_paths": [
            "src/data/HM_2023-2024.xlsx",
            "src/data/LOH_2023-2024.xlsx",
        ],
        "text_paths": [
            "src/data/broker_email.txt"
        ]
    }

    # Execute the workflow
    result = workflow.invoke(inputs)

    # Get the database entry
    db_entry = result["db_entry"]

    # Convert to JSON and print
    db_entry_json = db_entry.model_dump_json(indent=2)
    print(db_entry_json)

    return db_entry

if __name__ == "__main__":
    main()
