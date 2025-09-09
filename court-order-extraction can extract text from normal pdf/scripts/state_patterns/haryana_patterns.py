# Regex patterns for HARYANA courts

PATTERNS = {
    "court_name": [
        r"I\.L\.R\.\s+PUNJAB\s+AND\s+HARYANA",
        r"HIGH COURT OF PUNJAB AND HARYANA",
        r"IN THE HIGH COURT OF ([^\n]+)",
        r"HIGH COURT OF ([^\n]+)",
        r"([^\n]*HIGH COURT[^\n]*)",
        r"SUPREME COURT OF INDIA",
        r"IN THE COURT OF ([^\n]+)"
    ],
    
    "case_number": [
        r"CRA-S-(\d+-SB-\d{4})",
        r"CRA-S\s+No\.?\s*(\d+-SB\s+of\s+\d{4})",
        r"CRWP\s+No\.?\s*(\d+\s+of\s+\d{4})",
        r"CR\s+No\.?\s*(\d+\s+of\s+\d{4})",
        r"CRM-M\s+No\.?\s*(\d+\s+of\s+\d{4})",
        r"FAO-CARB\s+No\.?\s*(\d+\s+of\s+\d{4})",
        r"CWP\s+no\.?\s*(\d+\s+of\s+\d{4})",
        r"(?:WRIT PETITION|W\.P\.|WP|CRIMINAL PETITION|CIVIL APPEAL|SECOND APPEAL|MOTOR ACCIDENT)\s*(?:NO\.?|Number)?\s*:?\s*([\d\/]+\s*(?:of|OF)\s*\d{4})",
        r"([A-Z\.\s]*\d+\s*(?:of|OF)\s*\d{4})",
        r"Case\s*No\.?\s*([\d\/]+)",
        r"([A-Z][A-Z\.\s]*\d+\s*[\d\/]*\s*(?:of|OF)\s*\d{4})"
    ],
    
    "alternate_case_number": [
        r"FIR\s+No\.?\s*(\d+\s+dated\s+[\d\.]+)",
        r"Sessions\s+Case\s+No\.?\s*(\d+\s+of\s+[\d\.]+)",
        r"FIR\s+No\.?\s*(\d+)",
        r"Civil\s+Appeal\s+No\.?\s*(\d+\s+of\s+\d{4})",
        r"CRWP-(\d+-\d{4})",
        r"CRWP\s+(?:No\.?)?\s*(\d+\s+of\s+\d{4})",
        r"CS\s+No\.?\s*(\d+\s+of\s+\d{4})",
        r"CWP\s+no\.?\s*(\d+\s+of\s+\d{4})",
        r"dismissal\s+of\s+CWP\s+no\.?\s*(\d+\s+of\s+\d{4})",
        r"FAO-CARB\s+No\.?\s*(\d+\s+of\s+\d{4})",
        r"order\s+in\s+(?:CRWP|CWP|CRM-M|CR)\s+(?:No\.?)?\s*(\d+\s+of\s+\d{4})",
        r"vide\s+(?:CRWP|CWP|CRM-M|CR)\s+(?:No\.?)?\s*(\d+\s+of\s+\d{4})",
        r"earlier\s+order.*?(?:CRWP|CWP|CRM-M|CR)\s+(?:No\.?)?\s*(\d+\s+of\s+\d{4})",
        r"(?:arising|connected)\s+with[^\n]*(\d+\s+of\s+\d{4})"
    ],
    
    "order_date": [
        r"(November\s+\d{1,2},\s+\d{4})",
        r"(March\s+\d{1,2},\s+\d{4})",
        r"(May\s+\d{1,2},\s+\d{4})",
        r"(April\s+\d{1,2},\s+\d{4})",
        r"(\d{1,2}\.\d{1,2}\.\d{4})",
        r"(?:FRIDAY|MONDAY|TUESDAY|WEDNESDAY|THURSDAY|SATURDAY|SUNDAY),?\s*THE\s*([^\n]+TWO THOUSAND[^\n]+)",
        r"(?:Order Date|Date of Order|Judgment|JUDGMENT)\s*[:-]?\s*([\d{1,2}[\.\/\-][\d{1,2}][\.\/\-]\d{4})",
        r"([\d{1,2}[\.\/\-][\d{1,2}][\.\/\-]\d{4})",
        r"Decided on\s*[:-]?\s*([\d{1,2}[\.\/\-][\d{1,2}][\.\/\-]\d{4})"
    ],
    
    "judge_name": [
        r"Before\s+(N\.S\.Shekhawat),\s+J",
        r"Before\s+([^,]+)\s+and\s+([^,]+),\s+JJ\.",
        r"Before\s+([^,]+),\s+and\s+([^,]+),\s+JJ\.",
        r"Before\s+([^,]+),\s+J\.",
        r"Before\s+([A-Z][A-Za-z\.\s]+?),\s+J\b",
        r"([A-Z][a-zA-Z\s]+)\s+and\s+([A-Z][a-zA-Z\s]+),\s+JJ\.",
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
    
    "bench": [
        r"Division Bench",
        r"Single Judge",
        r"Full Bench",
        r"Special Bench",
        r"Constitution Bench"
    ],
    
    "parties": [
        {
            "pattern": r"([A-Z][A-Z\s\xa0]+)—Petitioners",
            "type": "individual"
        },
        {
            "pattern": r"([A-Z][A-Z\s\xa0]+)—Respondents",
            "type": "government"
        },
        {
            "pattern": r"(NARESH[\s\xa0]+KUMAR)",
            "type": "individual"
        },
        {
            "pattern": r"(RAMESH[\s\xa0]+KUMAR[\s\xa0]+@[\s\xa0]+RAJ)",
            "type": "individual"
        },
        {
            "pattern": r"(PAWAN[\s\xa0]+KUMAR)",
            "type": "individual"
        },
        {
            "pattern": r"(SHUBHAM[\s\xa0]+ALIAS[\s\xa0]+SHUBHAM[\s\xa0]+SAINI)",
            "type": "individual"
        },
        {
            "pattern": r"(AUNKARI[\s\xa0]+YADAV[\s\xa0]+AND[\s\xa0]+OTHERS)",
            "type": "individual"
        },
        {
            "pattern": r"([A-Z]+(?:[\s\xa0]+[A-Z]+)*[\s\xa0]+@[\s\xa0]+[A-Z]+(?:[\s\xa0]+[A-Z]+)*)",
            "type": "individual"
        },
        {
            "pattern": r"(SURINDER[\s\xa0]+@[\s\xa0]+CHOTI)",
            "type": "individual"
        },
        {
            "pattern": r"(MANURITA)",
            "type": "individual"
        },
        {
            "pattern": r"(ASHOK[\s\xa0]+KUMAR[\s\xa0]+SHARMA)",
            "type": "individual"
        },
        {
            "pattern": r"(RAKESH[\s\xa0]+KUMAR[\s\xa0]+SHARMA[\s\xa0]+AND[\s\xa0]+OTHERS)",
            "type": "individual"
        },
        {
            "pattern": r"(KAMALJEET)",
            "type": "individual"
        },
        {
            "pattern": r"(KRISHAN[\s\xa0]+LAL)",
            "type": "individual"
        },
        {
            "pattern": r"(CHIEF[\s\xa0]+ENGINEER/PROJECTS[\s\xa0]+HARYANA[\s\xa0]+POWER[\s\xa0]+GENERATION[\s\xa0]+CORPORATION[\s\xa0]+LTD\.[\s\xa0]+AND[\s\xa0]+ANOTHER)",
            "type": "company"
        },
        {
            "pattern": r"(M/S[\s\xa0]+TECHNOLOGY[\s\xa0]+PRODUCTS[\s\xa0]+AND[\s\xa0]+ANOTHER)",
            "type": "company"
        },
        {
            "pattern": r"(STATE OF [A-Z\s]+|GOVERNMENT OF [A-Z\s]+|UNION OF INDIA)",
            "type": "government"
        }
    ],
    
    "document_type": [
        r"CRA-S",
        r"Criminal Appeal Special",
        r"CWP",
        r"Civil Writ Petition",
        r"Writ Petition",
        r"CRM-M",
        r"Criminal Miscellaneous",
        r"CR",
        r"Civil Revision",
        r"FAO-CARB",
        r"First Appeal from Order",
        r"Criminal Appeal",
        r"Civil Appeal",
        r"Revision Petition"
    ],
    
    "statutes_sections": [
        r"Article\s+(\d+)\s+of\s+(?:the\s+)?Constitution",
        r"Order\s+(\d+)\s+Rule\s+(\d+[A-Z]*)",
        r"Order\s+(\d+)\s+Rules?\s+(\d+[A-Z]*)\s+to\s+(\d+[A-Z]*)",
        r"Section\s+(\d+)",
        r"Rule\s+(\d+[A-Z]*)",
        r"Code of Civil Procedure",
        r"Constitution of India",
        r"CPC"
    ]
}
