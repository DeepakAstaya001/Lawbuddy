# Regex patterns for JHARKHAND courts

PATTERNS = {
    "court_name": [
        r"IN THE (HIGH COURT OF JHARKHAND AT RANCHI)",
        r"(HIGH COURT OF JHARKHAND)",
        r"IN THE (SUPREME COURT OF INDIA)",
        r"(SUPREME COURT OF INDIA)",
        r"IN THE HIGH COURT OF ([^\n]+)",
        r"HIGH COURT OF ([^\n]+)",
        r"([^\n]*HIGH COURT[^\n]*)",
        r"IN THE COURT OF ([^\n]+)"
    ],
    
    "case_number": [
        r"Cr\.\s*Appeal\s*\(DB\)\s*No\.\s*(\d+\s*of\s*\d{4})",  # For "Cr. Appeal (DB) No. 71 of 2020"
        r"Cr\.\s*Appeal\s*\(S\.J\)\s*No\.\s*(\d+\s*of\s*\d{4})",  # For "Cr. Appeal (S.J) No. 1281 of 2016"
        r"CRIMINAL APPEAL NOS?\.\s*([\d\-]+\s*OF\s*\d{4})",  # For "1375-1376 OF 2013"
        r"(?:WRIT PETITION|W\.P\.|WP|CRIMINAL PETITION|CIVIL APPEAL|SECOND APPEAL|MOTOR ACCIDENT)\s*(?:NO\.?|Number)?\s*:?\s*([\d\/]+\s*(?:of|OF)\s*\d{4})",
        r"([A-Z\.\s]*\d+\s*(?:of|OF)\s*\d{4})",
        r"Case\s*No\.?\s*([\d\/]+)",
        r"([A-Z][A-Z\.\s]*\d+\s*[\d\/]*\s*(?:of|OF)\s*\d{4})"
    ],
    
    "order_date": [
        r"Dated:\s*(\d{1,2}\.\d{1,2}\.\d{4})",  # For "Dated: 15.10.2020"
        r"(\d{1,2}(?:st|nd|rd|th)?\s+of\s+\w+,\s+\d{4})",  # For "5th of November, 2020"
        r"Pronounced on:\s*-?\s*(\d{1,2}/\d{1,2}/\d{4})",  # For "Pronounced on: - 19/09/2018"
        r"C\.A\.V\.on:\s*-?\s*(\d{1,2}/\d{1,2}/\d{4})",  # For "C.A.V.on: - 31/08/2018"
        r"(\w+\s+\d{1,2},\s+\d{4})",  # For "April 25, 2018"
        r"New Delhi,\s*(\w+\s+\d{1,2},\s+\d{4})",  # For "New Delhi, April 25, 2018"
        r"(?:FRIDAY|MONDAY|TUESDAY|WEDNESDAY|THURSDAY|SATURDAY|SUNDAY),?\s*THE\s*([^\n]+TWO THOUSAND[^\n]+)",
        r"(?:Order Date|Date of Order|Judgment|JUDGMENT)\s*[:-]?\s*([\d{1,2}[\.\/\-][\d{1,2}][\.\/\-]\d{4})",
        r"([\d{1,2}[\.\/\-][\d{1,2}][\.\/\-]\d{4})",
        r"Decided on\s*[:-]?\s*([\d{1,2}[\.\/\-][\d{1,2}][\.\/\-]\d{4})"
    ],
    
    "judge_name": [
        r"CORAM:.*?(CHIEF JUSTICE).*?JUSTICE\s+(SUJIT NARAYAN PRASAD)",  # For CORAM with both judges - captures both
        r"JUSTICE\s+(SUJIT NARAYAN PRASAD)",  # For PRASAD specifically - simple pattern that works
        r"JUSTICE\s+([A-Z\.\s]+PRASAD)",  # For any PRASAD
        r"JUSTICE ([A-Z\.\s]+MISHRA)[^,\n]*\s*\n[^,\n]*JUSTICE ([A-Z\.\s]+MANGALMURTI)",  # For Jharkhand multi-judge
        r"JUSTICE ([A-Z\.\s]+MISHRA)",  # For single judge MISHRA
        r"JUSTICE ([A-Z\.\s]+MANGALMURTI)",  # For single judge MANGALMURTI
        r"JUSTICE ([A-Z\.\s]+CHOUDHARY)",  # For single judge CHOUDHARY
        r"PRESENT[^\n]*\n[^\n]*JUSTICE\s+([^\n]+)"
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
        r"I\.A\.\s*(?:No\.)?\s*(\d+\s*of\s*\d{4})",  # For "I.A. No. 974 of 2020"
        r"I\.A\.\s*(?:Number)?\s*(\d+/\d{4})",  # For "I.A. Number 974/2020"
        r"Cr\.\s*Appeal\s*\(S\.J\)\s*No\.?(\d+\s*of\s*\d{4})",  # For connected Jharkhand cases
        r"Cr\.\s*M\.\s*P\s*No\.?(\d+\s*of\s*\d{4})",  # For "Cr. M. P No.3260 of 2017"
        r"With\s*\n\s*Cr\.\s*Appeal\s*\(S\.J\)\s*No\.?(\d+\s*of\s*\d{4})",  # For "With Cr. Appeal"
        r"Crl\.A\.\s+No\.\s*(\d+/\d{4})",  # For "Crl.A. No. 1396/2013"
        r"SLP\(Crl\)\s+No\.\s*(\d+/\d{4})",  # For "SLP(Crl) No. 1451/2014"
        r"WITH\s*\n\s*Crl\.A\.\s+No\.\s*(\d+/\d{4})",
        r"Criminal Appeal\s+No\(s\)\.\s*([\d\-]+/\d{4})",
        r"ITEM NO\.(\d+)"  # For "ITEM NO.101"
    ],
    
    "document_type": [
        r"(Cr\.\s*Appeal\s*\(DB\))",  # For "Cr. Appeal (DB)" - Criminal Appeal Division Bench
        r"(CRIMINAL APPEAL)",
        r"(CIVIL APPEAL)",
        r"(WRIT PETITION)",
        r"(SPECIAL LEAVE PETITION)",
        r"O\s+R\s+D\s+E\s+R"  # For "O R D E R" format
    ],
    
    "bench": [
        r"\(DB\)",  # For "(DB)" - Division Bench abbreviation
        r"Cr\.\s*Appeal\s*\(DB\)",  # For "Cr. Appeal (DB)" format indicates Division Bench
        r"(DIVISION BENCH)",
        r"(Division Bench)",
        r"(Single Judge)",
        r"three Judge Bench"  # For "three Judge Bench"
    ],
    
    "statutes_sections": [
        r"judgment of three Judge Bench dated (\d{1,2}(?:st|nd|rd|th)?\s+\w+,?\s+\d{4})",  # For "28th March, 2018"
        r"Section\s+(\d+)",
        r"Article\s+(\d+)",
        r"(\d{4}\.\d{2}\.\d{2})"  # For "2018.04.27" date format
    ],

    "parties": [
        {
            "pattern": r"(ASIAN RESURFACING OF ROAD AGENCY[^\n]*)",
            "type": "company"
        },
        {
            "pattern": r"(CENTRAL BUREAU OF INVESTIGATION)",
            "type": "government"
        },
        {
            "pattern": r"([A-Z][A-Z\s]+),\s*(?:S\/O|W\/O|D\/O)\.?\s*[^,\n]*[^\n]*",
            "type": "individual"
        },
        {
            "pattern": r"([A-Z][A-Z\s]*(?:COMPANY|CORPORATION|LTD|LIMITED|INSURANCE|BANK|AGENCY)[^\n]*)",
            "type": "company"
        },
        {
            "pattern": r"(STATE OF [A-Z\s]+|GOVERNMENT OF [A-Z\s]+|UNION OF INDIA|CENTRAL BUREAU[^\n]*)",
            "type": "government"
        }
    ]
}
