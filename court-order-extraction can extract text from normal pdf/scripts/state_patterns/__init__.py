# Comprehensive State Pattern Imports for Legal Document Extraction
import re
from typing import Dict, List, Any

# Import all state-specific patterns
from .andhra_pradesh_patterns import PATTERNS as ANDHRA_PRADESH_PATTERNS
from .arunachal_pradesh_patterns import PATTERNS as ARUNACHAL_PRADESH_PATTERNS
from .assam_patterns import PATTERNS as ASSAM_PATTERNS
from .bihar_patterns import PATTERNS as BIHAR_PATTERNS
from .chandigarh_patterns import PATTERNS as CHANDIGARH_PATTERNS
from .dadra_nagar_haveli_patterns import PATTERNS as DADRA_NAGAR_HAVELI_PATTERNS
from .delhi_patterns import PATTERNS as DELHI_PATTERNS
from .goa_patterns import PATTERNS as GOA_PATTERNS
from .gujarat_patterns import PATTERNS as GUJARAT_PATTERNS
from .haryana_patterns import PATTERNS as HARYANA_PATTERNS
from .jharkhand_patterns import PATTERNS as JHARKHAND_PATTERNS
from .karnataka_patterns import PATTERNS as KARNATAKA_PATTERNS
from .maharashtra_patterns import PATTERNS as MAHARASHTRA_PATTERNS
from .manipur_patterns import PATTERNS as MANIPUR_PATTERNS
from .meghalaya_patterns import PATTERNS as MEGHALAYA_PATTERNS
from .mizoram_patterns import PATTERNS as MIZORAM_PATTERNS
from .nagaland_patterns import PATTERNS as NAGALAND_PATTERNS
from .punjab_patterns import PATTERNS as PUNJAB_PATTERNS
from .rajasthan_patterns import PATTERNS as RAJASTHAN_PATTERNS
from .supreme_court_patterns import PATTERNS as SUPREME_COURT_PATTERNS
from .telangana_patterns import PATTERNS as TELANGANA_PATTERNS
from .uttar_pradesh_patterns import PATTERNS as UTTAR_PRADESH_PATTERNS
from .uttarakhand_patterns import PATTERNS as UTTARAKHAND_PATTERNS
from .west_bengal_patterns import PATTERNS as WEST_BENGAL_PATTERNS
from .itat_patterns import PATTERNS as ITAT_PATTERNS
from .default_patterns import PATTERNS as DEFAULT_PATTERNS

# Import legacy patterns for backward compatibility
from .kerala import KERALA_PATTERNS
from .delhi import DELHI_PATTERNS as DELHI_LEGACY_PATTERNS
from .gujarat import GUJARAT_PATTERNS as GUJARAT_LEGACY_PATTERNS
from .maharashtra import MAHARASHTRA_PATTERNS as MAHARASHTRA_LEGACY_PATTERNS
from .tamil_nadu import TAMIL_NADU_PATTERNS
from .karnataka import KARNATAKA_PATTERNS as KARNATAKA_LEGACY_PATTERNS
from .uttar_pradesh import UTTAR_PRADESH_PATTERNS as UTTAR_PRADESH_LEGACY_PATTERNS, UP_PARTY_PATTERNS
from .arunachal_pradesh import ARUNACHAL_PRADESH_PATTERNS as ARUNACHAL_PRADESH_LEGACY_PATTERNS, ARUNACHAL_PRADESH_PARTY_PATTERNS

# Import common patterns
from .general import GENERAL_PATTERNS, PARTY_TYPE_PATTERNS, COMMON_PATTERNS

# Comprehensive STATE_PATTERNS dictionary with all Indian states and union territories
STATE_PATTERNS = {
    # States
    "Andhra Pradesh": ANDHRA_PRADESH_PATTERNS,
    "Arunachal Pradesh": ARUNACHAL_PRADESH_PATTERNS,
    "Assam": ASSAM_PATTERNS,
    "Bihar": BIHAR_PATTERNS,
    "Chhattisgarh": DEFAULT_PATTERNS,  # Use default until specific patterns available
    "Goa": GOA_PATTERNS,
    "Gujarat": GUJARAT_PATTERNS,
    "Haryana": HARYANA_PATTERNS,
    "Himachal Pradesh": DEFAULT_PATTERNS,
    "Jharkhand": JHARKHAND_PATTERNS,
    "Karnataka": KARNATAKA_PATTERNS,
    "Kerala": KERALA_PATTERNS,  # Using legacy patterns
    "Madhya Pradesh": DEFAULT_PATTERNS,
    "Maharashtra": MAHARASHTRA_PATTERNS,
    "Manipur": MANIPUR_PATTERNS,
    "Meghalaya": MEGHALAYA_PATTERNS,
    "Mizoram": MIZORAM_PATTERNS,
    "Nagaland": NAGALAND_PATTERNS,
    "Odisha": DEFAULT_PATTERNS,
    "Punjab": PUNJAB_PATTERNS,
    "Rajasthan": RAJASTHAN_PATTERNS,
    "Sikkim": DEFAULT_PATTERNS,
    "Tamil Nadu": TAMIL_NADU_PATTERNS,  # Using legacy patterns
    "Telangana": TELANGANA_PATTERNS,
    "Tripura": DEFAULT_PATTERNS,
    "Uttar Pradesh": UTTAR_PRADESH_PATTERNS,
    "Uttarakhand": UTTARAKHAND_PATTERNS,
    "West Bengal": WEST_BENGAL_PATTERNS,
    
    # Union Territories
    "Andaman and Nicobar Islands": DEFAULT_PATTERNS,
    "Chandigarh": CHANDIGARH_PATTERNS,
    "Dadra and Nagar Haveli and Daman and Diu": DADRA_NAGAR_HAVELI_PATTERNS,
    "Delhi": DELHI_PATTERNS,
    "Jammu and Kashmir": DEFAULT_PATTERNS,
    "Ladakh": DEFAULT_PATTERNS,
    "Lakshadweep": DEFAULT_PATTERNS,
    "Puducherry": DEFAULT_PATTERNS,
    
    # Special Courts
    "Supreme Court": SUPREME_COURT_PATTERNS,
    "ITAT": ITAT_PATTERNS,
    
    # Fallback
    "Default": DEFAULT_PATTERNS,
}

# Legacy compatibility - keep old pattern names for backward compatibility
KERALA_PATTERNS = KERALA_PATTERNS
DELHI_PATTERNS = DELHI_PATTERNS  # Use new comprehensive patterns
GUJARAT_PATTERNS = GUJARAT_PATTERNS  # Use new comprehensive patterns
MAHARASHTRA_PATTERNS = MAHARASHTRA_PATTERNS  # Use new comprehensive patterns
TAMIL_NADU_PATTERNS = TAMIL_NADU_PATTERNS
KARNATAKA_PATTERNS = KARNATAKA_PATTERNS  # Use new comprehensive patterns
UTTAR_PRADESH_PATTERNS = UTTAR_PRADESH_PATTERNS  # Use new comprehensive patterns
ARUNACHAL_PRADESH_PATTERNS = ARUNACHAL_PRADESH_PATTERNS  # Use new comprehensive patterns

def classify_party_type(party_name: str, additional_info: str = "") -> str:
    """Classify party type based on name and additional information"""
    combined_text = f"{party_name} {additional_info}".lower()
    
    for party_type, patterns in PARTY_TYPE_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, combined_text, re.IGNORECASE):
                return party_type
    
    return "individual"  # default

def get_state_patterns(state: str) -> Dict[str, Any]:
    """Get patterns for a specific state"""
    return STATE_PATTERNS.get(state, DEFAULT_PATTERNS)

def get_available_states() -> List[str]:
    """Get list of states with defined patterns"""
    return list(STATE_PATTERNS.keys())

def extract_field_with_patterns(text: str, patterns: List[str], field_name: str = "") -> str:
    """Extract a field using multiple patterns"""
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            if len(match.groups()) > 1:
                return f"{match.group(1)} OF {match.group(2)}"
            else:
                return match.group(1).strip()
    return ""

def extract_address_components(text: str, address_patterns: Dict[str, List[str]]) -> Dict[str, str]:
    """Extract address components using patterns"""
    address = {}
    for component, patterns in address_patterns.items():
        extracted_value = extract_field_with_patterns(text, patterns, component)
        address[component] = extracted_value if extracted_value else "not in document"
    return address

__all__ = [
    'STATE_PATTERNS',
    'GENERAL_PATTERNS',
    'PARTY_TYPE_PATTERNS', 
    'COMMON_PATTERNS',
    'DEFAULT_PATTERNS',
    
    # All state patterns
    'ANDHRA_PRADESH_PATTERNS',
    'ARUNACHAL_PRADESH_PATTERNS',
    'ASSAM_PATTERNS',
    'BIHAR_PATTERNS',
    'CHANDIGARH_PATTERNS',
    'DADRA_NAGAR_HAVELI_PATTERNS',
    'DELHI_PATTERNS',
    'GOA_PATTERNS',
    'GUJARAT_PATTERNS',
    'HARYANA_PATTERNS',
    'JHARKHAND_PATTERNS',
    'KARNATAKA_PATTERNS',
    'KERALA_PATTERNS',
    'MAHARASHTRA_PATTERNS',
    'MANIPUR_PATTERNS',
    'MEGHALAYA_PATTERNS',
    'MIZORAM_PATTERNS',
    'NAGALAND_PATTERNS',
    'PUNJAB_PATTERNS',
    'RAJASTHAN_PATTERNS',
    'SUPREME_COURT_PATTERNS',
    'TELANGANA_PATTERNS',
    'TAMIL_NADU_PATTERNS',
    'UTTAR_PRADESH_PATTERNS',
    'UTTARAKHAND_PATTERNS',
    'WEST_BENGAL_PATTERNS',
    'ITAT_PATTERNS',
    
    # Legacy patterns for backward compatibility
    'ARUNACHAL_PRADESH_PARTY_PATTERNS',
    'UP_PARTY_PATTERNS',
    
    # Utility functions
    'classify_party_type',
    'get_state_patterns',
    'get_available_states',
    'extract_field_with_patterns',
    'extract_address_components'
]
