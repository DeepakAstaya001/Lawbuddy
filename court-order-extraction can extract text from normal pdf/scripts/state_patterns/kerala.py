# Kerala High Court Patterns
# Enhanced patterns for Kerala High Court legal document extraction

KERALA_PATTERNS = {
    "case_number": [
        # WP(C) patterns - most common
        r'W\.P\(C\)\s*NO\.?\s*(\d+)\/(\d{2})',  # W.P(C) No.1291/24
        r'WP\(C\)\s*NO\.?\s*(\d+)\s*OF\s*(\d{4})',  # WP(C) NO. 1291 OF 2024
        r'W\.P\(C\)\s*NO\.?\s*(\d+)\s*OF\s*(\d{4})',  # W.P(C) NO. 1291 OF 2024
        
        # Bail Application patterns  
        r'BAIL\s+APPL\.?\s*NO\.?\s*(\d+)\s*OF\s*(\d{4})',  # BAIL APPL. NO. 41 OF 2024
        r'B\.A\.?\s*NO\.?\s*(\d+)\s*OF\s*(\d{4})',  # B.A.No. 41 of 2024
        
        # Criminal Appeal patterns
        r'CRL\.A\s*NO\.?\s*(\d+)\s*OF\s*(\d{4})',  # CRL.A NO. 967 OF 2008
        r'CRL\s+APPEAL\s*NO\.?\s*(\d+)\s*OF\s*(\d{4})',
        
        # Court ID patterns found in documents
        r'(\d{4}/KER/\d+)',  # 2024/KER/7543
        
        # Generic case number patterns
        r'([A-Z\.]+\s*NO\.?\s*\d+\s*OF\s*\d{4})',
        
        # Simple numeric patterns as fallback
        r'NO\.?\s*(\d+)\s*OF\s*(\d{4})',
        r'(\d+)\/(\d{2,4})'
    ],
    
    "order_date": [
        # Full date patterns in judgment headers
        r'dated\s+this\s+the\s+(\d{1,2}(?:st|nd|rd|th)?\s+day\s+of\s+\w+,?\s+\d{4})',
        r'(?:friday|monday|tuesday|wednesday|thursday|saturday|sunday),?\s+the\s+(\d{1,2}(?:st|nd|rd|th)?\s+day\s+of\s+\w+,?\s+\d{4})',
        
        # Simplified day patterns
        r'(\d{1,2}(?:st|nd|rd|th)?\s+day\s+of\s+\w+,?\s+\d{4})',
        
        # DD.MM.YYYY patterns
        r'(\d{2}\.\d{2}\.\d{4})',
        
        # Full month patterns  
        r'(\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4})',
        
        # Court delivery date patterns
        r'delivered\s+(?:the\s+following\s*:?\s*)?(?:on\s+)?(\d{2}\.\d{2}\.\d{4})',
        r'delivered\s+(?:the\s+following\s*:?\s*)?(?:on\s+)?(\d{1,2}(?:st|nd|rd|th)?\s+day\s+of\s+\w+,?\s+\d{4})'
    ],
    
    "judge_name": [
        # Standard justice patterns
        r'the\s+honourable\s+mr\.?\s*justice\s+([A-Z\s\.\,]+?)(?:\s*\n|\s*friday|\s*$)',
        r'THE\s+HONOURABLE\s+MR\.?\s*JUSTICE\s+([A-Z\s\.\,]+?)(?:\s*\n|\s*FRIDAY|\s*$)',
        
        # Judge signatures at end
        r'([A-Z\s\.,]+?),?\s+J\.?\s*-+',
        r'([A-Z\s\.,]+?),?\s+J\.?\s*\.+',
        
        # Simple justice patterns
        r'justice\s+([A-Z\s\.,]+?)(?:\s*\n|$)',
        r'JUSTICE\s+([A-Z\s\.,]+?)(?:\s*\n|$)',
        
        # Hon'ble patterns
        r'hon\'ble\s+mr\.?\s*justice\s+([A-Z\s\.\,]+?)(?:\s*\n|$)',
        
        # Present/Coram patterns
        r'PRESENT\s+THE\s+HONOURABLE\s+MR\.?\s*JUSTICE\s+([A-Z\s\.\,]+?)(?:\s*\n|\s*FRIDAY)',
        r'CORAM\s*:\s*([A-Z\s\.,]+?),?\s+J\.'
    ],
    
    "court_name": [
        # Standard high court patterns
        r'IN\s+THE\s+(HIGH\s+COURT\s+OF\s+KERALA)(?:\s+AT\s+[A-Z\s]+)?',
        r'in\s+the\s+(high\s+court\s+of\s+kerala)(?:\s+at\s+[a-z\s]+)?',
        r'(HIGH\s+COURT\s+OF\s+KERALA)',
        r'(high\s+court\s+of\s+kerala)'
    ],
    
    "petitioner_name": [
        # Enhanced petitioner patterns
        r'PETITIONER[\/S]*(?:\(S\))?(?:\/ACCUSED\s+NO\.\d+)?\s*:?\s*([A-Z][A-Z\s]+?)(?:\s*,\s*AGED|\s*,\s*REP|\s*\n|$)',
        r'petitioner[\/s]*(?:\(s\))?(?:\/accused\s+no\.\d+)?\s*:?\s*([A-Z][A-Za-z\s]+?)(?:\s*,\s*aged|\s*,\s*rep|\s*\n|$)',
        
        # Trust/Institution patterns
        r'PETITIONER[\/S]*(?:\(S\))?\s*:?\s*([A-Z][A-Z\s]+?TRUST)(?:\s*\n|\s*REP)',
        r'PETITIONER[\/S]*(?:\(S\))?\s*:?\s*([A-Z][A-Z\s]+?SCHOOL)(?:\s*\n|\s*REP)',
        r'PETITIONER[\/S]*(?:\(S\))?\s*:?\s*([A-Z][A-Z\s]+?COLLEGE)(?:\s*\n|\s*REP)',
        
        # Individual name patterns
        r'PETITIONER[\/S]*(?:\(S\))?\s*:?\s*([A-Z]+(?:\s+[A-Z]+)*)\s*,\s*AGED',
        r'petitioner[\/s]*(?:\(s\))?\s*:?\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*aged',
        
        # Accused patterns  
        r'ACCUSED\s+NO\.\d+\s*:?\s*([A-Z]+(?:\s+[A-Z]+)*)\s*,',
        r'accused\s+no\.\d+\s*:?\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,'
    ],
    
    "respondent_name": [
        # State patterns
        r'RESPONDENT[S]*(?:\(S\))?(?:\/COMPLAINANT)?\s*:?\s*\d*\s*(STATE\s+OF\s+KERALA)',
        r'respondent[s]*(?:\(s\))?(?:\/complainant)?\s*:?\s*\d*\s*(state\s+of\s+kerala)',
        
        # Union of India patterns
        r'RESPONDENT[S]*(?:\(S\))?\s*:?\s*\d*\s*(UNION\s+OF\s+INDIA)',
        r'respondent[s]*(?:\(s\))?\s*:?\s*\d*\s*(union\s+of\s+india)',
        
        # Officer patterns
        r'RESPONDENT[S]*(?:\(S\))?\s*:?\s*\d*\s*(THE\s+[A-Z\s]+?OFFICER)',
        r'respondent[s]*(?:\(s\))?\s*:?\s*\d*\s*(the\s+[a-z\s]+?officer)',
        
        # Council patterns
        r'RESPONDENT[S]*(?:\(S\))?\s*:?\s*\d*\s*(THE\s+[A-Z\s]+?COUNCIL[A-Z\s]*)',
        r'respondent[s]*(?:\(s\))?\s*:?\s*\d*\s*(the\s+[a-z\s]+?council[a-z\s]*)',
        
        # Enhanced patterns for multiple respondents
        r'RESPONDENTS?\s*:?\s*\d+\s*(THE\s+STATE\s+OF\s+KERALA)',
        r'RESPONDENTS?\s*:?\s*\d+\s*(THE\s+DISTRICT\s+COLLECTOR)',
        r'RESPONDENTS?\s*:?\s*\d+\s*(THE\s+REVENUE\s+DIVISIONAL\s+OFFICER)',
        r'RESPONDENTS?\s*:?\s*\d+\s*(THE\s+TAHSILDAR)',
        r'RESPONDENTS?\s*:?\s*\d+\s*(THE\s+DEPUTY\s+TAHSILDAR)',
        r'RESPONDENTS?\s*:?\s*\d+\s*(THE\s+VILLAGE\s+OFFICER)',
        
        # Generic government entity patterns
        r'\d+\s*\n\s*(THE\s+[A-Z\s]+?)(?:\s+REPRESENTED|\s+BY|\n)',
        r'(\w+\s+GOVERNMENT)',
        r'(GOVERNMENT\s+OF\s+KERALA)'
    ],
    
    "fir_crime_no": [
        # Crime number patterns from bail applications
        r'CRIME\s+NO\.?\s*(\d+\/\d{4})\s*OF\s+([A-Z\s]+?)\s+POLICE\s+STATION',
        r'crime\s+no\.?\s*(\d+\/\d{4})\s*of\s+([a-z\s]+?)\s+police\s+station',
        r'IN\s+CRIME\s+NO\.?\s*(\d+\/\d{4})',
        r'in\s+crime\s+no\.?\s*(\d+\/\d{4})'
    ],
    
    "police_station": [
        # Police station patterns
        r'(\w+(?:\s+\w+)*)\s+POLICE\s+STATION',
        r'(\w+(?:\s+\w+)*)\s+police\s+station',
        r'OF\s+([A-Z\s]+?)\s+POLICE\s+STATION',
        r'of\s+([a-z\s]+?)\s+police\s+station'
    ],
    
    "statutes_offences": [
        # IPC sections
        r'SECTION\s+(\d+[A-Z]*(?:\([A-Z0-9]+\))?)\s+OF\s+THE\s+(INDIAN\s+PENAL\s+CODE)',
        r'section\s+(\d+[a-z]*(?:\([a-z0-9]+\))?)\s+of\s+the\s+(indian\s+penal\s+code)',
        
        # Abkari Act patterns (commonly seen in Kerala)
        r'SECTION\s+(\d+\(\d+\))\s+OF\s+THE\s+(ABKARI\s+ACT)',
        r'section\s+(\d+\(\d+\))\s+of\s+the\s+(abkari\s+act)',
        r'UNDER\s+SECTION\s+(\d+\(\d+\))\s+OF\s+THE\s+(ABKARI\s+ACT)',
        r'under\s+section\s+(\d+\(\d+\))\s+of\s+the\s+(abkari\s+act)',
        
        # Other acts with enhanced patterns
        r'SECTION\s+(\d+[A-Z]*(?:\([A-Z0-9]+\))?)\s+OF\s+THE\s+([A-Z\s]+?ACT[A-Z\s]*)',
        r'section\s+(\d+[a-z]*(?:\([a-z0-9]+\))?)\s+of\s+the\s+([a-z\s]+?act[a-z\s]*)',
        
        # Under section patterns
        r'UNDER\s+SECTION\s+(\d+[A-Z]*)\s+OF\s+THE\s+([A-Z\s]+?)(?:\s+ACT)?',
        r'under\s+section\s+(\d+[a-z]*)\s+of\s+the\s+([a-z\s]+?)(?:\s+act)?',
        
        # Punishable under patterns
        r'PUNISHABLE\s+UNDER\s+SECTION\s+(\d+[A-Z]*)\s+OF\s+THE\s+([A-Z\s]+?)(?:\s+ACT)?',
        r'punishable\s+under\s+section\s+(\d+[a-z]*)\s+of\s+the\s+([a-z\s]+?)(?:\s+act)?',
        
        # Convicted under patterns
        r'CONVICTED\s+UNDER\s+SECTION\s+(\d+[A-Z]*(?:\([A-Z0-9]+\))?)\s+OF\s+THE\s+([A-Z\s]+?)(?:\s+ACT)?',
        r'convicted\s+under\s+section\s+(\d+[a-z]*(?:\([a-z0-9]+\))?)\s+of\s+the\s+([a-z\s]+?)(?:\s+act)?',
        
        # Simple section references
        r'SECTIONS?\s+(\d+[A-Z]*(?:\([A-Z0-9]+\))?(?:\s+AND\s+\d+[A-Z]*(?:\([A-Z0-9]+\))?)*)\s+(?:OF\s+)?(?:THE\s+)?([A-Z\s]+?)(?:\s+ACT)?',
        r'sections?\s+(\d+[a-z]*(?:\([a-z0-9]+\))?(?:\s+and\s+\d+[a-z]*(?:\([a-z0-9]+\))?)*)\s+(?:of\s+)?(?:the\s+)?([a-z\s]+?)(?:\s+act)?',
        
        # Charge patterns
        r'CHARGES?\s+(?:WERE\s+)?FRAMED\s+(?:AGAINST\s+(?:THEM|HIM|HER)\s+)?FOR\s+(?:THE\s+)?OFFENCES?\s+PUNISHABLE\s+UNDER\s+SECTIONS?\s+(\d+[A-Z]*(?:\([A-Z0-9]+\))?)\s+(?:OF\s+)?(?:THE\s+)?([A-Z\s]+?)(?:\s+ACT)?'
    ],
    
    "decision": [
        # Bail decision patterns
        r'I\s+DO\s+NOT\s+THINK\s+THIS\s+IS\s+A\s+FIT\s+CASE\s+TO\s+GRANT\s+([^.]+)',
        r'i\s+do\s+not\s+think\s+this\s+is\s+a\s+fit\s+case\s+to\s+grant\s+([^.]+)',
        
        # General decision patterns
        r'(?:HELD|DECIDED|ORDERED)\s*:?\s*([^.]+?)(?:\.|$)',
        r'(?:held|decided|ordered)\s*:?\s*([^.]+?)(?:\.|$)',
        
        # Writ petition decisions
        r'THE\s+WRIT\s+PETITION\s+IS\s+([^.]+?)(?:\.|$)',
        r'the\s+writ\s+petition\s+is\s+([^.]+?)(?:\.|$)',
        
        # Appeal decisions
        r'THE\s+APPEAL\s+IS\s+([^.]+?)(?:\.|$)',
        r'the\s+appeal\s+is\s+([^.]+?)(?:\.|$)',
        
        # Enhanced Kerala-specific decision patterns
        r'I\s+AM\s+OF\s+THE\s+VIEW\s+THAT\s*,?\s*([^.]+?)(?:\.|$)',
        r'i\s+am\s+of\s+the\s+view\s+that\s*,?\s*([^.]+?)(?:\.|$)',
        r'HAVING\s+HEARD\s+.*?,\s*I\s+AM\s+OF\s+THE\s+VIEW\s+THAT\s*,?\s*([^.]+?)(?:\.|$)',
        r'having\s+heard\s+.*?,\s*i\s+am\s+of\s+the\s+view\s+that\s*,?\s*([^.]+?)(?:\.|$)',
        r'(?:THERE\s+IS\s+CONSIDERABLE\s+MERIT|there\s+is\s+considerable\s+merit)\s+([^.]+?)(?:\.|$)',
        r'(?:THE\s+PETITIONER\s+CANNOT\s+BE\s+ENTITLED|the\s+petitioner\s+cannot\s+be\s+entitled)\s+([^.]+?)(?:\.|$)'
    ],
    
    "directions": [
        # Direction patterns
        r'THEREFORE,?\s+THE\s+FOLLOWING\s+DIRECTIONS\s+ARE\s+ISSUED\s*:?\s*-?\s*(.*?)(?:\d+\.|\n\n|$)',
        r'therefore,?\s+the\s+following\s+directions\s+are\s+issued\s*:?\s*-?\s*(.*?)(?:\d+\.|\n\n|$)',
        
        # Event patterns
        r'IN\s+THE\s+EVENT\s+([^.]+?\.)',
        r'in\s+the\s+event\s+([^.]+?\.)',
        
        # Court directives
        r'THE\s+COURT\s+(?:HEREBY\s+)?DIRECTS?\s+([^.]+?)(?:\.|$)',
        r'the\s+court\s+(?:hereby\s+)?directs?\s+([^.]+?)(?:\.|$)',
        
        # Enhanced Kerala-specific direction patterns
        r'THIS\s+WRIT\s+PETITION\s+WILL\s+STAND\s+DISPOSED\s+OF\s+DIRECTING\s+([^.]+?)(?:\.|$)',
        r'this\s+writ\s+petition\s+will\s+stand\s+disposed\s+of\s+directing\s+([^.]+?)(?:\.|$)',
        r'DIRECTING\s+THE\s+(\d+(?:ST|ND|RD|TH)?\s+RESPONDENT\s+TO\s+[^.]+?)(?:\.|$)',
        r'directing\s+the\s+(\d+(?:st|nd|rd|th)?\s+respondent\s+to\s+[^.]+?)(?:\.|$)',
        r'THE\s+(\d+(?:ST|ND|RD|TH)?\s+RESPONDENT\s+SHALL\s+[^.]+?)(?:\.|$)',
        r'the\s+(\d+(?:st|nd|rd|th)?\s+respondent\s+shall\s+[^.]+?)(?:\.|$)',
        r'WITHIN\s+A\s+PERIOD\s+OF\s+([^.]+?)(?:\.|$)',
        r'within\s+a\s+period\s+of\s+([^.]+?)(?:\.|$)',
        r'TILL\s+SUCH\s+TIME\s*,?\s*([^.]+?)(?:\.|$)',
        r'till\s+such\s+time\s*,?\s*([^.]+?)(?:\.|$)',
        r'STATUS\s+QUO\s+AS\s+ON\s+TODAY\s+SHALL\s+BE\s+MAINTAINED',
        r'status\s+quo\s+as\s+on\s+today\s+shall\s+be\s+maintained'
    ],
    
    "disposition": [
        # Case disposal patterns - enhanced for Kerala specific language
        r'THE\s+(BAIL\s+APPLICATION\s+IS\s+DISPOSED\s+OF\s+AS\s+ABOVE)',
        r'the\s+(bail\s+application\s+is\s+disposed\s+of\s+as\s+above)',
        r'THE\s+(WRIT\s+PETITION\s+IS\s+(?:ALLOWED|DISMISSED|DISPOSED))',
        r'the\s+(writ\s+petition\s+is\s+(?:allowed|dismissed|disposed))',
        r'THE\s+(APPEAL\s+IS\s+(?:ALLOWED|DISMISSED|DISPOSED))',
        r'the\s+(appeal\s+is\s+(?:allowed|dismissed|disposed))',
        
        # Kerala specific disposition patterns
        r'THIS\s+WRIT\s+PETITION\s+WILL\s+STAND\s+DISPOSED\s+OF',
        r'this\s+writ\s+petition\s+will\s+stand\s+disposed\s+of',
        r'(?:THIS\s+)?WRIT\s+PETITION\s+(?:IS\s+)?(?:HEREBY\s+)?(?:STANDS?\s+)?DISMISSED',
        r'(?:this\s+)?writ\s+petition\s+(?:is\s+)?(?:hereby\s+)?(?:stands?\s+)?dismissed',
        r'(?:THIS\s+)?WRIT\s+PETITION\s+(?:IS\s+)?(?:HEREBY\s+)?(?:STANDS?\s+)?ALLOWED',
        r'(?:this\s+)?writ\s+petition\s+(?:is\s+)?(?:hereby\s+)?(?:stands?\s+)?allowed',
        r'(?:THIS\s+)?WRIT\s+PETITION\s+(?:IS\s+)?(?:HEREBY\s+)?(?:STANDS?\s+)?DISPOSED\s+OF',
        r'(?:this\s+)?writ\s+petition\s+(?:is\s+)?(?:hereby\s+)?(?:stands?\s+)?disposed\s+of',
        r'DISPOSES?\s+OF\s+IN\s+THE\s+ABOVE\s+TERMS?',
        r'disposes?\s+of\s+in\s+the\s+above\s+terms?',
        r'WITH\s+THE\s+ABOVE\s+DIRECTIONS?\s*,?\s*THE\s+WRIT\s+PETITION',
        r'with\s+the\s+above\s+directions?\s*,?\s*the\s+writ\s+petition',
        r'(?:IN\s+)?(?:THE\s+)?ABOVE\s+CIRCUMSTANCES?\s*,?\s*THE\s+WRIT\s+PETITION',
        r'(?:in\s+)?(?:the\s+)?above\s+circumstances?\s*,?\s*the\s+writ\s+petition',
        r'ACCORDINGLY\s*,?\s*THE\s+WRIT\s+PETITION',
        r'accordingly\s*,?\s*the\s+writ\s+petition'
    ],
    
    "advocates": [
        # Advocate patterns - enhanced to capture full lists and multiple representations
        r'BY\s+ADVS?\.\s*(.*?)(?=\s+RESPONDENT|\s+THIS\s+(?:WRIT|BAIL|CRIMINAL)|\n\n)',
        r'by\s+advs?\.\s*(.*?)(?=\s+respondent|\s+this\s+(?:writ|bail|criminal)|\n\n)',
        
        # Individual advocate patterns
        r'BY\s+ADV\s+(SRI\.?[A-Z\s\.]+)',
        r'BY\s+ADVS\.\s*(SRI\.?[A-Z][A-Z\s\.]+?)(?:\s*\n|\s*RESPONDENT)',
        r'BY\s+ADVS\.\s*(SRI\.?[A-Z][A-Z\s\.]+?)\s*(?:SRI\.?[A-Z][A-Z\s\.]+?)?',
        
        # Multiple advocates in sequence
        r'SRI\.([A-Z][A-Z\s\.]+?)(?:\s*SRI\.|\s*SMT\.|\s*\n|\s*RESPONDENT)',
        r'SMT\.([A-Z][A-Z\s\.]+?)(?:\s*SRI\.|\s*SMT\.|\s*\n|\s*RESPONDENT)',
        
        # Enhanced Kerala-specific advocate patterns
        r'FOR\s+PETITIONER\s*:\s*ADVS?\.\s+([A-Z][A-Z\s\.&,]+?)(?=\s+FOR|\s+RESPONDENT|\n)',
        r'for\s+petitioner\s*:\s*advs?\.\s+([a-z][a-z\s\.&,]+?)(?=\s+for|\s+respondent|\n)',
        r'FOR\s+RESPONDENTS?\s*:\s*ADVS?\.\s+([A-Z][A-Z\s\.&,]+?)(?=\s+FOR|\s+PETITIONER|\n)',
        r'for\s+respondents?\s*:\s*advs?\.\s+([a-z][a-z\s\.&,]+?)(?=\s+for|\s+petitioner|\n)',
        r'PARTY\s+IN\s+PERSON\s*:\s*([A-Z][A-Z\s\.]+)',
        r'party\s+in\s+person\s*:\s*([a-z][a-z\s\.]+)',
        r'REPRESENTED\s+BY\s+ADVS?\.\s+([A-Z][A-Z\s\.&,]+)',
        r'represented\s+by\s+advs?\.\s+([a-z][a-z\s\.&,]+)',
        r'SRI\.\s*([A-Z][A-Z\s\.]+?)\s*,?\s*ADVOCATE',
        r'sri\.\s*([a-z][a-z\s\.]+?)\s*,?\s*advocate',
        
        # Government pleader patterns
        r'(SRI\.?[A-Z\s\.]+?,?\s+(?:SR\.?\s*GP|SENIOR\s+GOVERNMENT\s+PLEADER))',
        r'(sri\.?[a-z\s\.]+?,?\s+(?:sr\.?\s*gp|senior\s+government\s+pleader))',
        
        # Public prosecutor patterns
        r'BY\s+(PUBLIC\s+PROSECUTOR[A-Z\s]*)',
        r'by\s+(public\s+prosecutor[a-z\s]*)',
        
        # Government Pleader variations
        r'SRI\.\s*([A-Z\s\.]+?)\s*\(GP\)',
        r'SRI\.\s*([A-Z\s\.]+?)\s*\(GOVERNMENT\s+PLEADER\)'
    ],
    
    "crime_details": [
        # Crime description patterns
        r'THE\s+PROSECUTION\s+CASE\s+IS\s+THAT\s+([^.]+?)(?:\.|$)',
        r'the\s+prosecution\s+case\s+is\s+that\s+([^.]+?)(?:\.|$)',
        
        # Allegation patterns
        r'FOR\s+HAVING\s+ALLEGEDLY\s+([^.]+?)(?:\.|$)',
        r'for\s+having\s+allegedly\s+([^.]+?)(?:\.|$)',
        
        # Offense patterns
        r'COMMITTED\s+(?:THE\s+)?OFFENCES?\s+([^.]+?)(?:\.|$)',
        r'committed\s+(?:the\s+)?offences?\s+([^.]+?)(?:\.|$)'
    ],
    
    "judgment": [
        # Judgment section patterns
        r'JUDGMENT\s*\n\s*(.*?)(?=\n\s*\d+\.|$)',
        r'judgment\s*\n\s*(.*?)(?=\n\s*\d+\.|$)',
        
        # Order section patterns  
        r'O\s+R\s+D\s+E\s+R\s*\n\s*(.*?)(?=\n\s*\d+\.|$)',
        r'order\s*\n\s*(.*?)(?=\n\s*\d+\.|$)',
        
        # Reasoning patterns
        r'(?:CONSIDERING|AFTER\s+CONSIDERING)\s+([^.]+?)(?:\.|$)',
        r'(?:considering|after\s+considering)\s+([^.]+?)(?:\.|$)'
    ],
    
    "petitioner_details": {
        "name": [
            r'petitioner[\/]?(?:\(s\))?(?:\/accused\s+no\.\d+)?\s*:?\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*aged',
            r'petitioner[\/]?(?:\(s\))?(?:\/accused\s+no\.\d+)?\s*:?\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*(?:through|by)'
        ],
        "age": [
            r'aged\s+(\d{1,3})\s+years'
        ],
        "relation": [
            r'(s\/o|d\/o|w\/o|h\/o)\s+([a-z\s\.,]+?)(?:,|\n)'
        ],
        "address": {
            "house": [r'([a-z\s]+?\s+house),'],
            "street": [r'([a-z\s]+?)\s+street'],
            "village": [r'([a-z\s]+?)\s+village'],
            "city": [r'([a-z\s]+?)\s+city'],
            "district": [r'([a-z\s]+?)\s+district'],
            "pin": [r'pin\s*[–\-]?\s*(\d{6})'],
            "po": [r'([a-z\s]+?)\s+p\.o']
        },
        "designation": [
            r'petitioner[\/]?(accused\s+no\.\s*\d+)',
            r'[\/]?(accused\s+no\.\s*\d+):',
            r',\s*([a-z\s]+?)(?:\s*,\s*r/o|\s*\n)'
        ]
    },
    
    "respondent_details": {
        "name": [
            r'respondents?[\/]?(?:\(s\))?(?:\/complainant)?\s*:?\s*\d*\s*\d*\s*(STATE\s+OF\s+[A-Z\s]+)',
            r'respondents?[\/]?(?:\(s\))?(?:\/complainant)?\s*:?\s*\d*\s*\d*\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*?)(?:\s+through|\s+represented|\n)',
            r'\d+\s*\n\s*(STATE\s+OF\s+[A-Z\s]+)',
            r'\d+\s*\n\s*(THE\s+[A-Z\s]+?OFFICER)'
        ],
        "address": {
            "district": [r'([a-z\s]+?)\s+district', r'([a-z\s]+?),\s+pin'],
            "pin": [r'pin\s*[–\-]?\s*(\d{6})'],
            "court": [r'(high\s+court\s+of\s+[a-z\s]+)', r'([a-z\s]+\s+court)'],
            "police_station": [r'([a-z\s]+?)\s+police\s+station'],
            "represented_by": [r'represented\s+by\s+([^,\n]+?)(?:,|\n)'],
            "office": [r'(station\s+house\s+officer|public\s+prosecutor)']
        },
        "designation": [
            r'(station\s+house\s+officer)',
            r'represented\s+by\s+(public\s+prosecutor)',
            r'(sr\.?\s*gp|senior\s+government\s+pleader)',
            r'represented\s+by\s+([^,\n]+?)(?:,|\n)'
        ]
    }
}
