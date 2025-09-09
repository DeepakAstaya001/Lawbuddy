# Regex patterns for MANIPUR courts

PATTERNS = {
    "court_name": [
        r"IN THE (HIGH COURT OF MANIPUR)",  # For "IN THE HIGH COURT OF MANIPUR"
        r"IN THE HIGH COURT OF ([^\n]+)",
        r"HIGH COURT OF ([^\n]+)",
        r"([^\n]*HIGH COURT[^\n]*)",
        r"SUPREME COURT OF INDIA",
        r"IN THE COURT OF ([^\n]+)"
    ],
    
    "case_number": [
        r"(?:WRIT PETITION|W\.P\.|WP|CRIMINAL PETITION|CIVIL APPEAL|SECOND APPEAL|MOTOR ACCIDENT)\s*(?:NO\.?|Number)?\s*:?\s*([\d\/]+\s*(?:of|OF)\s*\d{4})",
        r"([A-Z\.\s]*\d+\s*(?:of|OF)\s*\d{4})",
        r"Case\s*No\.?\s*([\d\/]+)",
        r"([A-Z][A-Z\.\s]*\d+\s*[\d\/]*\s*(?:of|OF)\s*\d{4})"
    ],
    
    "order_date": [
        r"Date of Judgment & Order\s*::\s*(\d{2}-\d{2}-\d{4})",  # For "Date of Judgment & Order :: 25-07-2016"
        r"(?:FRIDAY|MONDAY|TUESDAY|WEDNESDAY|THURSDAY|SATURDAY|SUNDAY),?\s*THE\s*([^\n]+TWO THOUSAND[^\n]+)",
        r"(?:Order Date|Date of Order|Judgment|JUDGMENT)\s*[:-]?\s*([\d{1,2}[\.\/\-][\d{1,2}][\.\/\-]\d{4})",
        r"([\d{1,2}[\.\/\-][\d{1,2}][\.\/\-]\d{4})",
        r"Decided on\s*[:-]?\s*([\d{1,2}[\.\/\-][\d{1,2}][\.\/\-]\d{4})"
    ],
    
    "judge_name": [
        r"B E F O R E\s*\n\s*HON'BLE MR\.\s*JUSTICE\s+([A-Z\.\s]+)",  # For "B E F O R E HON'BLE MR. JUSTICE KH. NOBIN SINGH"
        r"HON'BLE MR\.\s*JUSTICE\s+(KH\.\s*NOBIN\s*SINGH)",  # For specific judge
        r"JUSTICE\s+(KH\.\s*NOBIN\s*SINGH)",  # Simple pattern for this judge
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
        r"With\s*\n\s*W\.P\.\s*\(C\)\s*No\.\s*(\d+\s*of\s*\d{4})",  # For "With W.P. (C) No. 622 of 2015" - captures alternate cases after "With"
        r"(?:also|with|connected)\s+.*?(\d+\s*of\s*\d{4})",  # Generic connected case pattern
        r"SLP\s*\([C]\)\s*(?:No\.)?\s*(\d+[\-/]\d{4})",  # For SLP cases
        r"Civil Appeal\s*(?:No\.)?\s*(\d+[\-/]\d{4})"  # For Civil Appeal cases
    ],
    
    "bench": [
        r"(Single Judge)",  # If one judge found, it's Single Judge
        r"(Division Bench)",
        r"(Full Bench)"
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
