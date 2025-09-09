# General Patterns
# Common fallback patterns that work across all states

GENERAL_PATTERNS = {
    "case_number": [
        r'(?:BAIL\s+APPL\.?|B\.A\.?|BAIL\s+APPLICATION)\s*NO\.?\s*(\d+)\s*OF\s*(\d{4})',
        r'(?:CWP|WRIT PETITION|W\.P\.)\s*NO\.?\s*(\d+)\s*OF\s*(\d{4})',
        r'(?:CRL\.?\s*P\.?|CRIMINAL\s+PETITION)\s*NO\.?\s*(\d+)\s*OF\s*(\d{4})',
        r'(?:CRL\.?\s*A\.?|CRIMINAL\s+APPEAL)\s*NO\.?\s*(\d+)\s*OF\s*(\d{4})',
        r'(\d{4}/[A-Z]{3}/\d+)',
        r'([A-Z\.]+\s*NO\.?\s*\d+\s*OF\s*\d{4})',
        r'Case\s+No\.?\s*:?\s*([A-Z0-9\-\/\s]+?)(?:\s+of\s+\d{4}|\n|$)'
    ],
    
    "order_date": [
        r'dated\s+this\s+the\s+(\d{1,2}(?:st|nd|rd|th)?\s+day\s+of\s+\w+,?\s+\d{4})',
        r'(?:friday|monday|tuesday|wednesday|thursday|saturday|sunday),?\s+the\s+(\d{1,2}(?:st|nd|rd|th)?\s+day\s+of\s+\w+,?\s+\d{4})',
        r'(\d{1,2}(?:st|nd|rd|th)?\s+day\s+of\s+\w+,?\s+\d{4})',
        r'(\d{2}\.\d{2}\.\d{4})',
        r'(\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4})',
        r'Date\s+of\s+(?:Decision|Judgment|Order)\s*:\s*(\d{2}\.\d{2}\.\d{4})',
        r'(\d{2}\-\d{2}\-\d{4})',
        r'(\d{1,2}\/\d{1,2}\/\d{4})'
    ],
    
    "judge_name": [
        r'the\s+honourable\s+mr\.?\s*justice\s+([A-Z\s\.\,]+?)(?:\s*\n|$)',
        r'([A-Z\s\.,]+?),?\s+j\.-+',
        r'justice\s+([A-Z\s\.,]+?)(?:\s*\n|$)',
        r'hon\'ble\s+mr\.?\s*justice\s+([A-Z\s\.\,]+?)(?:\s*\n|$)',
        r'CORAM\s*:\s*HON\'BLE\s+(?:MR\.?\s+)?JUSTICE\s+([A-Z\s\.,]+?)(?:\s*J\.|\n)',
        r'Per\s*:\s*([A-Z\s\.,]+?),?\s+J\.',
        r'BEFORE\s*:\s*([A-Z\s\.,]+?),?\s+J\.'
    ],
    
    "court_name": [
        r'in\s+the\s+(high\s+court\s+of\s+[A-Z\s]+?)(?:\s+at\s+[A-Z\s]+)?',
        r'IN\s+THE\s+(HIGH\s+COURT\s+OF\s+[A-Z\s]+?)(?:\s+AT\s+[A-Z\s]+)?',
        r'IN\s+THE\s+(HIGH\s+COURT\s+OF\s+JUDICATURE\s+AT\s+[A-Z\s]+)'
    ],
    
    "petitioner_name": [
        r'petitioner[\/]?(?:\(s\))?(?:\/accused\s+no\.\d+)?\s*:?\s*([a-z\s]+?),\s*aged',
        r'petitioner[\/]?(?:\(s\))?(?:\/accused\s+no\.\d+)?\s*:?\s*([a-z\s]+?)(?:,|\n)',
        r'appellant[\/]?(?:\(s\))?\s*:?\s*([A-Z\s]+?),?\s*(?:aged|through|\n)'
    ],
    
    "respondent_name": [
        r'respondents?[\/]?(?:\(s\))?(?:\/complainant)?\s*:?\s*\d*\s*\d*\s*(state\s+of\s+[a-z\s]+)',
        r'respondents?[\/]?(?:\(s\))?(?:\/complainant)?\s*:?\s*\d*\s*\d*\s*([a-z\s,]+?)(?:,?\s*represented|\n)',
        r'\d+\s*\n\s*(STATE\s+OF\s+[A-Z\s]+)',
        r'(?:state|union\s+of\s+india|govt\.|government)'
    ],
    
    "fir_crime_no": [
        r'crime\s+no\.?\s*(\d+\/\d{4})\s+of\s+([a-z\s]+?)\s+police\s+station',
        r'FIR\s+No\.?\s*(\d+\/\d{4})',
        r'Case\s+No\.?\s*(\d+\/\d{4})'
    ],
    
    "police_station": [
        r'of\s+([a-z\s]+?)\s+police\s+station',
        r'P\.S\.?\s+([A-Z\s]+)',
        r'Police\s+Station\s+([A-Z\s]+)'
    ],
    
    "statutes_offences": [
        r'section\s+(\d+[a-z]*(?:\([a-z0-9]+\))?)\s+of\s+the\s+([^,\n]+?)(?:,|and|\.|$)',
        r'under\s+section\s+(\d+[a-z]*)\s+of\s+the\s+([^,\n]+?)',
        r'Section\s+(\d+[A-Z]*)\s+of\s+([^,\n]+?)(?:,|and|\.|$)',
        r'u/s\s+(\d+[A-Z]*)\s+([^,\n]+?)'
    ],
    
    "decision": [
        r'i\s+do\s+not\s+think\s+this\s+is\s+a\s+fit\s+case\s+to\s+grant\s+([^.]+)',
        r'(?:held|decided|ordered)\s*:?\s*([^.]+?)(?:\.|$)',
        r'it\s+is\s+(?:held|ordered)\s+that\s+([^.]+?)'
    ],
    
    "directions": [
        r'in\s+the\s+event\s+([^.]+?\.)',
        r'therefore,?\s+the\s+following\s+directions\s+are\s+issued\s*:?\s*-?\s*(.*?)(?:\d+\.|\n\n|$)',
        r'accordingly,?\s+([^.]+?\.)',
        r'it\s+is\s+directed\s+that\s+([^.]+?\.)'
    ],
    
    "disposition": [
        r'the\s+(bail\s+application\s+is\s+disposed\s+of\s+as\s+above)',
        r'(?:petition|appeal)\s+is\s+(dismissed|allowed|disposed\s+of)',
        r'(?:petition|appeal)\s+(stands\s+disposed\s+of)'
    ],
    
    "advocates": [
        r'for\s+(?:petitioner|appellant)\s*:\s*(.*?)(?:\s+for\s+respondent|\n\n)',
        r'for\s+respondent\s*:\s*(.*?)(?:\n\n|$)',
        r'([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*),?\s+Adv\.?',
        r'Mr\.\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
        r'Ms\.\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)'
    ],
    
    "crime_details": [
        r'allegation\s+(?:is\s+)?that\s+([^\.]+?)\.?',
        r'accused\s+(?:of|with)\s+([^\.]+?)\.?',
        r'charged\s+(?:for|with)\s+([^\.]+?)\.?'
    ],
    
    "judgment": [
        r'JUDGMENT\s*\n\s*(.*?)(?=\n\s*\d+\.|$)',
        r'judgment\s*\n\s*(.*?)(?=\n\s*\d+\.|$)',
        r'O\s+R\s+D\s+E\s+R\s*\n\s*(.*?)(?=\n\s*\d+\.|$)',
        r'order\s*\n\s*(.*?)(?=\n\s*\d+\.|$)',
        r'(?:CONSIDERING|AFTER\s+CONSIDERING)\s+([^.]+?)(?:\.|$)',
        r'(?:considering|after\s+considering)\s+([^.]+?)(?:\.|$)'
    ]
}

# Party type classification patterns
PARTY_TYPE_PATTERNS = {
    "government": [
        r'state\s+of\s+\w+',
        r'government',
        r'union\s+of\s+india',
        r'central\s+government',
        r'ministry\s+of',
        r'department\s+of',
        r'commissioner',
        r'collector',
        r'superintendent\s+of\s+police'
    ],
    "ngo": [
        r'society',
        r'trust',
        r'foundation',
        r'welfare\s+association',
        r'ngo',
        r'non.governmental'
    ],
    "organization": [
        r'limited',
        r'ltd\.',
        r'private\s+limited',
        r'pvt\.\s*ltd\.',
        r'company',
        r'corporation',
        r'& ors',
        r'and\s+others',
        r'bank',
        r'insurance'
    ],
    "individual": [
        r's\/o',
        r'd\/o',
        r'w\/o',
        r'h\/o',
        r'aged\s+\d+',
        r'resident\s+of',
        r'r\/o'
    ]
}

# Additional utility patterns for common extractions
COMMON_PATTERNS = {
    "email": [
        r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
    ],
    "phone": [
        r'(\+91[-\s]?\d{10})',
        r'(\d{10})',
        r'(\d{3}[-\s]?\d{3}[-\s]?\d{4})'
    ],
    "aadhar": [
        r'(\d{4}\s\d{4}\s\d{4})',
        r'(\d{12})'
    ],
    "pan": [
        r'([A-Z]{5}\d{4}[A-Z])'
    ]
}
