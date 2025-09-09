# Regex patterns for MEGHALAYA courts

PATTERNS = {
    "court_name": [
        r"HIGH COURT OF MEGHALAYA\s*AT SHILLONG",  # For "HIGH COURT OF MEGHALAYA AT SHILLONG"
        r"HIGH COURT OF MEGHALAYA",  # For "HIGH COURT OF MEGHALAYA"
        r"IN THE HIGH COURT OF ([^\n]+)",
        r"HIGH COURT OF ([^\n]+)",
        r"([^\n]*HIGH COURT[^\n]*)",
        r"SUPREME COURT OF INDIA",
        r"IN THE COURT OF ([^\n]+)"
    ],
    
    "case_number": [
        r"AB No\.\s*(\d+\s*of\s*\d{4})",  # For "AB No. 13 of 2025"
        r"(?:WRIT PETITION|W\.P\.|WP|CRIMINAL PETITION|CIVIL APPEAL|SECOND APPEAL|MOTOR ACCIDENT)\s*(?:NO\.?|Number)?\s*:?\s*([\d\/]+\s*(?:of|OF)\s*\d{4})",
        r"([A-Z\.\s]*\d+\s*(?:of|OF)\s*\d{4})",
        r"Case\s*No\.?\s*([\d\/]+)",
        r"([A-Z][A-Z\.\s]*\d+\s*[\d\/]*\s*(?:of|OF)\s*\d{4})"
    ],
    
    "order_date": [
        r"Date of Decision:\s*(\d{2}\.\d{2}\.\d{4})",  # For "Date of Decision: 24.06.2025"
        r"(?:FRIDAY|MONDAY|TUESDAY|WEDNESDAY|THURSDAY|SATURDAY|SUNDAY),?\s*THE\s*([^\n]+TWO THOUSAND[^\n]+)",
        r"(?:Order Date|Date of Order|Judgment|JUDGMENT)\s*[:-]?\s*([\d{1,2}[\.\/\-][\d{1,2}][\.\/\-]\d{4})",
        r"([\d{1,2}[\.\/\-][\d{1,2}][\.\/\-]\d{4})",
        r"Decided on\s*[:-]?\s*([\d{1,2}[\.\/\-][\d{1,2}][\.\/\-]\d{4})"
    ],
    
    "judge_name": [
        r"Hon'ble Mr\.\s*Justice\s+([A-Z\.\s]+),\s*Judge",  # For "Hon'ble Mr. Justice W. Diengdoh, Judge"
        r"Hon'ble Mr\.\s*Justice\s+([A-Z\.\s]+)",  # For "Hon'ble Mr. Justice W. Diengdoh"
        r"Justice\s+([A-Z\.\s]+),\s*Judge",  # Simple pattern for "Justice W. Diengdoh, Judge"
        r"PRESENT[^\n]*\n[^\n]*JUSTICE\s+([^\n]+)",
        r"(?:HON\'BLE|HONOURABLE)\s*(?:MR\.|MS\.|MRS\.)?\s*JUSTICE\s+([^\n]+)",
        r"\(Presided over by[^)]*([^)]+)\)",
        r"BEFORE\s+([^\n]+JUSTICE[^\n]+)",
        r"CORAM[^\n]*\n[^\n]*JUSTICE\s+([^\n]+)"
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
    
    "alternate_case_number": [
        r"P\.S Case No\.\s*(\d+\(\d+\)\s*of\s*\d{4})",  # For "P.S Case No. 64(03) of 2025"
        r"Sadar P\.S case",  # Reference to Sadar P.S case
        r"connected with\s+([A-Z\.\s]*\d+\s*of\s*\d{4})",  # For connected cases
        r"also in\s+([A-Z\.\s]*\d+\s*of\s*\d{4})",  # For also mentioned cases
        r"with\s+([A-Z\.\s]*\d+\s*of\s*\d{4})",  # For cases mentioned with "with"
        r"FIR.*?(\d+/\d{4})",  # For FIR numbers if any
        r"Civil Appeal\s*(?:No\.)?\s*(\d+[\-/]\d{4})"  # For Civil Appeal cases
    ],
    
    "bench": [
        r"(Single Judge)",  # If one judge found, it's Single Judge
        r"(Division Bench)",
        r"(Full Bench)"
    ],
    
    "document_type": [
        r"(ORDER \(ORAL\))",  # For "ORDER (ORAL)"
        r"(JUDGMENT)",
        r"(ORDER)",
        r"(WRIT PETITION)",
        r"(CRIMINAL PETITION)",
        r"(CIVIL APPEAL)",
        r"(ANTICIPATORY BAIL)",  # For anticipatory bail applications
        r"(PRE-ARREST BAIL)"  # For pre-arrest bail applications
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
