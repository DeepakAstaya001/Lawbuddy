# Regex patterns for DELHI courts

PATTERNS = {
    "court_name": [
        r"IN THE HIGH COURT OF DELHI",
        r"HIGH COURT OF DELHI",
        r"DELHI HIGH COURT",
        r"HIGH COURT AT NEW DELHI",
        r"IN THE COURT OF (.+?)(?:NEW DELHI|DELHI)",
        r"DISTRICT COURT[^\n]*DELHI",
        r"SESSIONS COURT[^\n]*DELHI"
    ],
    
    "case_number": [
        r"CS\(COMM\)\s*(\d+/\d{4})",
        r"CS\(OS\)\s*(\d+/\d{4})",
        r"O\.M\.P\.\s*\(COMM\)\s*(\d+/\d{4})",
        r"W\.P\.\(C\)\s*(\d+/\d{4})",
        r"RSA\s+(\d+/\d{4})",
        r"(?:WRIT PETITION|W\.P\.|WP)\s*(?:NO\.?|Number)?\s*:?\s*([\d\/]+\s*(?:of|OF)\s*\d{4})",
        r"(?:CRIMINAL PETITION|Crl\.P\.|CRL\.P\.)\s*(?:NO\.?)?\s*:?\s*([\d\/]+\s*(?:of|OF)\s*\d{4})",
        r"(?:CIVIL APPEAL|C\.A\.|CA)\s*(?:NO\.?)?\s*:?\s*([\d\/]+\s*(?:of|OF)\s*\d{4})",
        r"(?:SECOND APPEAL|SA)\s*(?:NO\.?)?\s*:?\s*([\d\/]+\s*(?:of|OF)\s*\d{4})",
        r"(?:MOTOR ACCIDENT|MAC)\s*(?:NO\.?)?\s*:?\s*([\d\/]+\s*(?:of|OF)\s*\d{4})",
        r"([A-Z][A-Z\.\s]*\d+\s*[\d\/]*\s*(?:of|OF)\s*\d{4})",
        r"Case\s*No\.?\s*([\d\/]+)",
        r"Petition\s*No\.?\s*([\d\/]+)"
    ],
    
    "order_date": [
        r"Date of Decision:\s*(\d{1,2}(?:st|nd|rd|th)?\s*\w+,?\s*\d{4})",
        r"Judgment delivered on:\s*(\d{2}\.\d{2}\.\d{4})",
        r"PRONOUNCED ON\s*[-–]\s*(\d{2}\.\d{2}\.\d{4})",
        r"RESERVED ON\s*[-–]\s*(\d{2}\.\d{2}\.\d{4})",
        r"Reserved on:\s*(\d{1,2}(?:st|nd|rd|th)?\s*\w+,?\s*\d{4})",
        r"Pronounced on:\s*(\d{2}\.\d{2}\.\d{4})",
        r"Reserved on:\s*(\d{2}\.\d{2}\.\d{4})",
        r"(?:FRIDAY|MONDAY|TUESDAY|WEDNESDAY|THURSDAY|SATURDAY|SUNDAY),?\s*THE\s*([^\n]+TWO THOUSAND[^\n]+)",
        r"Date of Order\s*[:-]?\s*([\d{1,2}[\.\/-][\d{1,2}][\.\/-]\d{4})",
        r"Order Date\s*[:-]?\s*([\d{1,2}[\.\/-][\d{1,2}][\.\/-]\d{4})",
        r"Judgment\s*[:-]?\s*([\d{1,2}[\.\/-][\d{1,2}][\.\/-]\d{4})",
        r"JUDGMENT\s*[:-]?\s*([\d{1,2}[\.\/-][\d{1,2}][\.\/-]\d{4})",
        r"Decided on\s*[:-]?\s*([\d{1,2}[\.\/-][\d{1,2}][\.\/-]\d{4})",
        r"Date\s*[:-]?\s*([\d{1,2}[\.\/-][\d{1,2}][\.\/-]\d{4})"
    ],
    
    "judge_name": [
        r"HON'BLE MR\. JUSTICE ([A-Z\s\.]+)",
        r"PRESENT[^\n]*\n[^\n]*(?:HON\'BLE\s*)?(?:MR\.|MS\.|MRS\.)?\s*JUSTICE\s+([^\n]+)",
        r"(?:HON\'BLE|HONOURABLE)\s*(?:MR\.|MS\.|MRS\.)?\s*JUSTICE\s+([^\n,]+)",
        r"JUSTICE\s+([A-Z][A-Z\s\.]+?)(?:\n|$|,)",
        r"\(Presided over by[^)]*([^)]+)\)",
        r"BEFORE\s+(?:HON\'BLE\s*)?(?:MR\.|MS\.|MRS\.)?\s*JUSTICE\s+([^\n]+)",
        r"CORAM[^\n]*\n[^\n]*(?:HON\'BLE\s*)?JUSTICE\s+([^\n]+)",
        r"Hon\'ble\s+(?:Mr\.|Ms\.|Mrs\.)?\s*Justice\s+([^\n,]+)"
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
    
    "bench": [
        r"Division Bench",
        r"Single Judge", 
        r"Full Bench",
        r"Special Bench",
        r"Constitution Bench"
    ],
    
    "document_type": [
        r"JUDGMENT",
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
        r"Order ([XLIV]+)\s*Rules?\s*(\d+(?:\s*and\s*\d+)?)",
        r"Section (\d+) of the Code of Civil Procedure,?\s*(\d{4})",
        r"Section (\d+) of CPC,?\s*(\d{4})",
        r"Section (\d+) of CPC",
        r"Article (\d+)\s*\n.*?of the Constitution of India",
        r"Article (\d+)\s+of the Constitution of India",
        r"Article (\d+) of the Constitution of India",
        r"Article (\d+) Constitution of India",
        r"Sections (\d+/\d+/\d+/\d+) of the Indian Penal Code",
        r"Sections (\d+/\d+/\d+/\d+) of the (\w+)",
        r"Section (\d+\(\d+\)) of the (\w+)",
        r"Section (\d+) of the Code of Criminal",
        r"Section (\d+) of the CrPC",
        r"Section (\d+) of ([^\n]+Act[^\n]*)",
        r"(\w+ Act,? \d{4})",
        r"The ([^\n]+Act[^\n]*\d{4})",
        r"under ([^\n]+Act[^\n]*)",
        r"Indian Penal Code, (\d{4})",
        r"IPC"
    ],

    "counsel": [
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
        },
        {
            "pattern": r"Appearing for (?:the )?(?:Appellant|Petitioner)(?:s)?[^\n]*[:-]\s*([^\n]+)",
            "for": "Appellant/Petitioner"
        },
        {
            "pattern": r"Appearing for (?:the )?(?:Respondent|State)(?:s)?[^\n]*[:-]\s*([^\n]+)",
            "for": "Respondent/State"
        },
        {
            "pattern": r"(?:Mr\.|Ms\.|Shri|Smt\.)\s*([A-Z][^,\n]*),\s*Advocate for (?:the )?(?:Appellant|Petitioner)",
            "for": "Appellant/Petitioner"
        },
        {
            "pattern": r"(?:Mr\.|Ms\.|Shri|Smt\.)\s*([A-Z][^,\n]*),\s*Advocate for (?:the )?(?:Respondent|State)",
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
            "pattern": r"(STATE OF DELHI|GOVERNMENT OF NCT OF DELHI|UNION OF INDIA|GOVT\. OF DELHI)",
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
