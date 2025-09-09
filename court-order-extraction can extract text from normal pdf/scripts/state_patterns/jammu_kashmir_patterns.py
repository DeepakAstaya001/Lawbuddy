# Regex patterns for JAMMU KASHMIR courts

PATTERNS = {
    "court_name": [
        r"IN THE HIGH COURT OF ([^\n]+)",
        r"HIGH COURT OF ([^\n]+)",
        r"([^\n]*HIGH COURT[^\n]*)",
        r"SUPREME COURT OF INDIA",
        r"IN THE COURT OF ([^\n]+)"
    ],
    
    "case_number": [
        r"WP\s+\(C\)\s+No\.?\s*(\d+/\d{4})",
        r"FAO\s+No\.?\s*(\d+/\d{4})",
        r"CR\s+No\.?\s*(\d+/\d{4})", 
        r"WP\(C\)\s+No\.?\s*(\d+/\d{4})",
        r"LPA\s+No\.?\s*(\d+/\d{4})",
        r"HCP\s+No\.?\s*(\d+/\d{4})",
        r"(?:WRIT PETITION|W\.P\.|WP|CRIMINAL PETITION|CIVIL APPEAL|SECOND APPEAL|MOTOR ACCIDENT)\s*(?:NO\.?|Number)?\s*:?\s*([\d\/]+\s*(?:of|OF)\s*\d{4})",
        r"([A-Z\.\s]*\d+\s*(?:of|OF)\s*\d{4})",
        r"Case\s*No\.?\s*([\d\/]+)",
        r"([A-Z][A-Z\.\s]*\d+\s*[\d\/]*\s*(?:of|OF)\s*\d{4})"
    ],
    
    "order_date": [
        r"(?:JAMMU|SRINAGAR)\s+(\d{2}\.\d{2}\.\d{4})",  # For dates after location
        r"(?:ORDER \(ORAL\)|JUDGMENT)\s+(\d{2}\.\d{2}\.\d{4})",  # For dates after ORDER/JUDGMENT  
        r"Pronounced\s+on:\s*(\d{2}\.\d{2}\.\d{4})",
        r"Reserved\s+on\s*:\s*(\d{2}\.\d{2}\.\d{4})",
        r"(?:FRIDAY|MONDAY|TUESDAY|WEDNESDAY|THURSDAY|SATURDAY|SUNDAY),?\s*THE\s*([^\n]+TWO THOUSAND[^\n]+)",
        r"(?:Order Date|Date of Order|Judgment|JUDGMENT)\s*[:-]?\s*([\d{1,2}[\.\/\-][\d{1,2}][\.\/\-]\d{4})",
        r"(\d{2}\.\d{2}\.\d{4})",  # Generic pattern for DD.MM.YYYY
        r"([\d{1,2}[\.\/\-][\d{1,2}][\.\/\-]\d{4})",
        r"Decided on\s*[:-]?\s*([\d{1,2}[\.\/\-][\d{1,2}][\.\/\-]\d{4})"
    ],
    
    "judge_name": [
        # Multi-judge patterns (must come first) - simplest working pattern
        r"HON.BLE\s+MR\.\s+JUSTICE\s+([^,]+),\s+JUDGE\s+\nHON.BLE\s+MR\.\s+JUSTICE\s+([^,]+),\s+JUDGE",
        r"HON.BLE\s+MS\s+JUSTICE\s+([^,]+),\s+JUDGE\s+\nHON.BLE\s+MR\s+JUSTICE\s+([^,]+),\s+JUDGE",
        r"HON.BLE\s+MR\s+JUSTICE\s+([^,]+),\s+JUDGE\s+\nHON.BLE\s+MS\s+JUSTICE\s+([^,]+),\s+JUDGE",
        # Smart quotes versions  
        r"HON['']BLE\s+MS\s+JUSTICE\s+([^,]+),\s+JUDGE\s+\nHON['']BLE\s+MR\s+JUSTICE\s+([^,]+),\s+JUDGE",
        r"HON['']BLE\s+MR\s+JUSTICE\s+([^,]+),\s+JUDGE\s+\nHON['']BLE\s+MS\s+JUSTICE\s+([^,]+),\s+JUDGE",
        # Regular quotes versions
        r"HON'BLE\s+MS\s+JUSTICE\s+([^,]+),\s+JUDGE\s+\nHON'BLE\s+MR\s+JUSTICE\s+([^,]+),\s+JUDGE",
        r"HON'BLE\s+MR\s+JUSTICE\s+([^,]+),\s+JUDGE\s+\nHON'BLE\s+MS\s+JUSTICE\s+([^,]+),\s+JUDGE",
        r"CORAM:\s+\n\s+\n\s+\nHON'BLE\s+MS\s+JUSTICE\s+(MOKSHA\s+KHAJURIA\s+KAZMI),\s+JUDGE\s+\nHON'BLE\s+MR\s+JUSTICE\s+(MOHD\.\s+YOUSUF\s+WANI),\s+JUDGE",
        r"CORAM:\s*\n\s*\n\s*\nHON'BLE\s+MS\s+JUSTICE\s+(MOKSHA\s+KHAJURIA\s+KAZMI),\s+JUDGE\s*\n\s*HON'BLE\s+MR\s+JUSTICE\s+(MOHD\.\s+YOUSUF\s+WANI),\s+JUDGE",
        r"CORAM:\s*\n\s*\n\s*HON'BLE\s+MS\s+JUSTICE\s+(MOKSHA\s+KHAJURIA\s+KAZMI),\s+JUDGE\s*\n\s*HON'BLE\s+MR\s+JUSTICE\s+(MOHD\.\s+YOUSUF\s+WANI),\s+JUDGE",
        r"HON'BLE\s+MS\s+JUSTICE\s+(MOKSHA\s+KHAJURIA\s+KAZMI),\s+JUDGE\s*\n\s*HON'BLE\s+MR\s+JUSTICE\s+(MOHD\.\s+YOUSUF\s+WANI),\s+JUDGE",
        r"HON'BLE\s+MS\s+JUSTICE\s+([^,\n]+),\s+JUDGE\s*\n\s*HON'BLE\s+MR\s+JUSTICE\s+([^,\n]+),\s+JUDGE",
        r"HON'BLE\s+MR\s+JUSTICE\s+([^,\n]+),\s+JUDGE\s*\n\s*HON'BLE\s+MS\s+JUSTICE\s+([^,\n]+),\s+JUDGE",
        r"HON'BLE\s+MS\.\s+JUSTICE\s+([^,\n]+),\s+JUDGE\s*\n\s*HON'BLE\s+MR\.\s+JUSTICE\s+([^,\n]+),\s+JUDGE",
        r"HON'BLE\s+MR\.\s+JUSTICE\s+([^,\n]+),\s+JUDGE\s*\n\s*HON'BLE\s+MS\.\s+JUSTICE\s+([^,\n]+),\s+JUDGE",
        r"HON'BLE\s+MS\.\s+JUSTICE\s+(SINDHU\s+SHARMA),\s+JUDGE\s*.*?HON'BLE\s+MR\.\s+JUSTICE\s+(SHAHZAD\s+AZEEM),\s+JUDGE",
        # Single judge patterns
        r"HON‟BLE\s+MR\.\s+JUSTICE\s+([^,\n]+),\s+JUDGE",
        r"HON'BLE\s+THE\s+CHIEF\s+JUSTICE\s*\n\s*HON'BLE\s+MR\.\s+JUSTICE\s+([^,\n]+),\s+JUDGE",
        r"CORAM:\s+HON'BLE\s+MR\.\s+JUSTICE\s+([^,\n]+),\s+JUDGE",
        r"(SINDHU\s+SHARMA)",
        r"(SHAHZAD\s+AZEEM)",
        r"(M\s+A\s+CHOWDHARY)",
        r"(RAJNESH\s+OSWAL)",
        r"(ARUN\s+PALLI)",
        r"(SANJAY\s+DHAR)",
        r"(MOKSHA\s+KHAJURIA\s+KAZMI)",
        r"(MOHD\.\s+YOUSUF\s+WANI)",
        r"HON'BLE\s+MS\.\s+JUSTICE\s+(SINDHU\s+SHARMA),\s+JUDGE",
        r"HON'BLE\s+MR\.\s+JUSTICE\s+(SHAHZAD\s+AZEEM),\s+JUDGE",
        r"HON'BLE\s+MR\.\s+JUSTICE\s+(M\s+A\s+CHOWDHARY),\s+JUDGE",
        r"HON'BLE\s+MR\.\s+JUSTICE\s+(RAJNESH\s+OSWAL),\s+JUDGE",
        r"HON'BLE\s+MR\.\s+JUSTICE\s+(SANJAY\s+DHAR),\s+JUDGE",
        r"HON'BLE\s+MS\s+JUSTICE\s+(MOKSHA\s+KHAJURIA\s+KAZMI),\s+JUDGE",
        r"HON'BLE\s+MR\s+JUSTICE\s+(MOHD\.\s+YOUSUF\s+WANI),\s+JUDGE",
        r"HON'BLE\s+MS\.\s+JUSTICE\s+([^,]+),\s+JUDGE",
        r"HON'BLE\s+MR\.\s+JUSTICE\s+([^,]+),\s+JUDGE",
        r"HON'BLE\s+MS\s+JUSTICE\s+([^,]+),\s+JUDGE",
        r"HON'BLE\s+MR\s+JUSTICE\s+([^,]+),\s+JUDGE",
        r"PRESENT[^\n]*\n[^\n]*JUSTICE\s+([^\n]+)",
        r"(?:HON\'BLE|HONOURABLE)\s*(?:MR\.|MS\.|MRS\.)?\s*JUSTICE\s+([^\n]+)",
        r"\(Presided over by[^)]*([^)]+)\)",
        r"BEFORE\s+([^\n]+JUSTICE[^\n]+)",
        r"CORAM[^\n]*\n[^\n]*JUSTICE\s+([^\n]+)"
    ],
    
    "bench": [
        r"DIVISION\s+BENCH",
        r"HON'BLE\s+MS\.\s+JUSTICE.*?JUDGE\s*HON'BLE\s+MR\.\s+JUSTICE.*?JUDGE",
        r"HON'BLE\s+MR\.\s+JUSTICE.*?JUDGE\s*HON'BLE\s+MS\.\s+JUSTICE.*?JUDGE",
        r"(?:Chief\s+Justice|CHIEF\s+JUSTICE)",
        r"(?:Single\s+Judge|SINGLE\s+JUDGE)",
        r"(?:Hon\'ble|HONOURABLE)"
    ],
    
    "document_type": [
        r"(WP\s+\(C\))",  # Capture WP (C) as the document type
        r"(WRIT\s+PETITION)",
        r"(CIVIL\s+APPEAL)", 
        r"(CRIMINAL\s+APPEAL)",
        r"(SPECIAL\s+LEAVE\s+PETITION)",
        r"(REVIEW\s+PETITION)",
        r"(CONTEMPT\s+PETITION)",
        r"(LETTERS\s+PATENT\s+APPEAL)",
        r"(FIRST\s+APPEAL\s+FROM\s+ORDER)",
        r"(CIVIL\s+REVISION)",
        r"(HABEAS\s+CORPUS\s+PETITION)",
        r"(ORDER\s+\(ORAL\))",
        r"(JUDGMENT)"
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
        r"Serial\s+No\.?\s*(\d+)",  # For "Serial No. 107"
        r"OA\s+No\.?\s*(\d+/\d{4}\s*\([^)]+\))",  # For "OA No. 1082/2025 (Leh)"
        r"OA\s+No\.?\s*(\d+/\d{4})",  # For "OA No. 1082/2025"
        r"CM\s+no\.?\s*(\d+/\d{4})",
        r"SWP\s+No\.?\s*(\d+/\d{4})",
        r"CR\s+No\.?\s*(\d+/\d{4})",
        r"FAO\s+No\.?\s*(\d+/\d{4})",
        r"CM\s+No\.?\s*(\d+/\d{4})",
        r"WP\s+\(C\)\s+No\.?\s*(\d+/\d{4})",
        r"FIR\s+No\.?\s*(\d+/\d{4})",
        r"FIR\s+No\.?\s*(\d+)",
        r"Case\s+No\.?\s*(\d+/\d{4})",
        r"Criminal\s+Case\s+No\.?\s*(\d+/\d{4})"
    ],
    
    "statutes_sections": [
        r"(\d{4}\s*\(\d+\)\s*SCC\s*\d+)",  # For "2006 (5) SCC 475"
        r"Article[\s\xa0]+(\d+(?:\(\d+\))?[\s\xa0]+of[\s\xa0]+the[\s\xa0]+Constitution[\s\xa0]+of[\s\xa0]+India)",
        r"Article[\s\xa0]+(\d+)",
        r"Section[\s\xa0]+(\d+(?:\(\d+\))?)",
        r"Sections[\s\xa0]+(\d+(?:\s*and\s*\d+)*)",
        r"SO[\s\xa0]+(\d+[\s\xa0]+dated[\s\xa0]+\d{2}\.\d{2}\.\d{4})",
        r"Service[\s\xa0]+Recruitment[\s\xa0]+Rules,[\s\xa0]+(\d{4})",
        r"under[\s\xa0]+Section[\s\xa0]+(\d+(?:\s*read\s*with\s*Sections?\s*\d+(?:\([^\)]+\))?(?:\s*&\s*\d+(?:\([^\)]+\))?)*)?)",
        r"Central[\s\xa0]+Administrative[\s\xa0]+Tribunal",
        r"OA[\s\xa0]+No\.[\s\xa0]+\d+/\d{4}",
        r"Health[\s\xa0]+and[\s\xa0]+Medical[\s\xa0]+\([^)]+\)[\s\xa0]+Service[\s\xa0]+Recruitment[\s\xa0]+Rules"
    ],

    "parties": [
        {
            "pattern": r"(Mohammad[\s\xa0]+Yousuf[\s\xa0]+Mir)",
            "type": "individual"
        },
        {
            "pattern": r"(Union[\s\xa0]+Territory[\s\xa0]+of[\s\xa0]+J&K)",
            "type": "government"
        },
        {
            "pattern": r"(Asif[\s\xa0]+Mehmood)",
            "type": "individual"
        },
        {
            "pattern": r"(UT[\s\xa0]+of[\s\xa0]+Jammu[\s\xa0]+&[\s\xa0]+Kashmir)",
            "type": "government"
        },
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
