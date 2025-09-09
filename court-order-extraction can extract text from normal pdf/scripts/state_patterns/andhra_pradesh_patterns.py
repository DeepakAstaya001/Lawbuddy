# Regex patterns for ANDHRA PRADESH courts

PATTERNS = {
    "court_name": [
        r"IN THE HIGH COURT OF ANDHRA PRADESH AT AMARAVATI",
        r"HIGH COURT OF ANDHRA PRADESH",
        r"IN THE HIGH COURT OF ANDHRA PRADESH",
        r"ANDHRA PRADESH HIGH COURT"
    ],
    
    "case_number": [
        r"MOTOR ACCIDENT CIVIL MISCELLANEOUS APPEAL NO:\s*(\d+/\d{4})",
        r"M\.A\.C\.M\.A\.No\.(\d+\s*of\s*\d{4})",
        r"(?:WRIT PETITION|W\.P\.|WP)\s*(?:NO\.?|Number)?\s*:?\s*([\d\/]+\s*(?:of|OF)\s*\d{4})",
        r"(?:CRIMINAL PETITION|Crl\.P\.|CRL\.P\.)\s*(?:NO\.?)?\s*:?\s*([\d\/]+\s*(?:of|OF)\s*\d{4})",
        r"(?:CIVIL APPEAL|C\.A\.|CA)\s*(?:NO\.?)?\s*:?\s*([\d\/]+\s*(?:of|OF)\s*\d{4})",
        r"([A-Z][A-Z\.\s]*\d+\s*[\d\/]*\s*(?:of|OF)\s*\d{4})",
        r"Case\s*No\.?\s*([\d\/]+)",
        r"Petition\s*No\.?\s*([\d\/]+)"
    ],
    
    "alternate_case_number": [
        r"(\d+/\d{4})",
        r"No\.\s*(\d+\s*of\s*\d{4})"
    ],
    
    "crime_number": [
        r"Crime No\.\s*(\d+/\d{4})",
        r"FIR No\.\s*(\d+/\d{4})",
        r"Criminal Case No\.\s*(\d+/\d{4})"
    ],
    
    "order_date": [
        r"(THURSDAY|FRIDAY|MONDAY|TUESDAY|WEDNESDAY|SATURDAY|SUNDAY),?\s*THE\s+(.*?AUGUST)\s+(TWO THOUSAND[^\n]+)",
        r"(THURSDAY|FRIDAY|MONDAY|TUESDAY|WEDNESDAY|SATURDAY|SUNDAY),?\s*THE\s+(.*?DAY OF \w+)\s+(TWO THOUSAND[^\n]+)",
        r"(THURSDAY|FRIDAY|MONDAY|TUESDAY|WEDNESDAY|SATURDAY|SUNDAY),?\s*THE\s+([^\\n]+?)\s+(TWO THOUSAND[^\\n]+)",
        r"Pronounced on:\s*(\d{2}\.\d{2}\.\d{4})",
        r"Reserved on:\s*(\d{2}\.\d{2}\.\d{4})",
        r"Date of Order\s*[:-]?\s*([\d{1,2}[\.\/-][\d{1,2}][\.\/-]\d{4})",
        r"Order Date\s*[:-]?\s*([\d{1,2}[\.\/-][\d{1,2}][\.\/-]\d{4})",
        r"Judgment\s*[:-]?\s*([\d{1,2}[\.\/-][\d{1,2}][\.\/-]\d{4})",
        r"JUDGMENT\s*[:-]?\s*([\d{1,2}[\.\/-][\d{1,2}][\.\/-]\d{4})",
        r"Decided on\s*[:-]?\s*([\d{1,2}[\.\/-][\d{1,2}][\.\/-]\d{4})",
        r"Date\s*[:-]?\s*([\d{1,2}[\.\/-][\d{1,2}][\.\/-]\d{4})"
    ],
    
    "judge_name": [
        r"THE HONOURABLE SRI JUSTICE ([A-Z\s\.]+?)(?:\n|MOTOR|M\.A\.C|$)",
        r"PRESENT[^\n]*\n[^\n]*(?:HON\'BLE\s*)?(?:MR\.|MS\.|MRS\.)?\s*JUSTICE\s+([^\n]+)",
        r"(?:HON\'BLE|HONOURABLE)\s*(?:MR\.|MS\.|MRS\.|SRI)?\s*JUSTICE\s+([^\n,]+)",
        r"JUSTICE\s+([A-Z][A-Z\s\.]+?)(?:\n|$|,)",
        r"\(Presided over by[^)]*([^)]+)\)",
        r"BEFORE\s+(?:HON\'BLE\s*)?(?:MR\.|MS\.|MRS\.)?\s*JUSTICE\s+([^\n]+)",
        r"CORAM[^\n]*\n[^\n]*(?:HON\'BLE\s*)?JUSTICE\s+([^\n]+)",
        r"Hon\'ble\s+(?:Mr\.|Ms\.|Mrs\.)?\s*Justice\s+([^\n,]+)"
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
        r"Writ Petition",
        r"MOTOR ACCIDENT CIVIL MISCELLANEOUS APPEAL",
        r"Motor Accident Civil Miscellaneous Appeal",
        r"Writ petition \(civil\) judgment",
        r"Criminal Appeal",
        r"Civil Appeal",
        r"Second Appeal", 
        r"Regular Second Appeal",
        r"Revision Petition",
        r"Motor Accident Claim",
        r"Bail Application",
        r"Interim Application",
        r"Original Suit",
        r"Criminal Petition"
    ],
    
    "statutes_sections": [
        r"Article (\d+) of the Constitution of India",
        r"Article (\d+) Constitution of India",
        r"Article (\d+) of Constitution of India",
        r"Sections? (\d+(?:\([a-z]\))?(?:\([a-z]+\))?(?:\([A-Z]+\))?) (?:and (\d+) )?(?:of )?(?:the )?([^\n]*?(?:Code|Act)[^\n]*?)(?:\,|\.|$)",
        r"Section (\d+[A-Z]?\(\d+\)) of (?:the )?([^\n]*Act[^\n]*)",
        r"Section (\d+) CPC",
        r"Section (\d+) of ([^\n]+Act[^\n]*)",
        r"([A-Z][a-z\s]+ Act,? \d{4})",
        r"(\w+ Act,? \d{4})",
        r"The ([^\n]+Act[^\n]*\d{4})",
        r"under ([^\n]+Act[^\n]*)"
    ],

    "counsel": [
        {
            "pattern": r"Counsel for the Appellant\(S\):\s*([^\n]+)",
            "for": "Appellant"
        },
        {
            "pattern": r"Counsel for the Respondent\(S\):\s*([^\n]+)",
            "for": "Respondent"
        },
        {
            "pattern": r"\(Through:([^)]+)\)",
            "for": "General Counsel"
        },
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
            "pattern": r"([A-Z][A-Z\s]+),\s*(?:S\/O|W\/O|D\/O)\.?\s*[^,\n]*",
            "type": "individual"
        },
        {
            "pattern": r"([A-Z][A-Z\s]*(?:COMPANY|CORPORATION|LTD|LIMITED|INSURANCE|BANK|PRIVATE LIMITED)[^\n]*)",
            "type": "company"
        },
        {
            "pattern": r"(STATE OF [A-Z\s]+|GOVERNMENT OF [A-Z\s]+|UNION OF INDIA)",
            "type": "government"
        },
        {
            "pattern": r"([A-Z][A-Z\s]*(?:SOCIETY|ASSOCIATION|TRUST|FOUNDATION)[^\n]*)",
            "type": "organization"
        },
        {
            "pattern": r"(M\/S\. [A-Z][^\n]*)",
            "type": "company"
        }
    ]
}
