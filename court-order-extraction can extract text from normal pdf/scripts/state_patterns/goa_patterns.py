# Regex patterns for GOA courts

PATTERNS = {
    "court_name": [
        r"IN THE HIGH COURT OF ([^\n]+)",
        r"HIGH COURT OF ([^\n]+)",
        r"([^\n]*HIGH COURT[^\n]*)",
        r"SUPREME COURT OF INDIA",
        r"IN THE COURT OF ([^\n]+)"
    ],
    
    "case_number": [
        r"^WRIT PETITION NO\.\s*(\d+\s+OF\s+\d{4})",
        r"APPEAL NO\.\s*(\d+\s+OF\s+\d{4})",
        r"FIRST APPEAL NO\.(\d+\s+OF\s+\d{4})",
        r"WRIT PETITION NO\.(\d+/\d{4})",
        r"WRIT PETITION NO\.\s*(\d+\s+OF\s+\d{4})",
        r"(?:WRIT PETITION|W\.P\.|WP|CRIMINAL PETITION|CIVIL APPEAL|SECOND APPEAL|MOTOR ACCIDENT|FIRST APPEAL|APPEAL)\s*(?:NO\.?|Number)?\s*:?\s*(\d+\s*(?:of|OF)\s*\d{4})",
        r"Case\s*No\.?\s*([\d\/]+)",
        r"([A-Z][A-Z\.\s]*\d+\s*[\d\/]*\s*(?:of|OF)\s*\d{4})"
    ],
    
    "alternate_case_number": [
        r"NOTICE OF MOTION NO\.\s*(\d+\s+OF\s+\d{4})",
        r"Motor Accident Claims Tribunal.*Case No\.?\s*(\d+\s*(?:of|OF)\s*\d{4})",
        r"Regular Civil Suit No\.(\d+\s+of\s+\d{4})",
        r"(?:Civil Suit|Regular Civil Suit)\s*No\.?\s*(\d+\s*(?:of|OF)\s*\d{4})",
        r"(?:Criminal Case|Criminal Appeal|Civil Appeal)\s*No\.?\s*(\d+\s*(?:of|OF)\s*\d{4})",
        r"MACT.*No\.?\s*(\d+\s*(?:of|OF)\s*\d{4})",
        r"Tribunal.*Case.*No\.?\s*(\d+\s*(?:of|OF)\s*\d{4})"
    ],
    
    "order_date": [
        r"PRONOUNCED ON\s*:\s*(\d{1,2}th [A-Z]+, \d{4})",
        r"The date on which the Judgment is pronounced\s*:\s*(\d{1,2}TH [A-Z]+ \d{4})",
        r"Judgment Pron\. on\s*:\s*(\d{1,2} [A-Z]+ \d{4})",
        r"PRONOUNCED ON\s*:\s*([A-Z]+ \d{1,2}, \d{4})",
        r"DATE OF PRONOUNCING THE JUDGMENT\s*:\s*(\d{2}/\d{2}/\d{4})",
        r"DATE OF RESERVING THE JUDGMENT\s*:\s*(\d{2}/\d{2}/\d{4})",
        r"(?:FRIDAY|MONDAY|TUESDAY|WEDNESDAY|THURSDAY|SATURDAY|SUNDAY),?\s*THE\s*([^\n]+TWO THOUSAND[^\n]+)",
        r"(?:Order Date|Date of Order|Judgment|JUDGMENT)\s*[:-]?\s*([\d{1,2}[\.\/\-][\d{1,2}][\.\/\-]\d{4})",
        r"([\d{1,2}[\.\/\-][\d{1,2}][\.\/\-]\d{4})",
        r"Decided on\s*[:-]?\s*([\d{1,2}[\.\/\-][\d{1,2}][\.\/\-]\d{4})"
    ],
    
    "judge_name": [
        r"CORAM\s*\n:\s*(RAVINDRA V\. GHUGE,\s*\n\s*SANDEEP V\. MARNE &\s*\n\s*M\.M\. SATHAYE, JJ\.)",
        r"CORAM:\s*\n(ALOK ARADHE, CJ\.,\s*\n\s*M\. S\. KARNIK &\s*\n\s*SHYAM C\. CHANDAK, JJ\.)",
        r"CORAM\s*:\s*(A\.S\.\s*CHANDURKAR,\s*\nMANISH PITALE\s*&\s*\nSANDEEP V\. MARNE,\s*JJ\.)",
        r":\s*(REVATI MOHITE DERE,\s*\nAMIT BORKAR,\s*&\s*\nGAURI GODSE,\s*JJ\.)",
        r"CORAM\s*:\s*([^,\n]+(?:,\s*[^,\n]+)*)",
        r"PRESENT[^\n]*\n[^\n]*JUSTICE\s+([^\n]+)",
        r"(?:HON\'BLE|HONOURABLE)\s*(?:MR\.|MS\.|MRS\.)?\s*JUSTICE\s+([^\n]+)",
        r"\(Presided over by[^)]*([^)]+)\)",
        r"BEFORE\s+([^\n]+JUSTICE[^\n]+)",
        r"CORAM[^\n]*\n[^\n]*JUSTICE\s+([^\n]+)"
    ],
    
    "document_type": [
        r"JUDGMENT\s*:\s*\[PER[^\]]*\]",
        r"^Judgment$",
        r"JUDGMENT",
        r"Judgment",
        r"ORDER",
        r"Order"
    ],
    
    "statutes_sections": [
        r"Articles (\d+) and (\d+) of the Constitution",
        r"Article (\d+) of the Constitution",
        r"Section (\d+) of ([^\n]+Act[^\n]*)",
        r"(\w+ Act,? \d{4})",
        r"The ([^\n]+Act[^\n]*\d{4})",
        r"under ([^\n]+Act[^\n]*)",
        r"Constitution"
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
