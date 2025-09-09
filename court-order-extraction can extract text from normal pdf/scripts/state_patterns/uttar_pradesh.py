# Uttar Pradesh High Court (Allahabad High Court) Specific Patterns
# These patterns are optimized for documents from the High Court of Judicature at Allahabad

UTTAR_PRADESH_PATTERNS = {
    "case_number": [
        # Allahabad specific case number formats
        r'(?:CRIMINAL\s+REFERENCE)\s*NO\.?\s*-?\s*(\d+)\s*OF\s*(\d{4})',
        r'(?:BAIL\s+APPLICATION)\s*NO\.?\s*(\d+)\s*OF\s*(\d{4})',
        r'(?:B\.A\.?|BAIL\s+APPL\.?)\s*NO\.?\s*(\d+)\s*OF\s*(\d{4})',
        r'(?:CWP|WRIT\s+PETITION)\s*NO\.?\s*(\d+)\s*OF\s*(\d{4})',
        r'(?:CRIMINAL\s+REVISION)\s*NO\.?\s*(\d+)\s*OF\s*(\d{4})',
        r'(?:CRL\.?\s*REV\.?)\s*NO\.?\s*(\d+)\s*OF\s*(\d{4})',
        r'(?:CRL\.?\s*A\.?|CRIMINAL\s+APPEAL)\s*NO\.?\s*(\d+)\s*OF\s*(\d{4})',
        r'(?:CRL\.?\s*M\.?C\.?)\s*NO\.?\s*(\d+)\s*OF\s*(\d{4})',
        r'(?:HABEAS\s+CORPUS\s+WRIT\s+PETITION)\s*NO\.?\s*(\d+)\s*OF\s*(\d{4})',
        r'Case\s+No\.?\s*:?-?\s*([A-Z0-9\-\/\.\s]+?)(?:\s+of\s+\d{4}|\n|$)',
        r'Case\s*:-\s*([A-Z\s]+NO\.\s*-?\s*\d+\s+of\s+\d{4})'
    ],
    
    "court_name": [
        r'HIGH\s+COURT\s+OF\s+JUDICATURE\s+AT\s+ALLAHABAD',
        r'HIGH\s+COURT\s+OF\s+JUDICATURE\s+AT\s+PRAYAGRAJ',
        r'ALLAHABAD\s+HIGH\s+COURT',
        r'HIGH\s+COURT\s+ALLAHABAD',
        r'IN\s+THE\s+HIGH\s+COURT\s+OF\s+JUDICATURE\s+AT\s+ALLAHABAD',
        r'इलाहाबाद\s+उच्च\s+न्यायालय'
    ],
    
    "order_date": [
        # Allahabad court specific date formats
        r'dated\s+this\s+the\s+(\d{1,2}(?:st|nd|rd|th)?\s+day\s+of\s+\w+,?\s+\d{4})',
        r'(?:friday|monday|tuesday|wednesday|thursday|saturday|sunday),?\s+the\s+(\d{1,2}(?:st|nd|rd|th)?\s+day\s+of\s+\w+,?\s+\d{4})',
        r'(\d{1,2}(?:st|nd|rd|th)?\s+day\s+of\s+\w+,?\s+\d{4})',
        r'(\d{2}\.\d{2}\.\d{4})',
        r'(\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4})',
        r'Date\s+of\s+(?:Decision|Judgment|Order)\s*:\s*(\d{2}\.\d{2}\.\d{4})',
        r'(\d{2}\-\d{2}\-\d{4})',
        r'(\d{1,2}\/\d{1,2}\/\d{4})',
        r'दिनांक\s*(\d{1,2}\/\d{1,2}\/\d{4})'  # Hindi date format
    ],
    
    "judge_name": [
        # Allahabad specific judge name patterns
        r'HON\'BLE\s+(?:MRS\.?\s+|MR\.?\s+)?([A-Z\s\.\,]+?),?\s+J\.',
        r'Hon\'ble\s+(?:Mrs\.?\s+|Mr\.?\s+)?([A-Z\s\.\,]+?),?\s+J\.',
        r'THE\s+HONOURABLE\s+MR\.?\s*JUSTICE\s+([A-Z\s\.\,]+?)(?:\s*\n|$)',
        r'([A-Z\s\.,]+?),?\s+J\.-+',
        r'JUSTICE\s+([A-Z\s\.,]+?)(?:\s*\n|$)',
        r'HON\'BLE\s+MR\.?\s*JUSTICE\s+([A-Z\s\.\,]+?)(?:\s*\n|$)',
        r'CORAM\s*:\s*HON\'BLE\s+(?:MR\.?\s+)?JUSTICE\s+([A-Z\s\.,]+?)(?:\s*J\.|\n)',
        r'Per\s*:\s*([A-Z\s\.,]+?),?\s+J\.',
        r'BEFORE\s*:\s*([A-Z\s\.,]+?),?\s+J\.',
        r'न्यायमूर्ति\s+([A-Z\s\.,]+)'  # Hindi judge title
    ],
    
    "petitioner_name": [
        # UP specific petitioner patterns
        r'PETITIONER[\/]?(?:\(S\))?(?:\/ACCUSED\s+NO\.\d+)?\s*:?\s*([A-Z\s]+?),?\s*AGED',
        r'PETITIONER[\/]?(?:\(S\))?(?:\/ACCUSED\s+NO\.\d+)?\s*:?\s*([A-Z\s]+?)(?:,|\n)',
        r'APPELLANT[\/]?(?:\(S\))?\s*:?\s*([A-Z\s]+?),?\s*(?:AGED|THROUGH|\n)',
        r'याचिकाकर्ता\s*:?\s*([A-Z\s]+?),?'  # Hindi petitioner
    ],
    
    "respondent_name": [
        # UP/Allahabad specific respondent patterns
        r'OPPOSITE\s+PARTY\s*:?\s*-?\s*(STATE\s+OF\s+U\.P\.)',
        r'RESPONDENTS?[\/]?(?:\(S\))?(?:\/COMPLAINANT)?\s*:?\s*\d*\s*\d*\s*(STATE\s+OF\s+UTTAR\s+PRADESH)',
        r'RESPONDENTS?[\/]?(?:\(S\))?(?:\/COMPLAINANT)?\s*:?\s*\d*\s*\d*\s*(STATE\s+OF\s+U\.P\.)',
        r'RESPONDENTS?[\/]?(?:\(S\))?(?:\/COMPLAINANT)?\s*:?\s*\d*\s*\d*\s*([A-Z\s,]+?)(?:,?\s*REPRESENTED|\n)',
        r'\d+\s*\n\s*(STATE\s+OF\s+UTTAR\s+PRADESH)',
        r'उत्तर\s+प्रदेश\s+राज्य',  # Hindi UP state
        r'(?:STATE\s+OF\s+)?U\.P\.',
        r'GOVERNMENT\s+OF\s+UTTAR\s+PRADESH'
    ],
    
    "fir_crime_no": [
        # UP specific FIR and crime number patterns
        r'CRIME\s+NO\.?\s*(\d+\/\d{4})\s+OF\s+([A-Z\s]+?)\s+POLICE\s+STATION',
        r'FIR\s+NO\.?\s*(\d+\/\d{4})',
        r'CASE\s+NO\.?\s*(\d+\/\d{4})',
        r'G\.D\.?\s*NO\.?\s*(\d+)',
        r'अपराध\s+संख्या\s*(\d+\/\d{4})'  # Hindi crime number
    ],
    
    "police_station": [
        # UP police station patterns
        r'OF\s+([A-Z\s]+?)\s+POLICE\s+STATION',
        r'P\.S\.?\s+([A-Z\s]+)',
        r'POLICE\s+STATION\s+([A-Z\s]+)',
        r'थाना\s+([A-Z\s]+)',  # Hindi police station
        r'THANA\s+([A-Z\s]+)'
    ],
    
    "statutes_offences": [
        # UP specific statutes and offense patterns
        r'SECTION\s+(\d+[A-Z]*(?:\([A-Z0-9]+\))?)\s+OF\s+THE\s+([^,\n]+?)(?:,|AND|\.|$)',
        r'UNDER\s+SECTION\s+(\d+[A-Z]*)\s+OF\s+THE\s+([^,\n]+?)',
        r'U/S\s+(\d+[A-Z]*)\s+([^,\n]+?)',
        r'धारा\s+(\d+[A-Z]*)\s+([^,\n]+?)',  # Hindi section
        r'SECTION\s+(\d+[A-Z]*)\s+UTTAR\s+PRADESH\s+([^,\n]+?)',
        r'UP\s+GOONDA\s+ACT',
        r'PREVENTION\s+OF\s+CORRUPTION\s+ACT',
        r'NARCOTIC\s+DRUGS\s+AND\s+PSYCHOTROPIC\s+SUBSTANCES\s+ACT'
    ],
    
    "decision": [
        # UP court specific decision patterns
        r'I\s+DO\s+NOT\s+THINK\s+THIS\s+IS\s+A\s+FIT\s+CASE\s+TO\s+GRANT\s+([^.]+)',
        r'(?:HELD|DECIDED|ORDERED)\s*:?\s*([^.]+?)(?:\.|$)',
        r'IT\s+IS\s+(?:HELD|ORDERED)\s+THAT\s+([^.]+?)',
        r'THE\s+BAIL\s+APPLICATION\s+IS\s+(?:ALLOWED|DISMISSED|REJECTED)',
        r'APPLICATION\s+FOR\s+BAIL\s+IS\s+(?:ALLOWED|DISMISSED|REJECTED)',
        r'निर्णय\s*:?\s*([^.]+?)'  # Hindi decision
    ],
    
    "directions": [
        # Allahabad court specific directions
        r'IN\s+THE\s+EVENT\s+([^.]+?\.)',
        r'THEREFORE,?\s+THE\s+FOLLOWING\s+DIRECTIONS\s+ARE\s+ISSUED\s*:?\s*-?\s*(.*?)(?:\d+\.|\n\n|$)',
        r'ACCORDINGLY,?\s+([^.]+?\.)',
        r'IT\s+IS\s+DIRECTED\s+THAT\s+([^.]+?\.)',
        r'PETITIONER\s+SHALL\s+([^.]+?\.)',
        r'निर्देश\s*:?\s*([^.]+?)'  # Hindi directions
    ],
    
    "disposition": [
        # UP court disposition patterns
        r'THE\s+(BAIL\s+APPLICATION\s+IS\s+DISPOSED\s+OF\s+AS\s+ABOVE)',
        r'(?:PETITION|APPEAL)\s+IS\s+(DISMISSED|ALLOWED|DISPOSED\s+OF)',
        r'(?:PETITION|APPEAL)\s+(STANDS\s+DISPOSED\s+OF)',
        r'APPLICATION\s+(STANDS\s+DISPOSED\s+OF)',
        r'निपटान\s*:?\s*([^.]+?)'  # Hindi disposition
    ],
    
    "advocates": [
        # UP bar advocates patterns
        r'FOR\s+(?:PETITIONER|APPELLANT)\s*:\s*(.*?)(?:\s+FOR\s+RESPONDENT|\n\n)',
        r'FOR\s+RESPONDENT\s*:\s*(.*?)(?:\n\n|$)',
        r'([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*),?\s+ADV\.?',
        r'MR\.\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
        r'MS\.\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
        r'SRI\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
        r'SMT\.\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
        r'वकील\s*:?\s*([A-Z\s]+)'  # Hindi advocate
    ],
    
    "crime_details": [
        # UP specific crime detail patterns
        r'ALLEGATION\s+(?:IS\s+)?THAT\s+([^\.]+?)\.?',
        r'ACCUSED\s+(?:OF|WITH)\s+([^\.]+?)\.?',
        r'CHARGED\s+(?:FOR|WITH)\s+([^\.]+?)\.?',
        r'IT\s+IS\s+ALLEGED\s+THAT\s+([^\.]+?)\.?',
        r'आरोप\s*:?\s*([^\.]+?)\.?'  # Hindi allegation
    ],
    
    "judgment": [
        # Allahabad court judgment patterns
        r'JUDGMENT\s*\n\s*(.*?)(?=\n\s*\d+\.|$)',
        r'J\s+U\s+D\s+G\s+M\s+E\s+N\s+T\s*\n\s*(.*?)(?=\n\s*\d+\.|$)',
        r'O\s+R\s+D\s+E\s+R\s*\n\s*(.*?)(?=\n\s*\d+\.|$)',
        r'ORDER\s*\n\s*(.*?)(?=\n\s*\d+\.|$)',
        r'(?:CONSIDERING|AFTER\s+CONSIDERING)\s+([^.]+?)(?:\.|$)',
        r'न्यायाधीश\s*([^.]+?)(?:\.|$)'  # Hindi judge/judgment
    ],
    
    # UP specific patterns for local laws and regulations
    "up_specific_acts": [
        r'UTTAR\s+PRADESH\s+GANGSTERS\s+AND\s+ANTI\s+SOCIAL\s+ACTIVITIES',
        r'UP\s+GOONDA\s+ACT',
        r'UTTAR\s+PRADESH\s+CONTROL\s+OF\s+GOONDAS\s+ACT',
        r'UTTAR\s+PRADESH\s+PUBLIC\s+PREMISES',
        r'UTTAR\s+PRADESH\s+ZAMINDARI\s+ABOLITION',
        r'UP\s+LAND\s+REVENUE\s+ACT'
    ],
    
    # Common Hindi terms used in UP courts
    "hindi_terms": [
        r'याचिकाकर्ता',  # Petitioner
        r'प्रतिवादी',     # Respondent  
        r'न्यायमूर्ति',    # Justice
        r'उच्च\s+न्यायालय', # High Court
        r'आदेश',        # Order
        r'निर्णय',       # Decision
        r'अपील',        # Appeal
        r'जमानत',       # Bail
        r'थाना',        # Police Station
        r'अपराध\s+संख्या', # Crime Number
        r'धारा',        # Section
        r'कानून',       # Law
        r'वकील',        # Advocate
        r'न्यायालय',     # Court
        r'मुकदमा'       # Case
    ]
}

# UP specific party classification
UP_PARTY_PATTERNS = {
    "up_government": [
        r'STATE\s+OF\s+UTTAR\s+PRADESH',
        r'STATE\s+OF\s+U\.P\.',
        r'GOVERNMENT\s+OF\s+UTTAR\s+PRADESH',
        r'UTTAR\s+PRADESH\s+GOVERNMENT',
        r'उत्तर\s+प्रदेश\s+राज्य',
        r'UP\s+GOVERNMENT',
        r'COLLECTOR\s+[A-Z\s]+\s+UTTAR\s+PRADESH',
        r'SUPERINTENDENT\s+OF\s+POLICE\s+[A-Z\s]+\s+UP'
    ],
    "up_departments": [
        r'UTTAR\s+PRADESH\s+POLICE',
        r'UP\s+POLICE',
        r'UTTAR\s+PRADESH\s+HOUSING\s+BOARD',
        r'UP\s+HOUSING\s+BOARD',
        r'UTTAR\s+PRADESH\s+ELECTRICITY\s+BOARD',
        r'UPPCB',  # UP Pollution Control Board
        r'UPPWD',  # UP Public Works Department
        r'UPSRTC', # UP State Road Transport Corporation
        r'UPSIDC'  # UP State Industrial Development Corporation
    ]
}

# Export all patterns
__all__ = ['UTTAR_PRADESH_PATTERNS', 'UP_PARTY_PATTERNS']
