# Karnataka High Court Patterns
# Patterns for Karnataka High Court legal document extraction

KARNATAKA_PATTERNS = {
    "case_number": [
        r'(?:CRIMINAL\s+PETITION|CRL\.?\s*P\.?)\s*NO\.?\s*(\d+)\s*OF\s*(\d{4})',
        r'(?:BAIL\s+PETITION|B\.P\.?)\s*NO\.?\s*(\d+)\s*OF\s*(\d{4})',
        r'(?:CRIMINAL\s+APPEAL|CRL\.?\s*A\.?)\s*NO\.?\s*(\d+)\s*OF\s*(\d{4})',
        r'(?:WRIT\s+PETITION|W\.P\.?)\s*NO\.?\s*(\d+)\s*OF\s*(\d{4})',
        r'([A-Z\.]+\s*NO\.?\s*\d+\s*OF\s*\d{4})'
    ],
    
    "order_date": [
        r'(\d{1,2}(?:st|nd|rd|th)?\s+\w+,?\s+\d{4})',
        r'(\d{2}\-\d{2}\-\d{4})',
        r'(\d{2}\.\d{2}\.\d{4})',
        r'(\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4})',
        r'Date\s+of\s+Decision\s*:\s*(\d{2}\.\d{2}\.\d{4})',
        r'(\d{1,2}\/\d{1,2}\/\d{4})'
    ],
    
    "judge_name": [
        r'Hon\'ble\s+(?:Mr\.?\s+)?Justice\s+([A-Z\s\.,]+?)',
        r'BEFORE\s*:\s*([A-Z\s\.,]+?),?\s+J\.',
        r'Hon\'ble\s+(?:Mr\.?\s+)?Justice\s+([A-Z\s\.,]+?)(?:\s*\n|$)',
        r'CORAM\s*:\s*([A-Z\s\.,]+?),?\s+J\.',
        r'([A-Z\s\.,]+?),?\s+J\.'
    ],
    
    "court_name": [
        r'IN\s+THE\s+(HIGH\s+COURT\s+OF\s+KARNATAKA)(?:\s+AT\s+BANGALORE)?',
        r'in\s+the\s+(high\s+court\s+of\s+karnataka)(?:\s+at\s+bangalore)?',
        r'(HIGH\s+COURT\s+OF\s+KARNATAKA)',
        r'(high\s+court\s+of\s+karnataka)'
    ],
    
    "petitioner_name": [
        r'PETITIONER\s*:?\s*([A-Z\s]+?),?\s*(?:AGED|THROUGH|\n)',
        r'petitioner\s*:?\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*),?\s*(?:aged|through|\n)',
        r'([A-Z][A-Z\s&\.]+?)\s+\.{3,}\s+Petitioner',
        r'([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+\.{3,}\s+Petitioner'
    ],
    
    "respondent_name": [
        r'RESPONDENT[S]*\s*:?\s*([A-Z\s&,]+?)(?:\s+through|\n)',
        r'respondent[s]*\s*:?\s*([A-Z][a-z\s&,]+?)(?:\s+through|\n)',
        r'(STATE\s+OF\s+KARNATAKA)',
        r'(state\s+of\s+karnataka)',
        r'(UNION\s+OF\s+INDIA)',
        r'(union\s+of\s+india)'
    ],
    
    "advocates": [
        r'for\s+petitioner\s*:\s*(.*?)(?:\s+for\s+respondent|\n\n)',
        r'for\s+respondent\s*:\s*(.*?)(?:\n\n|$)',
        r'([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*),?\s+Adv\.?',
        r'Mr\.\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
        r'Ms\.\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
        r'([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*),?\s+Sr\.\s+Adv\.?'
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
