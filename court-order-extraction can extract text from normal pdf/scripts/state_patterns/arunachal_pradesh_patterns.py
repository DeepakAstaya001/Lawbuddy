# Regex patterns for ARUNACHAL PRADESH courts

PATTERNS = {
    "court_name": [
        r"THE GAUHATI HIGH COURT",
        r"GAUHATI HIGH COURT",
        r"HIGH COURT OF ASSAM, NAGALAND, MIZORAM AND ARUNACHAL PRADESH",
        r"IN THE HIGH COURT OF ([^\n]+)",
        r"HIGH COURT OF ([^\n]+)",
        r"([^\n]*HIGH COURT[^\n]*)",
        r"SUPREME COURT OF INDIA",
        r"IN THE COURT OF ([^\n]+)"
    ],
    
    "case_number": [
        r"Case No\.\s*:\s*(WP\(C\)\/\d+\/\d{4})",
        r"WP\(C\)\/(\d+\/\d{4})",
        r"Case No\.\s*:\s*([\w\(\)\/\d]+)",
        r"(?:WRIT PETITION|W\.P\.|WP|CRIMINAL PETITION|CIVIL APPEAL|SECOND APPEAL|MOTOR ACCIDENT)\s*(?:NO\.?|Number)?\s*:?\s*([\d\/]+\s*(?:of|OF)\s*\d{4})",
        r"([A-Z\.\s]*\d+\s*(?:of|OF)\s*\d{4})",
        r"Case\s*No\.?\s*([\d\/]+)",
        r"([A-Z][A-Z\.\s]*\d+\s*[\d\/]*\s*(?:of|OF)\s*\d{4})"
    ],
    
    "order_date": [
        r"Date of hearing & judgment\s*:\s*(\d{2}\.\d{2}\.\d{4})",
        r"Date of Judgment\s*:\s*(\d{2}\.\d{2}\.\d{4})",
        r"Date of Order\s*:\s*(\d{2}\.\d{2}\.\d{4})",
        r"(?:FRIDAY|MONDAY|TUESDAY|WEDNESDAY|THURSDAY|SATURDAY|SUNDAY),?\s*THE\s*([^\n]+TWO THOUSAND[^\n]+)",
        r"(?:Order Date|Date of Order|Judgment|JUDGMENT)\s*[:-]?\s*(\d{1,2}[\.\/\-]\d{1,2}[\.\/\-]\d{4})",
        r"(\d{1,2}[\.\/\-]\d{1,2}[\.\/\-]\d{4})",
        r"Decided on\s*[:-]?\s*([\d{1,2}[\.\/\-][\d{1,2}][\.\/\-]\d{4})"
    ],
    
    "judge_name": [
        r"Hon'ble MR\. JUSTICE ([A-Z][A-Z\s]+?)(?:\n|Advocate|$)",
        r"Hon.ble MR\. JUSTICE ([A-Z][A-Z\s]+?)(?:\n|Advocate|$)",
        r"B E F O R E\s*\n\s*Hon'ble MR\. JUSTICE ([A-Z][A-Z\s]+?)(?:\n|Advocate|$)",
        r"HONOURABLE MR\. JUSTICE ([A-Z][A-Z\s]+?)(?:\n|Advocate|$)",
        r"PRESENT[^\n]*\n[^\n]*JUSTICE\s+([^\n]+)",
        r"(?:HON\'BLE|HONOURABLE)\s*(?:MR\.|MS\.|MRS\.)?\s*JUSTICE\s+([^\n,]+)",
        r"\(Presided over by[^)]*([^)]+)\)",
        r"BEFORE\s+([^\n]+JUSTICE[^\n]+)",
        r"CORAM[^\n]*\n[^\n]*JUSTICE\s+([^\n]+)",
        r"Present:\s*([^,\n]+),\s*APJS",  # District court format: Present: Mr. Tage Halley, APJS
        r"Present:\s*([^,\n]+),"  # General present format
    ],
    
    "bench": [
        r"\s*(Addl\. Sessions Judge)",  # Additional Sessions Judge with whitespace
        r"(Sessions Judge)",
        r"(Additional District Judge)",
        r"(District Judge)", 
        r"(Chief Judicial Magistrate)",
        r"(Judicial Magistrate)",
        r"Division Bench",
        r"Single Judge", 
        r"Full Bench",
        r"Special Bench",
        r"Constitution Bench"
    ],
    
    "alternate_case_number": [
        r"SAO No\.\s*(\d+\/\d{4})",
        r"(\d{4}:GAU-AS:\d+)",
        r"(GAHC\d+)",
        r"Misc\. Appeal No\.(\d+\/\d{4})",
        r"Title Suit No\.\s*(\d+\/\d{4})",
        r"Misc\. Case No\.\s*(\d+\/\d{4})",
        r"(?:Criminal Appeal|Civil Appeal|Writ Petition|Review Petition)\s*No\.\s*(\d+\/\d{4})",
        r"(?:W\.P\.|WP|Appeal|Petition)\s*(?:NO\.?|Number|No\.)\s*(\d+\/\d{4})",
        r"(BSR\/ABA No\.\d+\/\d{2})",  # Bail application format: BSR/ABA No.01/23
        r"DMJ PS Case No\.(\d+\/\d{2,4})",  # Police case format: DMJ PS Case No.02/23
        r"(PS Case No\.\d+\/\d{2,4})"  # General police case format
    ],
    
    "document_type": [
        r"Civil Revision Petition",
        r"CRP\(IO\)",
        r"WRIT PETITION",
        r"Writ Petition", 
        r"WP\(C\)",
        r"Criminal Appeal",
        r"Civil Appeal",
        r"Second Appeal", 
        r"Regular Second Appeal",
        r"Revision Petition",
        r"Bail Application",
        r"Interim Application",
        r"Original Suit",
        r"Criminal Petition",
        r"(Order)",  # Simple order format
        r"(J U D G M E N T)",
        r"(JUDGMENT)",
        r"(O R D E R)",
        r"pre-arrest bail application"  # Specific bail application type
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
