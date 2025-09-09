# Regex patterns for DADRA NAGAR HAVELI courts

PATTERNS = {
    "court_name": [
        r"IN THE COURT OF THE\s*([^\n]+MAGISTRATE[^\n]*)",
        r"IN THE HIGH COURT OF ([^\n]+)",
        r"HIGH COURT OF ([^\n]+)",
        r"([^\n]*HIGH COURT[^\n]*)",
        r"SUPREME COURT OF INDIA",
        r"IN THE COURT OF ([^\n]+)"
    ],
    
    "case_number": [
        r"Oth\.\s*Cri\.\s*Misc\s*No\.\s*(\d+\s*of\s*\d{4})",
        r"C\.\s*M\.\s*A\.\s*\([^)]+\)\s*No\.\s*(\d+\s*/\s*\d{4})",
        r"(?:No\.\s*|Number\s*)(\d+\s*/\s*\d{4})",
        r"R\.\s*C\.\s*C\.\s*No\.\s*(\d+\s*/\s*\d{4})",
        r"S\.C\.C\.\s*No\.\s*(\d+\s*/\s*\d{4})",
        r"(?:WRIT PETITION|W\.P\.|WP|CRIMINAL PETITION|CIVIL APPEAL|SECOND APPEAL|MOTOR ACCIDENT)\s*(?:NO\.?|Number)?\s*:?\s*([\d\/]+\s*(?:of|OF)\s*\d{4})",
        r"([A-Z\.\s]*\d+\s*(?:of|OF)\s*\d{4})",
        r"Case\s*No\.?\s*([\d\/]+)",
        r"([A-Z][A-Z\.\s]*\d+\s*[\d\/]*\s*(?:of|OF)\s*\d{4})"
    ],
    
    "order_date": [
        r"Date\s*:\s*(\d{2}\.\d{2}\.\d{4})",
        r"Date\s*:-\s*(\d{2}\/\d{2}\/\d{4})",
        r"Passed on\s*(\d{2}\/\d{2}\/\d{4})",
        r"Decided on\s*[:-]?\s*(\d{2}\/\d{2}\/\d{4})",
        r"Delivered on\s*(\d{2}\/\d{2}\/\d{4})",
        r"(?:FRIDAY|MONDAY|TUESDAY|WEDNESDAY|THURSDAY|SATURDAY|SUNDAY),?\s*THE\s*([^\n]+TWO THOUSAND[^\n]+)",
        r"(?:Order Date|Date of Order|Judgment|JUDGMENT)\s*[:-]?\s*([\d{1,2}[\.\/\-][\d{1,2}][\.\/\-]\d{4})",
        r"([\d{1,2}[\.\/\-][\d{1,2}][\.\/\-]\d{4})"
    ],
    
    "judge_name": [
        r"\(Presided over by ([^)]+)\)",
        r"PRESENT[^\n]*\n[^\n]*JUSTICE\s+([^\n]+)",
        r"(?:HON\'BLE|HONOURABLE)\s*(?:MR\.|MS\.|MRS\.)?\s*JUSTICE\s+([^\n]+)",
        r"BEFORE\s+([^\n]+JUSTICE[^\n]+)",
        r"CORAM[^\n]*\n[^\n]*JUSTICE\s+([^\n]+)",
        r"\(([^)]+)\)\s*\n\s*Sessions Judge",
        r"Sd/-.*?\n.*?\n.*?\(([^)]+)\)\s*\n\s*Sessions Judge",
        r"\(([^)]+)\)\s*\n[^\n]*(?:Sessions Judge|District Judge|Magistrate)"
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
        r"UTDN(\d{12})",
        r"CNR:-([A-Z0-9\-]+)",
        r"([A-Z]{2,}\d+\-\d+\-\d{4})"
    ],
    
    "crime_number": [
        r"C\.R\.\s*No\.\s*(\d+\/\d{4})",
        r"C\.R\.\s*\(FIR\)\s*No\.(\d+\/\d{4})",
        r"FIR\s*/\s*Crime No\.\s*(\d+\s*/\s*\d{4})",
        r"Crime No\.\s*(\d+\s*/\s*\d{4})",
        r"Cr\.\s*No\.\s*(\d+\s*/\s*\d{4})",
        r"F\.I\.R\.\s*[^\n]*vide\s*crime\s*No\.\s*(\d+\/\d{4})",
        r"(?:\(|with).*Crime No\.\s*(\d+\s*/\s*\d{4})"
    ],
    
    "document_type": [
        r"Summary Criminal Case",
        r"S\.C\.C",
        r"Criminal Case",
        r"Civil Case",
        r"JUDGMENT",
        r"Writ Petition",
        r"Criminal Appeal",
        r"Civil Appeal",
        r"C\.M\.A\.\s*\([^)]+\)",
        r"Criminal Miscellaneous Application",
        r"ORDER"
    ],
    
    "parties": [
        {
            "pattern": r"Informant\s*\n\s*([^\n]+(?:\n[^\n]*Through[^\n]*)?)",
            "type": "informant"
        },
        {
            "pattern": r"(?:Accused|ACCUSED)\s*(?:\n\s*\d+\.\s*)?([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s+[A-Z][a-z]+)*)\s*\n\s*Age\s*[:–]\s*(\d+)\s*years?,?\s*\n\s*(?:Occupation[^\n]*)?\s*\n?\s*R\/o\.?\s*([^\n]+)",
            "type": "accused"
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
            "pattern": r"(STATE OF [A-Z\s]+|GOVERNMENT OF [A-Z\s]+|UNION OF INDIA|U\.T\.?\s*of\s*[A-Z\s]+)",
            "type": "government"
        }
    ],
    
    "statutes_sections": [
        r"Section (\d+) of the\s*(Code of Criminal Procedure)",
        r"Section (\d+) of the (Code of Criminal Procedure)",
        r"Section (\d+(?:\(\d+\))?(?:,\s*\d+)*) of (B\.N\.S\.S\.?)",
        r"Sections? (\d+(?:\(\d+\))?(?:,\s*\d+)*) of (B\.N\.S\.?,?\s*\d{4})",
        r"u/s\.?(\d+(?:\s*&\s*\d+)*) of the ([^,\n]+Act,?\s*\d{4})",
        r"u/s\.?(\d+(?:\s*&\s*\d+)*) of ([A-Z\s]+Act)",
        r"(Protection of Children from Sexual Offences Act,?\s*\d{4})",
        r"(B\.N\.S\.?,?\s*\d{4})",
        r"(POCSO Act)",
        r"Section (\d+(?:\(\d+\))?(?:,\s*\d+)*) of ([^,\n]+Act[^,\n]*)",
        r"([A-Z][A-Za-z\s]+Act,?\s*\d{4})"
    ]
}
