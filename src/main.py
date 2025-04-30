from langgraph.graph import StateGraph, END, START
from src.document_processor import DocumentProcessor
from src.information_extractor import InformationExtractor
from src.history_lookup import VesselHistoryClient, CompanyHistoryClient
from src.risk_assessor import Assessor
from src.models import DatabaseEntry
from src.workflow_state import WorkflowState
from src.utils import get_vessel_objects, safe_model_dump


"""Step 1: Process Documents"""
def process_documents(state: WorkflowState):
    """Process the documents and add them to the state"""
    processor = DocumentProcessor()
    documents = processor.process_documents(
        pdf_paths=state.get("pdf_paths", []),
        text_paths=state.get("text_paths", []),
        excel_paths=state.get("excel_paths", [])
    )
    return {"documents": documents}

def extract_information(state: WorkflowState):
    """Extract key information from the documents"""
    extractor = InformationExtractor()

    entity_data = extractor.extract_entity_data(state["documents"])
    financial_data = extractor.extract_financial_data(state["documents"])
    insurance_data = extractor.extract_insurance_data(state["documents"])

    # Return all extracted data
    return {
        "entity_data": entity_data,
        "financial_data": financial_data,
        "insurance_data": insurance_data
    }
"""/Step 1: Process Documents"""

"""Step 2: Lookup History"""
def lookup_history(state: WorkflowState):
    """Look up vessel and company history"""
    vessel_client = VesselHistoryClient()
    company_client = CompanyHistoryClient()

    # Get entity data with safe default
    entity_data = state.get("entity_data", {})
    
    # Handle CompanyInfo with safe access
    company_info = entity_data.company_info
    company_name = company_info.company_name if company_info else "Unknown Company"
    company_history = company_client.get(company_name)

    # Handle vessel info with simplified approach
    vessel_histories = {}
    if entity_data.vessel_info:
        vessel_histories = {
            vessel.imo_number: vessel_client.get(vessel.imo_number)
            for vessel in entity_data.vessel_info
        }

    return {
        "company_history": company_history,
        "vessel_histories_lookup": vessel_histories,
    }
"""/Step 2: Lookup History"""

"""Step 3: Assess Case and Create Database Entry"""

def create_db_entry(state: WorkflowState):
    """Create the final database entry"""
    
    # Extract data from state with safe defaults
    entity_data = state.get("entity_data", None)
    financial_data = state.get("financial_data", {})
    insurance_data = state.get("insurance_data", {})
    
    # Create db_entry_data dictionary with all components
    db_entry_data = {
        "agreement": safe_model_dump(insurance_data.agreement_info),
        "premium": safe_model_dump(financial_data.premium_info),
        "loss_ratio": safe_model_dump(financial_data.loss_ratio_info),
        "risk": safe_model_dump(insurance_data.risk_info),
        "objects": get_vessel_objects(entity_data),
        "reinsurance": safe_model_dump(insurance_data.reinsurance_info),
        "contacts": [contact.model_dump() for contact in entity_data.contact_info] if entity_data.contact_info else [],
        "recommendation": state["assessment"].recommendation if "assessment" in state else None,
        "risk_breakdown": state["assessment"].risk_breakdown if "assessment" in state else None,
        "overall_risk_score": state["assessment"].overall_risk_score if "assessment" in state else None,
        "points_of_attention": state["assessment"].points_of_attention if "assessment" in state else None,
        "request_summary": state["assessment"].request_summary if "assessment" in state else None,
    }
    
    # Create the database entry using model_validate
    db_entry = DatabaseEntry.model_validate(db_entry_data)
    
    return {"db_entry": db_entry}

def create_workflow():
    """Create the LangGraph workflow"""
    # Create the graph
    workflow = StateGraph(WorkflowState)

    # Add nodes
    workflow.add_node("process_documents", process_documents)
    workflow.add_node("extract_information", extract_information)
    workflow.add_node("lookup_history", lookup_history)
    workflow.add_node("assess", Assessor().assess_case)
    workflow.add_node("create_db_entry", create_db_entry)

    # Add edges
    workflow.add_edge(START, "process_documents")
    workflow.add_edge("process_documents", "extract_information")
    workflow.add_edge("extract_information", "lookup_history")
    workflow.add_edge("lookup_history", "assess")
    workflow.add_edge("assess", "create_db_entry")
    workflow.add_edge("create_db_entry", END)

    # Compile the graph
    return workflow.compile()

def main():
    # Create the workflow
    workflow = create_workflow()

    # Define input paths with absolute paths from project root
    inputs = {
        "pdf_paths": [
            "src/data/Bergen_Shipping_Company_Presentation_Final3.pdf",
            "src/data/Maritime_Reinsurance_Contract.pdf",
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

if __name__ == "__main__":
    main()
