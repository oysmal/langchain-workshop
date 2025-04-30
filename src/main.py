from langgraph.graph import StateGraph, END, START
from src.document_processor import DocumentProcessor
from src.information_extractor import InformationExtractor
from src.history_lookup import VesselHistoryClient, CompanyHistoryClient
from src.workflow_state import WorkflowState


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

def lookup_history(state: WorkflowState):
    """Look up vessel and company history"""
    vessel_client = VesselHistoryClient()
    company_client = CompanyHistoryClient()

    return None

    # TODO: complete function

def create_workflow():
    """Create the LangGraph workflow"""
    # Create the graph
    workflow = StateGraph(WorkflowState)

    # Add nodes
    workflow.add_node("process_documents", process_documents)
    workflow.add_node("extract_information", extract_information)
    workflow.add_node("lookup_history", lookup_history)
    # TODO: Add lookup_history node

    # Add edges
    workflow.add_edge(START, "process_documents")
    workflow.add_edge("process_documents", "extract_information")
    workflow.add_edge("extract_information", "lookup_history")
    # TODO: Add edges for lookup_history

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
    print("Workflow result:", result)

if __name__ == "__main__":
    main()
