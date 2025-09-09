# Regex patterns for UTTAR PRADESH courts

PATTERNS = {
    "court_name": [
        r"IN THE HIGH COURT OF ([^\n]+)",
        r"HIGH COURT OF ([^\n]+)",
        r"([^\n]*HIGH COURT[^\n]*)",
        r"SUPREME COURT OF INDIA",
        r"IN THE COURT OF ([^\n]+)"
    ],
    
    "case_number": [
        r"MATTERS UNDER ARTICLE 227 No\.\s*-\s*(\d+\s*of\s*\d{4})",
        r"(?:WRIT PETITION|W\.P\.|WP|CRIMINAL PETITION|CIVIL APPEAL|SECOND APPEAL|MOTOR ACCIDENT)\s*(?:NO\.?|Number)?\s*:?\s*([\d\/]+\s*(?:of|OF)\s*\d{4})",
        r"([A-Z\.\s]*\d+\s*(?:of|OF)\s*\d{4})",
        r"Case\s*No\.?\s*([\d\/]+)",
        r"([A-Z][A-Z\.\s]*\d+\s*[\d\/]*\s*(?:of|OF)\s*\d{4})"
    ],
    
    "alternate_case_number": [
        r"Regular Suit No\.(\d+\s*of\s*\d{4})",
        r"Miscellaneous Case No\.(\d+\/\d+\/\d{4})",
        r"Case No\.(\d+\/\d+\/\d{4})",
        r"(?:Criminal Appeal|Civil Appeal|Writ Petition|Review Petition)\s*No\.\s*(\d+\/\d{4})",
        r"(?:W\.P\.|WP|Appeal|Petition|Suit)\s*(?:NO\.?|Number|No\.)\s*(\d+\s*(?:of|\/)\s*\d{4})"
    ],
    
    "order_date": [
        r"Order Date\s*:-\s*(\d{1,2}\.\d{1,2}\.\d{4})",
        r"Order Date\s*:?\s*-?\s*(\d{1,2}\.\d{1,2}\.\d{4})",
        r"(?:FRIDAY|MONDAY|TUESDAY|WEDNESDAY|THURSDAY|SATURDAY|SUNDAY),?\s*THE\s*([^\n]+TWO THOUSAND[^\n]+)",
        r"(?:Order Date|Date of Order|Judgment|JUDGMENT)\s*[:-]?\s*(\d{1,2}[\.\/\-]\d{1,2}[\.\/\-]\d{4})",
        r"(\d{1,2}[\.\/\-]\d{1,2}[\.\/\-]\d{4})",
        r"Decided on\s*[:-]?\s*(\d{1,2}[\.\/\-]\d{1,2}[\.\/\-]\d{4})"
    ],
    
    "judge_name": [
        r"Hon'ble\s+([^,]+),J\.",
        r"Hon'ble\s+([A-Z][A-Za-z\s]+?)\s*,\s*J\.",
        r"Hon'ble\s+([A-Z][A-Za-z\s]+?)(?:,J\.|,\s*J\.)",
        r"Hon'ble ([A-Z][A-Za-z\s]+),J\.",
        r"([A-Z][A-Za-z\.\s]+), J\.",
        r"PRESENT[^\n]*\n[^\n]*JUSTICE\s+([^\n]+)",
        r"(?:HON\'BLE|HONOURABLE)\s*(?:MR\.|MS\.|MRS\.)?\s*JUSTICE\s+([^\n,]+)",
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
        r"MATTERS UNDER ARTICLE 227",
        r"Criminal Appeal",
        r"Civil Appeal",
        r"Second Appeal",
        r"Writ Petition",
        r"Review Petition",
        r"Special Leave Petition",
        r"Transfer Petition",
        r"Contempt Petition"
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
