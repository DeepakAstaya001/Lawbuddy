# Regex patterns for TELANGANA courts

PATTERNS = {
    "court_name": [
        r"HIGH COURT OF TELANGANA",
        r"TELANGANA HIGH COURT", 
        r"THE HON'BLE.*?JUSTICE.*?(HIGH COURT OF TELANGANA)",  # Default inference
        r"IN THE HIGH COURT OF ([^\n]+)",
        r"HIGH COURT OF ([^\n]+)",
        r"([^\n]*HIGH COURT[^\n]*)",
        r"SUPREME COURT OF INDIA",
        r"IN THE COURT OF ([^\n]+)"
    ],
    
    "case_number": [
        r"WRIT PETITION No\.(\d+\s*of\s*\d{4})",
        r"(?:WRIT PETITION|W\.P\.|WP|CRIMINAL PETITION|CIVIL APPEAL|SECOND APPEAL|MOTOR ACCIDENT)\s*(?:NO\.?|Number)?\s*:?\s*([\d\/]+\s*(?:of|OF)\s*\d{4})",
        r"([A-Z\.\s]*\d+\s*(?:of|OF)\s*\d{4})",
        r"Case\s*No\.?\s*([\d\/]+)",
        r"([A-Z][A-Z\.\s]*\d+\s*[\d\/]*\s*(?:of|OF)\s*\d{4})"
    ],
    
    "alternate_case_number": [
        r"wp_(\d+_\d{4})",
        r"([A-Z]+\/\d+\/\d{4})",
        r"(?:Criminal Appeal|Civil Appeal|Writ Petition|Review Petition)\s*No\.\s*(\d+\/\d{4})",
        r"(?:W\.P\.|WP|Appeal|Petition)\s*(?:NO\.?|Number|No\.)\s*(\d+\/\d{4})"
    ],
    
    "order_date": [
        r"Date\s*:\s*(\d{2}\.\d{2}\.\d{4})",
        r"(?:FRIDAY|MONDAY|TUESDAY|WEDNESDAY|THURSDAY|SATURDAY|SUNDAY),?\s*THE\s*([^\n]+TWO THOUSAND[^\n]+)",
        r"(?:Order Date|Date of Order|Judgment|JUDGMENT)\s*[:-]?\s*(\d{1,2}[\.\/\-]\d{1,2}[\.\/\-]\d{4})",
        r"(\d{1,2}[\.\/\-]\d{1,2}[\.\/\-]\d{4})",
        r"Decided on\s*[:-]?\s*(\d{1,2}[\.\/\-]\d{1,2}[\.\/\-]\d{4})"
    ],
    
    "judge_name": [
        r"THE HON'BLE SMT\. JUSTICE ([A-Z\.\s]+)",
        r"JUSTICE ([A-Z\.\s]+)",
        r"Hon'ble.*?JUSTICE ([A-Z][A-Z\s]+?)(?:\n|Advocate|$)",
        r"PRESENT[^\n]*\n[^\n]*JUSTICE\s+([^\n]+)",
        r"(?:HON\'BLE|HONOURABLE)\s*(?:MR\.|MS\.|MRS\.|SMT\.)?\s*JUSTICE\s+([^\n,]+)",
        r"\(Presided over by[^)]*([^)]+)\)",
        r"BEFORE\s+([^\n]+JUSTICE[^\n]+)",
        r"CORAM[^\n]*\n[^\n]*JUSTICE\s+([^\n]+)"
    ],
    
    "bench": [
        r"Division Bench",
        r"Single Judge", 
        r"Full Bench",
        r"Special Bench",
        r"Constitution Bench"
    ],
    
    "document_type": [
        r"WRIT PETITION",
        r"Criminal Appeal",
        r"Civil Appeal",
        r"Second Appeal",
        r"Review Petition",
        r"Special Leave Petition",
        r"Transfer Petition",
        r"Contempt Petition"
    ],
    
    "counsel": [
        {
            "pattern": r"Counsel for (?:the )?(?:Appellant|Petitioner)(?:s)?[^\n]*[:-]\s*([^\n]+)",
            "for": "Appellant/Petitioner"
        },
        {
            "pattern": r"Counsel for (?:the )?(?:Respondent|State)(?:s)?[^\n]*[:-]\s*([^\n]+)",
            "for": "Respondent/State"
        },
        {
            "pattern": r"For (?:the )?(?:Appellant|Petitioner)(?:s)?[^\n]*[:-]\s*([^\n]+)",
            "for": "Appellant/Petitioner"
        },
        {
            "pattern": r"For (?:the )?(?:Respondent|State)(?:s)?[^\n]*[:-]\s*([^\n]+)",
            "for": "Respondent/State"
        }
    ],
    
    "parties": [
        {
            "pattern": r"([A-Z][A-Z\s]+),\s*(?:S\/O|W\/O|D\/O)\.?\s*[^,\n]*[^\n]*",
            "type": "individual"
        },
        {
            "pattern": r"([A-Z][A-Z\s]*(?:COMPANY|CORPORATION|LTD|LIMITED|INSURANCE|BANK)[^\n]*)",
            "type": "company"
        },
        {
            "pattern": r"(STATE OF [A-Z\s]+|GOVERNMENT OF [A-Z\s]+|UNION OF INDIA)",
            "type": "government"
        }
    ]
}
