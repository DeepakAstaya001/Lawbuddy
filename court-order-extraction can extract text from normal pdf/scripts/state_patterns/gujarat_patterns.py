# Regex patterns for GUJARAT courts

PATTERNS = {
    "court_name": [
        r"IN[\s\xa0]+THE[\s\xa0]+SUPREME[\s\xa0]+COURT[\s\xa0]+OF[\s\xa0]+INDIA",
        r"SUPREME[\s\xa0]+COURT[\s\xa0]+OF[\s\xa0]+INDIA", 
        r"IN THE HIGH COURT OF ([^\n]+)",
        r"HIGH COURT OF ([^\n]+)",
        r"([^\n]*HIGH COURT[^\n]*)",
        r"IN THE COURT OF ([^\n]+)"
    ],
    
    "case_number": [
        r"CIVIL[\s\xa0]+APPEAL[\s\xa0]+NO\.[\s\xa0]*(\d+\/\d{4})",
        r"CRIMINAL[\s\xa0]+APPEAL[\s\xa0]+NO\.[\s\xa0]*(\d+[\s\xa0]+of[\s\xa0]+\d{4})",
        r"CIVIL[\s\xa0]+APPEAL[\s\xa0]+NO\.[\s\xa0]*(\d+[\s\xa0]+of[\s\xa0]+\d{4})",
        r"(?:WRIT PETITION|W\.P\.|WP|CRIMINAL PETITION|CIVIL APPEAL|SECOND APPEAL|MOTOR ACCIDENT)\s*(?:NO\.?|Number)?\s*:?\s*([\d\/]+\s*(?:of|OF)\s*\d{4})",
        r"([A-Z\.\s]*\d+\s*(?:of|OF)\s*\d{4})",
        r"Case\s*No\.?\s*([\d\/]+)",
        r"([A-Z][A-Z\.\s]*\d+\s*[\d\/]*\s*(?:of|OF)\s*\d{4})"
    ],
    
    "order_date": [
        r"Date:\s*(\d{4}\.\d{2}\.\d{2})",
        r"(?:FRIDAY|MONDAY|TUESDAY|WEDNESDAY|THURSDAY|SATURDAY|SUNDAY),?\s*THE\s*([^\n]+TWO THOUSAND[^\n]+)",
        r"(?:Order Date|Date of Order|Judgment|JUDGMENT)\s*[:-]?\s*([\d{1,2}[\.\/\-][\d{1,2}][\.\/\-]\d{4})",
        r"([\d{1,2}[\.\/\-][\d{1,2}][\.\/\-]\d{4})",
        r"Decided on\s*[:-]?\s*([\d{1,2}[\.\/\-][\d{1,2}][\.\/\-]\d{4})"
    ],
    
    "judge_name": [
        r"JUDGMENT[\s\xa0]*\n([A-Z][a-z\s]+),[\s\xa0]*J\.",
        r"J[\xa0\s]*U[\xa0\s]*D[\xa0\s]*G[\xa0\s]*M[\xa0\s]*E[\xa0\s]*N[\xa0\s]*T[\xa0\s]*\n([A-Z][\xa0\s]*[A-Z\s]+),J\.",
        r"J U D G M E N T\s*\n([A-Z\s]+),\s*J\.",
        r"(VIKRAM[\xa0\s]*NATH),[\xa0\s]*J\.",
        r"J U D G M E N T[\s\xa0]*\n([A-Z][A-Z\s]+),\s*J\.",
        r"J U D G M E N T\s+([A-Z\s\.]+),\s*J\.",
        r"J U D G M E N T[\s\xa0\n]+([A-Z][A-Z\s]+),\s*J\.",
        r"([A-Z]\.[\s\xa0]*[A-Z]\.[\s\xa0]*[A-Za-z]+),[\s\xa0]*J\.",
        r"([A-Z][A-Za-z\.\s]+), J\.",
        r"PRESENT[^\n]*\n[^\n]*JUSTICE\s+([^\n]+)",
        r"(?:HON\'BLE|HONOURABLE)\s*(?:MR\.|MS\.|MRS\.)?\s*JUSTICE\s+([^\n]+)",
        r"\(Presided over by[^)]*([^)]+)\)",
        r"BEFORE\s+([^\n]+JUSTICE[^\n]+)",
        r"CORAM[^\n]*\n[^\n]*JUSTICE\s+([^\n]+)"
    ],
    
    "bench": [
        r"Supreme Court Bench",
        r"Division Bench", 
        r"Single Judge",
        r"Full Bench",
        r"Special Bench",
        r"Constitution Bench"
    ],
    
    "alternate_case_number": [
        r"ARISING OUT OF SLP\(C\)[\s\xa0]+NO\.[\s\xa0]*(\d+/\d{4})",
        r"@SLP\s*\([^\)]*\)\s*NOS?\.[\s\xa0]*(\d+[-­]\d+[\s\xa0]+OF[\s\xa0]+\d{4})",
        r"Special Civil Application[\s\xa0]+No\.[\s\xa0]*(\d+/\d{4})",
        r"Letters Patent Appeal No\.[\s\xa0]*(\d+[\s\xa0]+of[\s\xa0]+\d{4})",
        r"Special Civil Application No\.[\s\xa0]*(\d+[\s\xa0]+of[\s\xa0]+\d{4})",
        r"OA[\s\xa0]+No\.?[\s\xa0]*(\d+[\s\xa0]+of[\s\xa0]+\d{4})",
        r"Writ Appeal No\.\s*(\d+\s*of\s*\d{4})",
        r"Criminal Appeal No\.(\d+\s*of\s*\d{4})",
        r"High Court.*?in\s*(?:Criminal Appeal|Appeal|Writ Petition|WP|W\.P\.)\s*No\.?\s*(\d+\s*of\s*\d{4})",
        r"in\s*(?:Criminal Appeal|Appeal|Writ Petition|WP|W\.P\.)\s*No\.?\s*(\d+\s*of\s*\d{4})",
        r"Gujarat.*?(?:Criminal Appeal|Appeal|Writ Petition|WP|W\.P\.)\s*No\.?\s*(\d+\s*of\s*\d{4})",
        r"(?:W\.P\.|WP|Writ Petition|Appeal|Criminal Appeal|Civil Appeal)\s*(?:NO\.?|Number|No\.)\s*(\d+\s*of\s*\d{4})"
    ],
    
    "document_type": [
        r"CRIMINAL[\s\xa0]+APPEAL",
        r"CIVIL[\s\xa0]+APPEAL", 
        r"SPECIAL LEAVE PETITION",
        r"WRIT PETITION",
        r"REVIEW PETITION",
        r"CONTEMPT PETITION",
        r"TRANSFER PETITION"
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
            "pattern": r"(KAHKASHAN[\s\xa0]+KAUSAR[\s\xa0]*@[\s\xa0]*SONAM[\s\xa0]*&[\s\xa0]*ORS\.?)",
            "type": "individual"
        },
        {
            "pattern": r"(STATE[\s\xa0]+OF[\s\xa0]+BIHAR[\s\xa0]*&[\s\xa0]*ORS\.?)",
            "type": "government"
        },
        {
            "pattern": r"(SHAH[\s\xa0]+NEWAZ[\s\xa0]+KHAN[\s\xa0]*&[\s\xa0]*ORS\.?)",
            "type": "individual"
        },
        {
            "pattern": r"(STATE[\s\xa0]+OF[\s\xa0]+NAGALAND[\s\xa0]*&[\s\xa0]*ORS\.?)",
            "type": "government"
        },
        {
            "pattern": r"(CHAUS[\s\xa0]+TAUSHIF[\s\xa0]+ALIMIYA[\s\xa0]+ETC\.?)",
            "type": "individual"
        },
        {
            "pattern": r"(MEMON[\s\xa0]+MAHMMAD[\s\xa0]+UMAR[\s\xa0]+ANWARBHAI[\s\xa0]*&[\s\xa0]*ORS\.?)",
            "type": "individual"
        },
        {
            "pattern": r"(JAYANTIBHAI[\s\xa0]+ISHWARBHAI[\s\xa0]+PATEL)",
            "type": "individual"
        },
        {
            "pattern": r"(H\.[\s\xa0]*B\.[\s\xa0]*KAPADIA[\s\xa0]+EDUCATION[\s\xa0]+TRUST[\s\xa0]*&[\s\xa0]*ANR\.?)",
            "type": "organization"
        },
        {
            "pattern": r"(THE[\s\xa0]+STATE[\s\xa0]+OF[\s\xa0]+GUJARAT[\s\xa0]*&[\s\xa0]*ORS\.?)",
            "type": "government"
        },
        {
            "pattern": r"(Kantha[\s\xa0]+Vibhag[\s\xa0]+Yuva[\s\xa0]+Koli[\s\xa0]+Samaj[\s\xa0]+Parivartan[\s\xa0]*(?:Trust)?[\s\xa0]*(?:and[\s\xa0]+Others)?)",
            "type": "organization"
        },
        {
            "pattern": r"(Sureshkumar[\s\xa0]+Lalitkumar[\s\xa0]+Patel[\s\xa0]*&[\s\xa0]*Ors\.?)",
            "type": "individual"
        },
        {
            "pattern": r"(State[\s\xa0]+of[\s\xa0]+Gujarat[\s\xa0]*&[\s\xa0]*Ors\.?)",
            "type": "government"
        },
        {
            "pattern": r"(State[\s\xa0]+of[\s\xa0]+Gujarat)",
            "type": "government"
        },
        {
            "pattern": r"(Bhalchandra[\s\xa0]+Laxmishankar[\s\xa0]+Dave)",
            "type": "individual"
        }
    ],
    
    "statutes_sections": [
        r"Section[\s\xa0]+166[\s\xa0]+(?:of[\s\xa0]+)?(?:the[\s\xa0]+)?Motor[\s\xa0]+Vehicles[\s\xa0]+Act",
        r"M\.A\.C\.P\.?[\s\xa0]*(?:No\.)?[\s\xa0]*\d+",
        r"Section\s+(\d+(?:\(\d+\))?)",
        r"Sections\s+(\d+(?:\s*and\s*\d+)*)",
        r"Article\s+(\d+(?:\(\d+\))?)",
        r"under\s+Section\s+(\d+(?:\s*read\s*with\s*Sections?\s*\d+(?:\([^\)]+\))?(?:\s*&\s*\d+(?:\([^\)]+\))?)*)?)",
        r"Land Acquisition Act",
        r"Right to Fair Compensation and Transparency in Land Acquisition",
        r"National Green Tribunal Act",
        r"NGT Act",
        r"Prevention of Corruption Act",
        r"Indian Penal Code",
        r"Code of Criminal Procedure",
        r"Evidence Act",
        r"Constitution of India"
    ]
}
