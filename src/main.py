from langgraph.graph import StateGraph, END, START
from typing import Dict, List, Any, TypedDict
from src.document_processor import DocumentProcessor
from src.information_extractor import InformationExtractor
from src.history_lookup import VesselHistoryTool, CompanyHistoryTool
from src.risk_assessor import RiskAssessor
from src.models import DatabaseEntry, Company, Vessel, InsuranceDetails, History, Incident, Claim, RiskAssessment as ModelsRiskAssessment
from src.risk_assessor import RiskAssessment as AssessorRiskAssessment

def process_documents(state):
    """Process the documents and add them to the state"""
    processor = DocumentProcessor()
    documents = processor.process_documents(
        pdf_paths=state["pdf_paths"],
        text_paths=state["text_paths"]
    )
    return {"documents": documents}

def extract_information(state):
    """Extract key information from the documents"""
    extractor = InformationExtractor()
    company_info = extractor.extract_company_info(state["documents"])
    vessel_info = extractor.extract_vessel_info(state["documents"])
    insurance_offer = extractor.extract_insurance_offer(state["documents"])
    
    return {
        "company_info": company_info,
        "vessel_info": vessel_info,
        "insurance_offer": insurance_offer
    }

def lookup_history(state):
    """Look up vessel and company history"""
    vessel_tool = VesselHistoryTool()
    company_tool = CompanyHistoryTool()
    
    # Handle CompanyInfo object directly
    company_info = state["company_info"][0]
    company_name = company_info.company_name if hasattr(company_info, "company_name") else company_info["company_name"]
    company_history = company_tool.run(company_name)
    
    vessel_histories = {}
    for vessel in state["vessel_info"]:
        # Handle VesselInfo object directly
        imo = vessel.imo_number if hasattr(vessel, "imo_number") else vessel["imo_number"]
        vessel_histories[imo] = vessel_tool.run(imo)
    
    return {
        "company_history": company_history,
        "vessel_histories": vessel_histories
    }

def assess_risk(state):
    """Generate risk assessment"""
    assessor = RiskAssessor()
    
    # For simplicity, we'll just use the first vessel if multiple are found
    vessel_info = state["vessel_info"][0] if state["vessel_info"] else {}
    vessel_history = {}
    
    # Handle both object attributes and dictionary access
    if vessel_info:
        imo = vessel_info.imo_number if hasattr(vessel_info, "imo_number") else vessel_info.get("imo_number")
        if imo:
            vessel_history = state["vessel_histories"].get(imo, {})
    
    # Convert Pydantic models to dictionaries if needed
    company_info = state["company_info"][0] if state["company_info"] else {}
    if hasattr(company_info, "model_dump"):
        company_info = company_info.model_dump()
    elif hasattr(company_info, "dict"):
        company_info = company_info.dict()
    
    vessel_info_dict = vessel_info
    if hasattr(vessel_info, "model_dump"):
        vessel_info_dict = vessel_info.model_dump()
    elif hasattr(vessel_info, "dict"):
        vessel_info_dict = vessel_info.dict()
    
    insurance_offer = state["insurance_offer"][0] if state["insurance_offer"] else {}
    if hasattr(insurance_offer, "model_dump"):
        insurance_offer = insurance_offer.model_dump()
    elif hasattr(insurance_offer, "dict"):
        insurance_offer = insurance_offer.dict()
    
    # Generate assessment using the RiskAssessment from risk_assessor.py
    assessor_result = assessor.generate_assessment(
        company_info=company_info,
        vessel_info=vessel_info_dict,
        insurance_offer=insurance_offer,
        company_history=state["company_history"],
        vessel_history=vessel_history
    )
    
    # Convert to the RiskAssessment from models.py
    assessment = ModelsRiskAssessment(
        risk_score=assessor_result.risk_score,
        company_description=assessor_result.company_description,
        case_description=assessor_result.case_description,
        recommendation=assessor_result.recommendation
    )
    
    return {"assessment": assessment}

def create_db_entry(state):
    """Create the final database entry model"""
    # This would be more complex in a real application
    # For the tutorial, we'll create a simplified version
    
    # Convert extracted data to our models
    company_data = state["company_info"][0] if state["company_info"] else {}
    
    # Handle both object attributes and dictionary access for company data
    if hasattr(company_data, "company_name"):
        company_name = company_data.company_name
        company_id = company_data.company_id if hasattr(company_data, "company_id") else None
    else:
        company_name = company_data.get("company_name", "Unknown")
        company_id = company_data.get("company_id")
    
    company = Company(
        name=company_name,
        company_id=company_id
    )
    
    vessels = []
    for v in state["vessel_info"]:
        # Handle both object attributes and dictionary access for vessel data
        if hasattr(v, "vessel_name"):
            vessel_name = v.vessel_name
            imo_number = v.imo_number
        else:
            vessel_name = v.get("vessel_name", "Unknown")
            imo_number = v.get("imo_number", "Unknown")
            
        vessels.append(Vessel(
            name=vessel_name,
            imo_number=imo_number
        ))
    
    insurance_data = state["insurance_offer"][0] if state["insurance_offer"] else {}
    
    # Handle both object attributes and dictionary access for insurance data
    if hasattr(insurance_data, "coverage_percentage"):
        coverage_percentage = insurance_data.coverage_percentage
        premium_amount = insurance_data.premium_amount if hasattr(insurance_data, "premium_amount") else None
        coverage_type = insurance_data.coverage_type
    else:
        coverage_percentage = insurance_data.get("coverage_percentage", 0)
        premium_amount = insurance_data.get("premium_amount")
        coverage_type = insurance_data.get("coverage_type", "Unknown")
    
    insurance = InsuranceDetails(
        coverage_percentage=coverage_percentage,
        premium_amount=premium_amount,
        coverage_type=coverage_type
    )
    
    # Create the database entry
    # Convert assessment to ModelsRiskAssessment object if it's a dictionary
    assessment = state["assessment"]
    if isinstance(assessment, dict):
        assessment = ModelsRiskAssessment(
            risk_score=assessment.get("risk_score", 5),
            company_description=assessment.get("company_description", ""),
            case_description=assessment.get("case_description", ""),
            recommendation=assessment.get("recommendation", "")
        )
    # Convert from AssessorRiskAssessment to ModelsRiskAssessment if needed
    elif isinstance(assessment, AssessorRiskAssessment):
        assessment = ModelsRiskAssessment(
            risk_score=assessment.risk_score,
            company_description=assessment.company_description,
            case_description=assessment.case_description,
            recommendation=assessment.recommendation
        )
    
    # Convert company_history to History object if it's a dictionary
    company_history = state["company_history"]
    if isinstance(company_history, dict) and not isinstance(company_history, History):
        incidents = []
        claims = []
        
        if "incidents" in company_history and isinstance(company_history["incidents"], list):
            for incident in company_history["incidents"]:
                if isinstance(incident, dict):
                    incidents.append(Incident(
                        date=incident.get("date", ""),
                        description=incident.get("description", ""),
                        severity=incident.get("severity", "")
                    ))
        
        if "claims" in company_history and isinstance(company_history["claims"], list):
            for claim in company_history["claims"]:
                if isinstance(claim, dict):
                    claims.append(Claim(
                        date=claim.get("date", ""),
                        amount=claim.get("amount", 0.0),
                        status=claim.get("status", ""),
                        description=claim.get("description", "")
                    ))
        
        company_history = History(incidents=incidents, claims=claims)
    
    # Convert vessel_histories to Dict[str, History] if it's a dictionary
    vessel_histories = state["vessel_histories"]
    converted_vessel_histories = {}
    
    if isinstance(vessel_histories, dict):
        for imo, history in vessel_histories.items():
            if isinstance(history, dict) and not isinstance(history, History):
                incidents = []
                claims = []
                
                if "incidents" in history and isinstance(history["incidents"], list):
                    for incident in history["incidents"]:
                        if isinstance(incident, dict):
                            incidents.append(Incident(
                                date=incident.get("date", ""),
                                description=incident.get("description", ""),
                                severity=incident.get("severity", "")
                            ))
                
                if "claims" in history and isinstance(history["claims"], list):
                    for claim in history["claims"]:
                        if isinstance(claim, dict):
                            claims.append(Claim(
                                date=claim.get("date", ""),
                                amount=claim.get("amount", 0.0),
                                status=claim.get("status", ""),
                                description=claim.get("description", "")
                            ))
                
                converted_vessel_histories[imo] = History(incidents=incidents, claims=claims)
            else:
                converted_vessel_histories[imo] = history
    
    db_entry = DatabaseEntry(
        company=company,
        vessels=vessels,
        insurance=insurance,
        company_history=company_history,
        vessel_histories=converted_vessel_histories,
        assessment=assessment
    )
    
    return {"db_entry": db_entry}

# Define the state schema
class WorkflowState(TypedDict, total=False):
    pdf_paths: List[str]
    text_paths: List[str]
    documents: List
    company_info: List[Dict]
    vessel_info: List[Dict]
    insurance_offer: List[Dict]
    company_history: Dict
    vessel_histories: Dict
    assessment: Dict
    db_entry: Any

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
            "src/data/Maritime_Insurance_Proposal2.pdf"
        ],
        "text_paths": [
            "src/data/broker_email.txt"
        ]
    }
    
    # Execute the workflow
    result = workflow.invoke(inputs)
    
    # Print the final database entry
    print("\n=== FINAL DATABASE ENTRY ===")
    db_entry = result["db_entry"]
    print(f"Company: {db_entry.company.name}")
    print(f"Vessels: {', '.join([v.name + ' (IMO: ' + v.imo_number + ')' for v in db_entry.vessels])}")
    print(f"Insurance: {db_entry.insurance.coverage_percentage}% coverage for {db_entry.insurance.coverage_type}")
    print(f"Risk Score: {db_entry.assessment.risk_score}/10")
    print(f"Recommendation: {db_entry.assessment.recommendation}")
    print("\nCompany Description:")
    print(db_entry.assessment.company_description)
    print("\nCase Description:")
    print(db_entry.assessment.case_description)
    
    return db_entry

if __name__ == "__main__":
    main()