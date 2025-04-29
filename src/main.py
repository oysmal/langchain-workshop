from langgraph.graph import StateGraph, END, START
from typing import Dict, List, Any, TypedDict
from pydantic import BaseModel
from src.document_processor import DocumentProcessor
from src.information_extractor import InformationExtractor
from src.history_lookup import VesselHistoryTool, CompanyHistoryTool
from src.risk_assessor import RiskAssessor
from src.models import (
        DatabaseEntry, Validity, Agreement, Premium, LossRatio,
        Risk, Reinsurance, Contact
        )
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

def process_documents(state):
    """Process the documents and add them to the state"""
    processor = DocumentProcessor()
    documents = processor.process_documents(
            pdf_paths=state["pdf_paths"],
            text_paths=state["text_paths"],
            excel_paths=state["excel_paths"]
            )
    return {"documents": documents}

def extract_information(state):
    """Extract key information from the documents"""
    extractor = InformationExtractor()

    # Extract data using consolidated extraction methods
    entity_data = extractor.extract_entity_data(state["documents"])
    financial_data = extractor.extract_financial_data(state["documents"])
    insurance_risk_data = extractor.extract_insurance_risk_data(state["documents"])

    print("Entity Data:", entity_data.model_dump())
    print("Financial Data:", financial_data.model_dump())
    print("Insurance Risk Data:", insurance_risk_data.model_dump())

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

    # Handle CompanyInfo from entity_data
    company_info = state["entity_data"].company_info
    company_name = company_info.company_name if company_info else "Unknown Company"
    company_history = company_tool.run(company_name)

    # Handle vessel info from entity_data
    vessel_histories = {}
    if state["entity_data"].vessel_info:
        for vessel in state["entity_data"].vessel_info:
            vessel_histories[vessel.imo_number] = vessel_tool.run(vessel.imo_number)

    return {
            "company_history": company_history,
            "vessel_histories": vessel_histories,
            }

def assess_risk(state):
    """Generate risk assessment"""
    assessor = RiskAssessor()

    vessel_info = {}
    vessel_history = {}

    # Get vessel info from entity_data
    if state["entity_data"].vessel_info and len(state["entity_data"].vessel_info) > 0:
        vessel_info = { state["entity_data"].vessel_info[i].imo_number: state["entity_data"].vessel_info[i].model_dump() for i in range(len(state["entity_data"].vessel_info))}
        vessel_history = { imo_number: state["vessel_histories"].get(imo_number, {}) for imo_number in vessel_info }

    # Get company info and convert to dict if needed
    company_info = {}
    if state["entity_data"].company_info:
        company_info = state["entity_data"].company_info.model_dump()

    # Get insurance offer info and convert to dict if needed
    insurance_offer = {}
    if state["insurance_risk_data"].insurance_offer:
        insurance_offer = state["insurance_risk_data"].insurance_offer.model_dump()

    # Generate assessment using the RiskAssessment from risk_assessor.py
    assessor_result = assessor.generate_assessment(
            company_info=company_info,
            vessel_info=vessel_info,
            insurance_offer=insurance_offer,
            company_history=state["company_history"],
            vessel_history=vessel_history
            )

    return {"assessment": assessor_result}

class AdditionalInsights(BaseModel):
    request_summary: str
    recommendation: str
    points_of_attention: List[str]

def generate_additional_insights(state) -> AdditionalInsights:
    """Generate additional insights for the database entry"""
    llm = ChatOpenAI(model="gpt-4.1")

    # Extract relevant information
    company_info = state["entity_data"].company_info

    vessel_info = None
    if state["entity_data"].vessel_info and len(state["entity_data"].vessel_info) > 0:
        vessel_info = state["entity_data"].vessel_info[0]

    insurance_offer = state["insurance_risk_data"].insurance_offer
    assessment = state.get("assessment", {})
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
            | llm.with_structured_output(AdditionalInsights)
            )

    # Generate insights
    result = chain.invoke({})

    if not isinstance(result, AdditionalInsights):
        result = AdditionalInsights(**result)

    return result


def create_db_entry(state):
    """Create the final database entry model"""

    # Create Validity object - Use agreement_info if available
    validity = Validity(start_date=None, end_date=None)
    if state["insurance_risk_data"].agreement_info:
        agreement_info = state["insurance_risk_data"].agreement_info
        validity = Validity(
            start_date=agreement_info.start_date,
            end_date=agreement_info.end_date
        )

    # Create Agreement object from insurance_risk_data.agreement_info
    agreement = Agreement(
        id=None,
        name=None,
        validity=validity,
        products=[],
        our_share=None,
        installments=None,
        conditions=None
    )

    if state["insurance_risk_data"].agreement_info:
        agreement_info = state["insurance_risk_data"].agreement_info
        agreement = Agreement(
            id=agreement_info.id,
            name=agreement_info.name,
            validity=validity,
            products=agreement_info.products or [],
            our_share=agreement_info.our_share,
            installments=agreement_info.installments,
            conditions=agreement_info.conditions
        )

    # Create Premium object from financial_data.premium_info
    premium = Premium(
        gross_premium=None,
        brokerage_percent=None,
        net_premium=None
    )

    if state["financial_data"].premium_info:
        premium_info = state["financial_data"].premium_info
        premium = Premium(
            gross_premium=premium_info.gross_premium,
            brokerage_percent=premium_info.brokerage_percent,
            net_premium=premium_info.net_premium
        )

    # Create LossRatio object from financial_data.loss_ratio_info
    loss_ratio = LossRatio(
        value_percent=None,
        claims=None,
        premium=None
    )

    if state["financial_data"].loss_ratio_info:
        loss_ratio_info = state["financial_data"].loss_ratio_info
        loss_ratio = LossRatio(
            value_percent=loss_ratio_info.value_percent,
            claims=loss_ratio_info.claims,
            premium=loss_ratio_info.premium
        )

    # Create Risk object - First try from insurance_risk_data.risk_info
    # If not available, use the assessment
    risk_categories = {}

    if state["insurance_risk_data"].risk_info and state["insurance_risk_data"].risk_info.risk_categories:
        risk_categories = state["insurance_risk_data"].risk_info.risk_categories
    else:
        # If risk values are not available, use the assessment
        assessment = state.get("assessment", {})
        if assessment:
            # Check if assessment is a dictionary or an object
            if isinstance(assessment, dict) and "risk_categories" in assessment:
                risk_categories = assessment["risk_categories"]
            elif hasattr(assessment, "risk_categories"):
                risk_categories = assessment.risk_categories

    risk = Risk(risk_categories=risk_categories)

    # Create objects list - Use vessel info as objects if available
    objects_data = []
    if state["entity_data"].vessel_info:
        for vessel in state["entity_data"].vessel_info:
            objects_data.append({
                "name": vessel.vessel_name,
                "id": vessel.imo_number
            })

    # Create Reinsurance object from insurance_risk_data.reinsurance_info
    reinsurance = Reinsurance(
        net_tty=None,
        net_fac=None,
        net_retention=None,
        commission=None
    )

    if state["insurance_risk_data"].reinsurance_info:
        reinsurance_info = state["insurance_risk_data"].reinsurance_info
        reinsurance = Reinsurance(
            net_tty=reinsurance_info.net_tty,
            net_fac=reinsurance_info.net_fac,
            net_retention=reinsurance_info.net_retention,
            commission=reinsurance_info.commission
        )

    # Create Contact objects from entity_data.contact_info
    contacts = []
    if state["entity_data"].contact_info:
        for contact_info in state["entity_data"].contact_info:
            contacts.append(Contact(
                name=contact_info.name,
                role=contact_info.role,
                email=contact_info.email,
                phone=contact_info.phone
            ))

    # Generate additional insights
    insights = generate_additional_insights(state)

    # Create the database entry
    db_entry = DatabaseEntry(
        agreement=agreement,
        premium=premium,
        loss_ratio=loss_ratio,
        risk=risk,
        objects=objects_data,
        reinsurance=reinsurance,
        contacts=contacts,
        request_summary=insights.request_summary,
        recommendation=insights.recommendation,
        points_of_attention=insights.points_of_attention,
    )

    return {"db_entry": db_entry}

# Define the state schema
class WorkflowState(TypedDict, total=False):
    pdf_paths: List[str]
    text_paths: List[str]
    excel_paths: List[str]
    documents: List
    entity_data: Any
    financial_data: Any
    insurance_risk_data: Any
    company_history: Dict
    vessel_histories: Dict
    assessment: Any
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
                "src/data/Maritime_Insurance_Proposal2.pdf",
                ],
            "excel_paths": [],
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
