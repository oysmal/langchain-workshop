from langgraph.graph import StateGraph, END, START
from src.document_processor import DocumentProcessor
from src.workflow_state import WorkflowState

def process_documents(state: WorkflowState):
    """Process the documents and add them to the state"""
    processor = DocumentProcessor()
    # TODO: Call the document processor with the paths from the state
    # and add the processed documents to the state

def create_workflow():
    """Create the LangGraph workflow"""
    # TODO: Create the graph
    # TODO: Add the edge from START to the process_documents node, and to the END node.
    # TODO: Return the compiled graph
    pass

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
