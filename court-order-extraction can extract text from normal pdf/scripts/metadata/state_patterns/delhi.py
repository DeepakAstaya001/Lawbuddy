# Delhi High Court Patterns
# Enhanced patterns for Delhi High Court legal document extraction

DELHI_PATTERNS = {
    "case_number": [
        # Delhi High Court specific formats
        r'W\.P\.\(C\)\s*(\d+/\d{4})',  # W.P.(C) 1065/2021
        r'W\.P\.\s*\(C\)\s*(\d+/\d{4})',  # W.P. (C) 1065/2021 - with space
        r'WP\(C\)\s*(\d+/\d{4})',  # WP(C) without dots
        r'WRIT\s+PETITION\s+\(C\)\s*NO\.?\s*(\d+/\d{4})',  # WRIT PETITION (C) NO. 1065/2021
        
        # Criminal Appeals and other Delhi formats
        r'CRL\.A\s*NO\.?\s*(\d+/\d{4})',  # CRL.A NO. 967/2008
        r'CRL\s+APPEAL\s*NO\.?\s*(\d+/\d{4})',
        r'FAO\s*NO\.?\s*(\d+/\d{4})',  # First Appeal from Order
        r'RFA\s*NO\.?\s*(\d+/\d{4})',  # Regular First Appeal
        
        # CM Applications
        r'CM\s+APPL\.?\s*NO\.?\s*(\d+/\d{4})',  # CM APPL. 39041/2019
        r'CM\s+APPLs?\.?\s*(\d+/\d{4})',  # CM APPLs.
        
        # Generic case number patterns for Delhi
        r'([A-Z\.]+\s*\(?[A-Z]*\)?\s*NO\.?\s*\d+/\d{4})',
        r'(\d+/\d{4})',  # Simple fallback for Delhi year format
    ],
    
    "order_date": [
        r'Date\s+of\s+Decision\s*:\s*(\d{2}\.\d{2}\.\d{4})',
        r'Date\s+of\s+Judgment\s*:\s*(\d{2}\.\d{2}\.\d{4})',
        r'(\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4})',
        r'(\d{2}\-\d{2}\-\d{4})',
        r'(\d{2}\.\d{2}\.\d{4})',
        r'Judgment\s+pronounced\s+on:\s*(\d{2}\s+[A-Za-z]+,?\s+\d{4})',
        r'Judgment\s+reserved\s+on:\s*(\d{2}\s+[A-Za-z]+,?\s+\d{4})'
    ],
    
    "judge_name": [
        r'CORAM\s*:\s*HON\'BLE\s+(?:MR\.?\s+)?JUSTICE\s+([A-Z\s\.,]+?)(?:\s*J\.|\n)',
        r'Per\s*:\s*([A-Z\s\.,]+?),?\s+J\.',
        r'Hon\'ble\s+(?:Mr\.?\s+)?Justice\s+([A-Z\s\.,]+?)',
        r'BEFORE\s*:\s*([A-Z\s\.,]+?),?\s+J\.',
        r'Author:\s+([A-Z\s\.,]+)',
        r'Bench:\s+([A-Z\s\.,]+)'
    ],
    
    "court_name": [
        r'IN\s+THE\s+(HIGH\s+COURT\s+OF\s+DELHI)(?:\s+AT\s+NEW\s+DELHI)?',
        r'in\s+the\s+(high\s+court\s+of\s+delhi)(?:\s+at\s+new\s+delhi)?',
        r'(HIGH\s+COURT\s+OF\s+DELHI)',
        r'(high\s+court\s+of\s+delhi)'
    ],
    
    "petitioner_name": [
        # Delhi High Court company/entity patterns
        r'(\w+(?:\s+\w+)*?)\s+(?:PRIVATE\s+LIMITED|PVT\.?\s+LTD\.?|LIMITED|LTD\.?)\s+\.{3,}\s+Petitioner',
        r'(\w+(?:\s+\w+)*?)\s+(?:PRIVATE\s+LIMITED|PVT\.?\s+LTD\.?|LIMITED|LTD\.?)\s+\.{3,}',
        r'([A-Z][A-Z\s&\.]+?)\s+\.{3,}\s+Petitioner',  # Entity names followed by dots
        r'([A-Z][A-Z\s&\.]+?)\s+\.{3,}',  # Entity names followed by dots
        
        # Individual petitioner patterns
        r'([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+\.{3,}\s+Petitioner',
        r'([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+\.{3,}',
        
        # Multiple petitioners
        r'([A-Z][A-Z\s&\.]+?)\s+&\s+(?:ANR|ORS)\.?\s+\.{3,}',
        r'([A-Z][A-Z\s&\.]+?)\s+AND\s+OTHERS?\s+\.{3,}'
    ],
    
    "respondent_name": [
        # Delhi High Court respondent patterns
        r'versus\s+([A-Z][A-Z\s&\.]+?)\s+\.{3,}\s+Respondent',
        r'versus\s+([A-Z][A-Z\s&\.]+?)\s+\.{3,}',
        r'v[s]?\.\s+([A-Z][A-Z\s&\.]+?)\s+\.{3,}',
        
        # Government respondents
        r'(UNION\s+OF\s+INDIA(?:\s+&\s+(?:ANR|ORS)\.?)?)',
        r'(GOVERNMENT\s+OF\s+[A-Z\s]+)',
        r'(STATE\s+OF\s+[A-Z\s]+)',
        r'([A-Z][A-Z\s&\.]+?)\s+&\s+(?:ANR|ORS)\.?\s+\.{3,}\s+Respondent'
    ],
    
    "advocates": [
        # Delhi specific advocate patterns - multiple advocates listed after "Through:"
        r'Through:\s+([^,\n]+(?:,\s*[^,\n]+)*)\s+Adv[s]?\.?',  # Through: Mr. X, Mr. Y, Advs.
        r'Through:\s+([^,\n]+)\s+Sr\.\s+Adv[s]?\.?',  # Senior Advocate
        r'Through:\s+([^,\n]+)\s+(?:Sr\.\s+)?Adv[s]?\.?\s+with',  # Lead advocate with others
        r'Through:\s+([^,\n]+(?:,\s*[^,\n]+)*)',  # All names after Through:
        
        # Multiple advocate patterns
        r'([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*),?\s+Sr\.\s+Adv[s]?\.?',  # Senior Advocates
        r'([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*),?\s+Adv[s]?\.?',  # Regular Advocates
        r'Mr\.\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',  # Mr. names
        r'Ms\.\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',  # Ms. names
        
        # For multiple advocates in same entry
        r'(?:Mr\.|Ms\.)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:,\s*(?:Mr\.|Ms\.)\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)*)',
        
        # Government pleader patterns
        r'([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*),?\s+(?:CGSC|CGS|SSC|JSC)',
        r'([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*),?\s+(?:UOI|for\s+UOI)'
    ],
    
    "statutes_offences": [
        # Delhi patterns for statutes
        r'Section\s+(\d+[A-C]?)\s+of\s+the\s+([^,\n\.]+?)(?:,|\.|\s+Act|\n)',
        r'under\s+Section\s+(\d+[A-C]?)\s+of\s+([^,\n\.]+?)(?:,|\.|\s+Act|\n)',
        r'u/s\s+(\d+[A-C]?)\s+([^,\n\.]+?)(?:,|\.|\s+Act|\n)',
        r'(\d+[A-C]?)\s+of\s+the\s+([^,\n\.]+?)(?:,|\.|\s+Act|\n)',
        
        # Tax related statutes common in Delhi HC
        r'Section\s+(\d+[A-Z]*)\s+of\s+the\s+(Income\s+Tax\s+Act)',
        r'Section\s+(\d+[A-Z]*)\s+of\s+the\s+(Goods\s+and\s+Services\s+Tax\s+Act)',
        r'Section\s+(\d+[A-Z]*)\s+of\s+the\s+(Companies\s+Act)'
    ],
    
    "decision": [
        # Delhi decision patterns
        r'(?:Court|Tribunal|Authority)\s+(?:held|decided|ruled)\s+that\s+([^\.]+?)\.?',
        r'(?:It\s+is\s+(?:held|decided|ruled|ordered))\s+that\s+([^\.]+?)\.?',
        r'(?:The\s+Court\s+(?:finds|holds|decides))\s+that\s+([^\.]+?)\.?',
        r'liable\s+to\s+have\s+([^\.]+?)\.?',
        r'(?:We\s+(?:hold|find|decide))\s+that\s+([^\.]+?)\.?'
    ],
    
    "directions": [
        # Delhi directions patterns
        r'(?:directed|ordered)\s+that\s+([^\.]+?)\.?',
        r'(?:It\s+is\s+(?:directed|ordered))\s+that\s+([^\.]+?)\.?',
        r'(?:The\s+(?:following\s+)?directions?\s+(?:are\s+)?(?:issued|given))\s*:?\s*([^\.]+?)\.?',
        r'shall\s+pay\s+([^\.]+?)\.?',
        r'(?:We\s+(?:direct|order))\s+that\s+([^\.]+?)\.?'
    ],
    
    "disposition": [
        # Delhi disposition patterns
        r'(?:petition|appeal|application)\s+is\s+(?:hereby\s+)?(dismissed|allowed|disposed\s+of)',
        r'(?:petition|appeal|application)\s+(?:stands\s+)?(dismissed|allowed|disposed\s+of)',
        r'(?:The\s+)?(?:writ\s+)?petition\s+is\s+(dismissed|allowed)',
        r'(?:The\s+)?appeal\s+is\s+(dismissed|allowed|disposed\s+of)'
    ],
    
    "fir_crime_no": [
        # Delhi FIR patterns
        r'FIR\s+No\.?\s*(\d+\/\d{4})',
        r'F\.I\.R\.?\s+No\.?\s*(\d+\/\d{4})',
        r'Case\s+No\.?\s*(\d+\/\d{4})',
        r'DD\s+No\.?\s*(\d+\/\d{4})'
    ],
    
    "police_station": [
        # Delhi police station patterns
        r'P\.S\.?\s+([A-Z\s]+)',
        r'Police\s+Station\s+([A-Z\s]+)',
        r'PS\s+([A-Z\s]+)',
        r'([A-Z\s]+?)\s+Police\s+Station'
    ],
    
    "crime_details": [
        # Crime description patterns for Delhi
        r'allegation\s+(?:is\s+)?that\s+([^\.]+?)\.?',
        r'accused\s+(?:of|with)\s+([^\.]+?)\.?',
        r'charged\s+(?:for|with)\s+([^\.]+?)\.?'
    ],
    
    "judgment": [
        # Delhi judgment patterns
        r'JUDGMENT\s*\n\s*(.*?)(?=\n\s*(?:\d+\.|ORDER|CONCLUSION)|$)',
        r'(?:We\s+(?:hold|conclude|find))\s+([^\.]+?)\.?',
        r'(?:In\s+view\s+of\s+the\s+above)\s*,?\s*([^\.]+?)\.?'
    ]
}
