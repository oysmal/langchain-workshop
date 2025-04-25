from langgraph.graph import StateGraph, END, START
from typing import Dict, List, Any, TypedDict
from src.document_processor import DocumentProcessor
from src.information_extractor import InformationExtractor
from src.history_lookup import VesselHistoryTool, CompanyHistoryTool
from src.risk_assessor import RiskAssessor
from src.models import (
    DatabaseEntry, Validity, Agreement, Premium, Accounting, LossRatio, 
    Risk, Reinsurance, Contact, Company, Vessel, InsuranceDetails, 
    History, Incident, Claim, RiskAssessment as ModelsRiskAssessment,
    LegacyDatabaseEntry
)
from src.risk_assessor import RiskAssessment as AssessorRiskAssessment
from src.data.mock_data import (
    AGREEMENT_DATA, PREMIUM_DATA, ACCOUNTING_DATA, LOSS_RATIO_DATA,
    RISK_DATA, REINSURANCE_DATA, OBJECTS_DATA, CONTACTS_DATA
)
import json
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

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
    
    # Extract legacy information
    company_info = extractor.extract_company_info(state["documents"])
    vessel_info = extractor.extract_vessel_info(state["documents"])
    insurance_offer = extractor.extract_insurance_offer(state["documents"])
    
    # Extract new information
    agreement_info = extractor.extract_agreement_info(state["documents"])
    premium_info = extractor.extract_premium_info(state["documents"])
    accounting_info = extractor.extract_accounting_info(state["documents"])
    loss_ratio_info = extractor.extract_loss_ratio_info(state["documents"])
    risk_info = extractor.extract_risk_info(state["documents"])
    reinsurance_info = extractor.extract_reinsurance_info(state["documents"])
    contact_info = extractor.extract_contact_info(state["documents"])
    objects_info = extractor.extract_objects(state["documents"])
    
    return {
        # Legacy information
        "company_info": company_info,
        "vessel_info": vessel_info,
        "insurance_offer": insurance_offer,
        
        # New information
        "agreement_info": agreement_info,
        "premium_info": premium_info,
        "accounting_info": accounting_info,
        "loss_ratio_info": loss_ratio_info,
        "risk_info": risk_info,
        "reinsurance_info": reinsurance_info,
        "contact_info": contact_info,
        "objects_info": objects_info
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
    
    # Look up mock data for the new structure
    agreement_data = AGREEMENT_DATA.get(company_name, AGREEMENT_DATA.get("Bergen Shipping Company", {}))
    premium_data = PREMIUM_DATA.get(company_name, PREMIUM_DATA.get("Bergen Shipping Company", {}))
    accounting_data = ACCOUNTING_DATA.get(company_name, ACCOUNTING_DATA.get("Bergen Shipping Company", {}))
    loss_ratio_data = LOSS_RATIO_DATA.get(company_name, LOSS_RATIO_DATA.get("Bergen Shipping Company", {}))
    risk_data = RISK_DATA.get(company_name, RISK_DATA.get("Bergen Shipping Company", {}))
    reinsurance_data = REINSURANCE_DATA.get(company_name, REINSURANCE_DATA.get("Bergen Shipping Company", {}))
    objects_data = OBJECTS_DATA.get(company_name, OBJECTS_DATA.get("Bergen Shipping Company", []))
    contacts_data = CONTACTS_DATA.get(company_name, CONTACTS_DATA.get("Bergen Shipping Company", []))
    
    return {
        # Legacy data
        "company_history": company_history,
        "vessel_histories": vessel_histories,
        
        # New data
        "agreement_data": agreement_data,
        "premium_data": premium_data,
        "accounting_data": accounting_data,
        "loss_ratio_data": loss_ratio_data,
        "risk_data": risk_data,
        "reinsurance_data": reinsurance_data,
        "objects_data": objects_data,
        "contacts_data": contacts_data
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
    
    return {"assessment": assessor_result}

def generate_additional_insights(state):
    """Generate additional insights for the database entry"""
    llm = ChatOpenAI(model="gpt-4.1")
    
    # Extract relevant information
    company_info = state["company_info"][0] if state["company_info"] else {}
    vessel_info = state["vessel_info"][0] if state["vessel_info"] else {}
    insurance_offer = state["insurance_offer"][0] if state["insurance_offer"] else {}
    assessment = state["assessment"]
    agreement_data = state.get("agreement_data", {})
    premium_data = state.get("premium_data", {})
    risk_data = state.get("risk_data", {})
    
    # Convert to strings for the prompt
    company_str = str(company_info)
    vessel_str = str(vessel_info)
    insurance_str = str(insurance_offer)
    assessment_str = str(assessment)
    agreement_str = str(agreement_data)
    premium_str = str(premium_data)
    risk_str = str(risk_data)
    
    # Create a prompt for generating additional insights
    prompt = ChatPromptTemplate.from_template("""
    You are a maritime insurance expert. Based on the following information, provide:
    
    1. A concise summary of the underwriting request (2-3 sentences)
    2. A clear recommendation regarding the case (Accept/Reject/Request More Information with brief justification)
    3. A list of 3-5 specific points that the reviewer should pay particular attention to when reviewing this case
    
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
    
    # Create a chain for generating insights
    chain = (
        {"company_info": lambda _: company_str,
         "vessel_info": lambda _: vessel_str,
         "insurance_offer": lambda _: insurance_str,
         "assessment": lambda _: assessment_str,
         "agreement": lambda _: agreement_str,
         "premium": lambda _: premium_str,
         "risk": lambda _: risk_str}
        | prompt
        | llm
    )
    
    # Generate insights
    result = chain.invoke({})
    
    # Parse the result
    result_text = result.content
    
    # Extract request summary
    request_summary = ""
    if "REQUEST SUMMARY:" in result_text:
        request_summary_section = result_text.split("REQUEST SUMMARY:")[1].split("RECOMMENDATION:")[0].strip()
        request_summary = request_summary_section
    
    # Extract recommendation
    recommendation = ""
    if "RECOMMENDATION:" in result_text:
        recommendation_section = result_text.split("RECOMMENDATION:")[1].split("POINTS OF ATTENTION:")[0].strip()
        recommendation = recommendation_section
    
    # Extract points of attention
    points_of_attention = []
    if "POINTS OF ATTENTION:" in result_text:
        points_section = result_text.split("POINTS OF ATTENTION:")[1].strip()
        for line in points_section.split("\n"):
            if line.strip().startswith("-"):
                point = line.strip()[1:].strip()
                if point:
                    points_of_attention.append(point)
    
    return {
        "request_summary": request_summary,
        "recommendation": recommendation,
        "points_of_attention": points_of_attention
    }

def create_db_entry(state):
    """Create the final database entry model"""
    # Extract company name for reference
    company_data = state["company_info"][0] if state["company_info"] else {}
    company_name = company_data.company_name if hasattr(company_data, "company_name") else company_data.get("company_name", "Unknown")
    
    # Create Validity object
    agreement_data = state.get("agreement_data", {})
    validity_data = agreement_data.get("validity", {})
    validity = Validity(
        start_date=validity_data.get("start_date", "2025-01-01"),
        end_date=validity_data.get("end_date", "2026-01-01")
    )
    
    # Create Agreement object
    agreement = Agreement(
        id=agreement_data.get("id", "000000-00-R0"),
        name=agreement_data.get("name", "Unknown Agreement"),
        validity=validity,
        products=agreement_data.get("products", []),
        our_share=agreement_data.get("our_share", "0%"),
        installments=agreement_data.get("installments", 1),
        conditions=agreement_data.get("conditions", "Standard")
    )
    
    # Create Premium object
    premium_data = state.get("premium_data", {})
    premium = Premium(
        gross_premium=premium_data.get("gross_premium", 0),
        brokerage_percent=premium_data.get("brokerage_percent", 0),
        net_premium=premium_data.get("net_premium", 0)
    )
    
    # Create Accounting object
    accounting_data = state.get("accounting_data", {})
    accounting = Accounting(
        paid=accounting_data.get("paid", 0),
        amount_due=accounting_data.get("amount_due", 0),
        remaining=accounting_data.get("remaining", 0),
        balance_percent=accounting_data.get("balance_percent", 0)
    )
    
    # Create LossRatio object
    loss_ratio_data = state.get("loss_ratio_data", {})
    loss_ratio = LossRatio(
        value_percent=loss_ratio_data.get("value_percent", 0),
        claims=loss_ratio_data.get("claims"),
        premium=loss_ratio_data.get("premium")
    )
    
    # Create Risk object
    risk_data = state.get("risk_data", {})
    risk_values = risk_data.get("values_by_id", {})
    
    # If risk values are not available, use the assessment
    assessment = state.get("assessment", {})
    if not risk_values and hasattr(assessment, "values_by_id"):
        risk_values = assessment.values_by_id
    
    risk = Risk(
        values_by_id=risk_values
    )
    
    # Create objects list
    objects_data = state.get("objects_data", [])
    
    # Create Reinsurance object
    reinsurance_data = state.get("reinsurance_data", {})
    reinsurance = Reinsurance(
        net_tty=reinsurance_data.get("net_tty", 0),
        net_fac=reinsurance_data.get("net_fac"),
        net_retention=reinsurance_data.get("net_retention", 0),
        commission=reinsurance_data.get("commission")
    )
    
    # Create Contact objects
    contacts_data = state.get("contacts_data", [])
    contacts = []
    for contact_data in contacts_data:
        contacts.append(Contact(
            name=contact_data.get("name", "Unknown"),
            role=contact_data.get("role", "Unknown"),
            email=contact_data.get("email", "unknown@example.com"),
            phone=contact_data.get("phone", "Unknown")
        ))
    
    # Generate additional insights
    insights = generate_additional_insights(state)
    
    # Create the database entry
    db_entry = DatabaseEntry(
        agreement=agreement,
        premium=premium,
        accounting=accounting,
        loss_ratio=loss_ratio,
        risk=risk,
        objects=objects_data,
        reinsurance=reinsurance,
        contacts=contacts,
        request_summary=insights.get("request_summary", ""),
        recommendation=insights.get("recommendation", ""),
        points_of_attention=insights.get("points_of_attention", [])
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
    agreement_info: List[Dict]
    premium_info: List[Dict]
    accounting_info: List[Dict]
    loss_ratio_info: List[Dict]
    risk_info: List[Dict]
    reinsurance_info: List[Dict]
    contact_info: List[Dict]
    objects_info: List[Dict]
    company_history: Dict
    vessel_histories: Dict
    agreement_data: Dict
    premium_data: Dict
    accounting_data: Dict
    loss_ratio_data: Dict
    risk_data: Dict
    reinsurance_data: Dict
    objects_data: List
    contacts_data: List
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
    
    # Get the database entry
    db_entry = result["db_entry"]
    
    # Convert to JSON and print
    db_entry_json = db_entry.model_dump_json(indent=2)
    print(db_entry_json)
    
    return db_entry

if __name__ == "__main__":
    main()