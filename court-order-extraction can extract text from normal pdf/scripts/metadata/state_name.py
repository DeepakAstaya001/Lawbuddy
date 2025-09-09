import re
from typing import Tuple, Optional

# 28 States
INDIAN_STATES = [
    "Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chhattisgarh","Goa","Gujarat",
    "Haryana","Himachal Pradesh","Jharkhand","Karnataka","Kerala","Madhya Pradesh",
    "Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Punjab",
    "Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh",
    "Uttarakhand","West Bengal"
]

# 8 Union Territories (current official list)
INDIAN_UNION_TERRITORIES = [
    "Andaman and Nicobar Islands",
    "Chandigarh",
    "Dadra and Nagar Haveli and Daman and Diu",
    "Delhi",
    "Jammu and Kashmir",
    "Ladakh",
    "Lakshadweep",
    "Puducherry",
]

# Common aliases/old names → canonical
ALIASES = {
    "orissa": "Odisha",
    "pondicherry": "Puducherry",
    "nct of delhi": "Delhi",
    "j&k": "Jammu and Kashmir",
    "jammu & kashmir": "Jammu and Kashmir",
    # pre-2020 separate UT names → merged UT
    "dadra and nagar haveli": "Dadra and Nagar Haveli and Daman and Diu",
    "daman and diu": "Dadra and Nagar Haveli and Daman and Diu",
}

ALL_REGIONS = INDIAN_STATES + INDIAN_UNION_TERRITORIES
REGEX = re.compile(
    r'\b(' + '|'.join(map(re.escape, ALL_REGIONS + list(ALIASES.keys()))) + r')\b',
    re.IGNORECASE
)

def match_region(text: str) -> Tuple[str, Optional[str]]:
    if not text:
        return "", None
    m = REGEX.search(text)
    if not m:
        return "", None
    found = m.group(1)
    canonical = ALIASES.get(found.lower(), found.title())  # Use title case as default
    if canonical in INDIAN_STATES:
        return canonical, "state"
    if canonical in INDIAN_UNION_TERRITORIES:
        return canonical, "union_territory"
    return "", None

def match_state(text: str) -> str:
    name, kind = match_region(text)
    return name if kind == "state" else ""

def match_union_territory(text: str) -> str:
    name, kind = match_region(text)
    return name if kind == "union_territory" else ""

def detect_state_from_text(text: str) -> str:
    """
    Comprehensive state detection from court document text
    Returns the detected state/UT name or "not in document"
    """
    import re
    
    # Try to find court name first
    court_match = re.search(r'(?:IN THE )?HIGH COURT OF (?:JUDICATURE AT )?([A-Z\s&]+?)(?:\s+AT|\n|$)', text, re.IGNORECASE)

    if court_match:
        court_str = court_match.group(1).strip()
        print(f"Found court string: '{court_str}'")
        
        # Use match_region for efficient single-call matching
        region_name, region_type = match_region(court_str)
        if region_name:
            state = region_name
            print(f"Matched {region_type}: '{state}'")
            return state
        else:
            # fallback: try whole text
            region_name, region_type = match_region(text)
            state = region_name if region_name else ""
            if state:
                print(f"Matched {region_type} from full text: '{state}'")
                return state
            else:
                print("No region found in full text")
                return "not in document"
    else:
        print("No court match found")
        region_name, region_type = match_region(text)
        state = region_name if region_name else "not in document"
        if region_name:
            print(f"Matched {region_type} from full text: '{state}'")
        else:
            print("No region found in full text")
        return state