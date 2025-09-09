# State Patterns Package
# Organized state-wise patterns for legal document extraction

import re
from typing import Dict, List, Any

from .kerala import KERALA_PATTERNS
from .delhi import DELHI_PATTERNS
from .gujarat import GUJARAT_PATTERNS
from .maharashtra import MAHARASHTRA_PATTERNS
from .tamil_nadu import TAMIL_NADU_PATTERNS
from .karnataka import KARNATAKA_PATTERNS
from .general import GENERAL_PATTERNS, PARTY_TYPE_PATTERNS, COMMON_PATTERNS

# Create the main STATE_PATTERNS dictionary here
STATE_PATTERNS = {
    "Kerala": KERALA_PATTERNS,
    "Delhi": DELHI_PATTERNS,
    "Gujarat": GUJARAT_PATTERNS,
    "Maharashtra": MAHARASHTRA_PATTERNS,
    "Tamil Nadu": TAMIL_NADU_PATTERNS,
    "Karnataka": KARNATAKA_PATTERNS,
}

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

__all__ = [
    'STATE_PATTERNS',
    'KERALA_PATTERNS',
    'DELHI_PATTERNS', 
    'GUJARAT_PATTERNS',
    'MAHARASHTRA_PATTERNS',
    'TAMIL_NADU_PATTERNS',
    'KARNATAKA_PATTERNS',
    'GENERAL_PATTERNS',
    'PARTY_TYPE_PATTERNS',
    'COMMON_PATTERNS',
    'classify_party_type',
    'get_state_patterns',
    'get_available_states',
    'extract_field_with_patterns',
    'extract_address_components'
]
