from typing import Dict, List, Optional, Any
from src.models import RiskCategories

def get_risk_categories(state) -> Optional[RiskCategories]:
    """Extract risk categories from state with proper fallbacks"""
    if state["insurance_risk_data"].risk_info and state["insurance_risk_data"].risk_info.risk_categories:
        return state["insurance_risk_data"].risk_info.risk_categories
    
    assessment = state.get("assessment", {})
    if isinstance(assessment, dict) and "risk_categories" in assessment:
        return assessment["risk_categories"]
    elif hasattr(assessment, "risk_categories"):
        return assessment.risk_categories
    
    return None

def get_vessel_objects(entity_data) -> List[Dict]:
    """Convert vessel info to objects format"""
    if not entity_data.vessel_info:
        return []
    
    return [{"name": vessel.vessel_name, "id": vessel.imo_number} 
            for vessel in entity_data.vessel_info]

def safe_model_dump(model, default=None):
    """Safely convert a model to a dictionary"""
    if model is None:
        return default if default is not None else {}
    return model.model_dump()