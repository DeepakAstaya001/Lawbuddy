# Regex patterns for BIHAR courts

PATTERNS = {
    "court_name": [
        r"IN THE HIGH COURT OF ([^\n]+)",
        r"HIGH COURT OF ([^\n]+)",
        r"([^\n]*HIGH COURT[^\n]*)",
        r"SUPREME COURT OF INDIA",
        r"IN THE COURT OF ([^\n]+)"
    ],
    
    "case_number": [
        r"Miscellaneous Jurisdiction Case No\.(\d+\s*of\s*\d{4})",
        r"Letters Patent Appeal No\.(\d+\s*of\s*\d{4})",
        r"Civil Writ Jurisdiction Case No\.(\d+\s*of\s*\d{4})",
        r"Case No\.(\d+\s*of\s*\d{4})",
        r"(?:WRIT PETITION|W\.P\.|WP|CRIMINAL PETITION|CIVIL APPEAL|SECOND APPEAL|MOTOR ACCIDENT)\s*(?:NO\.?|Number)?\s*:?\s*([\d\/]+\s*(?:of|OF)\s*\d{4})",
        r"([A-Z\.\s]*\d+\s*(?:of|OF)\s*\d{4})",
        r"([A-Z][A-Z\.\s]*\d+\s*[\d\/]*\s*(?:of|OF)\s*\d{4})"
    ],
    
    "alternate_case_number": [
        r"CR\.\s*MISC\.\s*No\.(\d+\s*of\s*\d{4}\(\d+\))",
        r"MJC No\.(\d+\s*of\s*\d{4}\(\d+\))",
        r"L\.P\.A No\.(\d+\s*of\s*\d{4}\(\d+\))",
        r"CWJC No\.(\d+\s*of\s*\d{4}\(\d+\))",
        r"CWJC No\.\s*(\d+\s*of\s*\d{4})",
        r"Patna High Court CWJC No\.(\d+\s*of\s*\d{4})\(\d+\)",
        r"([A-Z]{2,10}\d{8,15})",
        r"(\d{4}:[A-Z\-]+:\d+)"
    ],
    
    "document_type": [
        r"(CRIMINAL MISCELLANEOUS)",
        r"(Miscellaneous Jurisdiction Case)",
        r"(MJC)",
        r"(contempt petition)",
        r"(Letters Patent Appeal)",
        r"(L\.P\.A)",
        r"(Civil Writ Jurisdiction)",
        r"(CWJC)",
        r"(WRIT PETITION)",
        r"(CRIMINAL PETITION)", 
        r"(CIVIL APPEAL)",
        r"(SECOND APPEAL)",
        r"(MOTOR ACCIDENT CLAIM)",
        r"(CONTEMPT PETITION)"
    ],
    
    "order_date": [
        r"(?:FRIDAY|MONDAY|TUESDAY|WEDNESDAY|THURSDAY|SATURDAY|SUNDAY),?\s*THE\s*([^\n]+TWO THOUSAND[^\n]+)",
        r"(?:Order Date|Date of Order|Judgment|JUDGMENT)\s*[:-]?\s*([\d{1,2}[\.\/\-][\d{1,2}][\.\/\-]\d{4})",
        r"([\d{1,2}[\.\/\-][\d{1,2}][\.\/\-]\d{4})",
        r"Decided on\s*[:-]?\s*([\d{1,2}[\.\/\-][\d{1,2}][\.\/\-]\d{4})"
    ],
    
    "judge_name": [
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
