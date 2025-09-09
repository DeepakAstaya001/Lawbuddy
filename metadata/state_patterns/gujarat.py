# Gujarat High Court Patterns
# Patterns for Gujarat High Court legal document extraction

GUJARAT_PATTERNS = {
    "case_number": [
        # Gujarat High Court specific formats
        r'R/CR\.A\s*NO\.?\s*(\d+/\d{4})',  # R/CR.A NO. 229/2020
        r'SPECIAL\s+CRIMINAL\s+APPLICATION\s*NO\.?\s*(\d+/\d{4})',
        r'SPECIAL\s+CIVIL\s+APPLICATION\s*NO\.?\s*(\d+/\d{4})',
        r'SCA\s*NO\.?\s*(\d+/\d{4})',  # SCA short form
        r'R/SCR\.A\s*NO\.?\s*(\d+/\d{4})',  # Regular Criminal Appeal
        r'R/FAO\s*NO\.?\s*(\d+/\d{4})',  # First Appeal from Order
        
        # General Gujarat patterns
        r'([A-Z]+/[A-Z\.]+)\s*NO\.?\s*(\d+/\d{4})',
        r'(\d+/\d{4})',  # Simple fallback
    ],
    
    "order_date": [
        r'Date\s+of\s+Decision\s*:\s*(\d{2}\.\d{2}\.\d{4})',
        r'(\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4})',
        r'(\d{2}-\d{2}-\d{4})',
        r'(\d{2}\.\d{2}\.\d{4})',
        r'Decided\s+on:\s*(\d{2}\s+[A-Za-z]+,?\s+\d{4})',
        r'Date\s+of\s+Hearing:\s*(\d{2}\s+[A-Za-z]+,?\s+\d{4})'
    ],
    
    "judge_name": [
        r'(?:HONBLE\s+)?(?:MR\.\s+)?JUSTICE\s+([A-Z\s\.]+?)(?:\s*J\.|\s*,|\n)',
        r'(?:Hon\'ble\s+)?(?:Mr\.\s+)?Justice\s+([A-Z\s\.]+?)',
        r'CORAM\s*:\s*([A-Z\s\.]+?),?\s+J\.',
        r'Before\s*:\s*([A-Z\s\.]+?),?\s+J\.',
        r'Author:\s+([A-Z\s\.]+)'
    ],
    
    "court_name": [
        r'IN\s+THE\s+(HIGH\s+COURT\s+OF\s+GUJARAT)(?:\s+AT\s+AHMEDABAD)?',
        r'in\s+the\s+(high\s+court\s+of\s+gujarat)(?:\s+at\s+ahmedabad)?',
        r'(HIGH\s+COURT\s+OF\s+GUJARAT)',
        r'(high\s+court\s+of\s+gujarat)'
    ],
    
    "petitioner_name": [
        # Gujarat specific patterns
        r'([A-Z][A-Z\s&\.]+?)\s+\.{3,}\s+Petitioner',
        r'([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+\.{3,}\s+Petitioner',
        r'([A-Z][A-Z\s&\.]+?)\s+\.{3,}',
        r'Petitioner\s*[-–]\s*([A-Z][A-Z\s&\.]+)',
        r'([A-Z][A-Z\s&\.]+?)\s+(?:and\s+others?\s+)?\.{3,}'
    ],
    
    "respondent_name": [
        r'versus\s+([A-Z][A-Z\s&\.]+?)\s+\.{3,}\s+Respondent',
        r'versus\s+([A-Z][A-Z\s&\.]+?)\s+\.{3,}',
        r'v[s]?\.\s+([A-Z][A-Z\s&\.]+?)\s+\.{3,}',
        r'Respondent\s*[-–]\s*([A-Z][A-Z\s&\.]+)',
        r'(STATE\s+OF\s+GUJARAT)',
        r'([A-Z][A-Z\s&\.]+?)\s+&\s+(?:ANR|ORS)\.?\s+\.{3,}'
    ],
    
    "advocates": [
        # Gujarat advocate patterns
        r'([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*),?\s+Adv\.?',
        r'Mr\.\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
        r'Ms\.\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
        r'([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*),?\s+for\s+the\s+(?:petitioner|respondent)',
        r'Advocate\s+for\s+[^:]+:\s+([^,\n]+)',
        r'([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*),?\s+AGP'
    ],
    
    "statutes_offences": [
        r'Section\s+(\d+[A-C]?)\s+of\s+the\s+([^,\n\.]+?)(?:,|\.|\s+Act|\n)',
        r'under\s+Section\s+(\d+[A-C]?)\s+of\s+([^,\n\.]+?)(?:,|\.|\s+Act|\n)',
        r'u/s\s+(\d+[A-C]?)\s+([^,\n\.]+?)(?:,|\.|\s+Act|\n)',
        r'(\d+[A-C]?)\s+of\s+the\s+([^,\n\.]+?)(?:,|\.|\s+Act|\n)'
    ],
    
    "decision": [
        r'(?:Court|Tribunal)\s+(?:held|decided|ruled)\s+that\s+([^\.]+?)\.?',
        r'(?:It\s+is\s+(?:held|decided|ruled))\s+that\s+([^\.]+?)\.?',
        r'(?:We\s+(?:hold|find|decide))\s+that\s+([^\.]+?)\.?'
    ],
    
    "directions": [
        r'(?:directed|ordered)\s+that\s+([^\.]+?)\.?',
        r'(?:It\s+is\s+(?:directed|ordered))\s+that\s+([^\.]+?)\.?',
        r'shall\s+pay\s+([^\.]+?)\.?'
    ],
    
    "disposition": [
        r'(?:petition|appeal|application)\s+is\s+(?:hereby\s+)?(dismissed|allowed|disposed\s+of)',
        r'(?:petition|appeal|application)\s+(?:stands\s+)?(dismissed|allowed|disposed\s+of)'
    ],
    
    "fir_crime_no": [
        r'FIR\s+No\.?\s*(\d+\/\d{4})',
        r'F\.I\.R\.?\s+No\.?\s*(\d+\/\d{4})',
        r'Case\s+No\.?\s*(\d+\/\d{4})',
        r'DD\s+No\.?\s*(\d+\/\d{4})'
    ],
    
    "police_station": [
        r'P\.S\.?\s+([A-Z\s]+)',
        r'Police\s+Station\s+([A-Z\s]+)',
        r'PS\s+([A-Z\s]+)',
        r'([A-Z\s]+?)\s+Police\s+Station'
    ],
    
    "crime_details": [
        r'allegation\s+(?:is\s+)?that\s+([^\.]+?)\.?',
        r'accused\s+(?:of|with)\s+([^\.]+?)\.?',
        r'charged\s+(?:for|with)\s+([^\.]+?)\.?'
    ],
    
    "judgment": [
        r'JUDGMENT\s*\n\s*(.*?)(?=\n\s*(?:\d+\.|ORDER|CONCLUSION)|$)',
        r'(?:We\s+(?:hold|conclude|find))\s+([^\.]+?)\.?',
        r'(?:In\s+view\s+of\s+the\s+above)\s*,?\s*([^\.]+?)\.?'
    ]
}
