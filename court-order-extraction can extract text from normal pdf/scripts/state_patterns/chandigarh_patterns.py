# Regex patterns for CHANDIGARH courts

PATTERNS = {
    "court_name": [
        r"HIGH COURT OF PUNJAB AND HARYANA",
        r"PUNJAB AND HARYANA HIGH COURT",
        r"IN THE HIGH COURT OF ([^\n]+)",
        r"HIGH COURT OF ([^\n]+)",
        r"([^\n]*HIGH COURT[^\n]*)",
        r"SUPREME COURT OF INDIA",
        r"IN THE COURT OF ([^\n]+)"
    ],
    
    "case_number": [
        r"C\.W\.P\. No\.(\d+\s*of\s*\d{4})",
        r"regular second appeal no\.(\d+\s*of\s*\d{4})",
        r"(?:WRIT PETITION|W\.P\.|WP|CRIMINAL PETITION|CIVIL APPEAL|SECOND APPEAL|MOTOR ACCIDENT)\s*(?:NO\.?|Number)?\s*:?\s*([\d\/]+\s*(?:of|OF)\s*\d{4})",
        r"([A-Z\.\s]*\d+\s*(?:of|OF)\s*\d{4})",
        r"Case\s*No\.?\s*([\d\/]+)",
        r"([A-Z][A-Z\.\s]*\d+\s*[\d\/]*\s*(?:of|OF)\s*\d{4})"
    ],
    
    "alternate_case_number": [
        r"C\.O\.C\.P\.\s*NO\.\s*(\d+\s*OF\s*\d{4})",
        r"LPA No\.\s*(\d+\s*of\s*\d{4})",
        r"CWP No\.\s*(\d+\s*of\s*\d{4})",
        r"C\.W\.P\. No\.(\d+\s*of\s*\d{4})",
        r"Civil suit No\.(\d+\s*of\s*\d{4})",
        r"appeal no\.(\d+\s*of\s*\d{4})",
        r"(?:Criminal Appeal|Civil Appeal|Writ Petition|Review Petition)\s*No\.\s*(\d+\/\d{4})",
        r"(?:W\.P\.|WP|Appeal|Petition)\s*(?:NO\.?|Number|No\.)\s*(\d+\/\d{4})"
    ],
    
    "order_date": [
        r"(\d{1,2}(?:st|nd|rd|th)\s+[A-Z][a-z]+,\s*\d{4})",
        r"(?:FRIDAY|MONDAY|TUESDAY|WEDNESDAY|THURSDAY|SATURDAY|SUNDAY),?\s*THE\s*([^\n]+TWO THOUSAND[^\n]+)",
        r"(?:Order Date|Date of Order|Judgment|JUDGMENT)\s*[:-]?\s*(\d{1,2}[\.\/\-]\d{1,2}[\.\/\-]\d{4})",
        r"(\d{1,2}[\.\/\-]\d{1,2}[\.\/\-]\d{4})",
        r"Decided on\s*[:-]?\s*(\d{1,2}[\.\/\-]\d{1,2}[\.\/\-]\d{4})"
    ],
    
    "judge_name": [
        r"Before ([A-Z][a-z]+\s+[A-Z][a-z]+\s+[A-Z][a-z]+),\s*J\.",
        r"Before ([A-Z]\.[A-Z]\.\s+[A-Z][a-z]+\s*&\s*[A-Z][a-z]+\s+[A-Z][a-z]+),\s*JJ\.",
        r"([A-Z][a-z]+\s+[A-Z][a-z]+\s+[A-Z][a-z]+),\s*J\.",
        r"Before ([A-Z]\.\s*[A-Z][a-z]+),\s*J\.",
        r"([A-Z]\.\s*[A-Z][A-Z]+),\s*J\.\s*\(ORAL\)",
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
        r"CWP",
        r"Civil Writ Petition",
        r"second appeal",
        r"Criminal Appeal",
        r"Civil Appeal",
        r"Second Appeal",
        r"Writ Petition",
        r"Review Petition",
        r"Special Leave Petition",
        r"Transfer Petition",
        r"Contempt Petition"
    ],
    
    "statutes_sections": [
        r"Article (\d+) of the Constitution of India",
        r"Article (\d+) Constitution of India",
        r"Article (\d+) of Constitution of India",
        r"Section (\d+) of ([^\n]+Act[^\n]*)",
        r"(\w+ Act,? \d{4})",
        r"The ([^\n]+Act[^\n]*\d{4})",
        r"under ([^\n]+Act[^\n]*)"
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
