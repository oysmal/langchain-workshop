from typing import Dict, List

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