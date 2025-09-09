import re
from typing import Dict, List, Any

# Import patterns from separate state files
from .state_patterns import (
    KERALA_PATTERNS,
    DELHI_PATTERNS,
    GUJARAT_PATTERNS,
    MAHARASHTRA_PATTERNS,
    TAMIL_NADU_PATTERNS,
    KARNATAKA_PATTERNS,
    GENERAL_PATTERNS,
    PARTY_TYPE_PATTERNS,
    COMMON_PATTERNS
)

# Enhanced State-wise Regex Patterns for Court Order Information Extraction
STATE_PATTERNS = {
    "Kerala": KERALA_PATTERNS,
    
    "Delhi": DELHI_PATTERNS,
    
    "Maharashtra": MAHARASHTRA_PATTERNS,
    
    "Tamil Nadu": TAMIL_NADU_PATTERNS,
    
    "Karnataka": KARNATAKA_PATTERNS,
    
    "Gujarat": GUJARAT_PATTERNS,
}

# Party type classification patterns (imported from general.py)
# PARTY_TYPE_PATTERNS are now available from the import

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
    return STATE_PATTERNS.get(state, {})

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

# Additional utility patterns for common extractions (imported from general.py)
# COMMON_PATTERNS are now available from the import

# General patterns that work across all states - fallback when state-specific patterns fail
# GENERAL_PATTERNS are now available from the import

if __name__ == "__main__":
    # Test the patterns
    print("Available states:", get_available_states())
    print("Kerala patterns keys:", list(get_state_patterns("Kerala").keys()))
    print("General patterns keys:", list(GENERAL_PATTERNS.keys()))
    print("Party type for 'State of Kerala':", classify_party_type("State of Kerala"))
