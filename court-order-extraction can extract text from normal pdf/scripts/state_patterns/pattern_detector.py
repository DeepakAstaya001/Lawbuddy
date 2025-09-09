import re
import json
import os
from typing import Dict, List, Any

class PatternDetector:
    """
    Detects state/jurisdiction and provides appropriate regex patterns
    """
    
    def __init__(self):
        self.state_patterns_dir = os.path.join(os.path.dirname(__file__))
        
    def detect_state(self, text: str, pdf_path: str = "") -> str:
        """
        Detect state/jurisdiction from text or file path
        
        Args:
            text: Court judgment text
            pdf_path: Path to PDF file
            
        Returns:
            Detected state name
        """
        # First try to detect from file path
        if pdf_path:
            state_from_path = self._detect_state_from_path(pdf_path)
            if state_from_path:  # Only use path result if it's not None
                return state_from_path
        
        # Then try to detect from text content
        return self._detect_state_from_text(text)
    
    def _detect_state_from_path(self, pdf_path: str) -> str:
        """Detect state from file path"""
        path_upper = pdf_path.upper()
        
        state_mappings = {
            "ANDHRA_PRADESH": "andhra_pradesh",
            "ANDRA_PRADESH": "andhra_pradesh",  # Handle alternate spelling
            "ANDAMAN": "andaman_nicobar",
            "ARUNACHAL": "arunachal_pradesh", 
            "ASSAM": "assam",
            "BIHAR": "bihar",
            "CHANDIGARH": "chandigarh",
            "DADAR": "dadra_nagar_haveli",
            "DELHI": "delhi",
            "GOA": "goa",
            "GUJARAT": "gujarat",
            "HARYANA": "haryana",
            "HIMACHAL": "himachal_pradesh",
            "JAMMU": "jammu_kashmir",
            "JHARKHAND": "jharkhand",
            "KARNATAKA": "karnataka",
            "KERALA": "kerala",
            "MADHYA": "madhya_pradesh",
            "MAHARASHTRA": "maharashtra",
            "MANIPUR": "manipur",
            "MEGHALAYA": "meghalaya",
            "MIZORAM": "mizoram",
            "NAGALAND": "nagaland",
            "ODISHA": "odisha",
            "PUNJAB": "punjab",
            "RAJASTHAN": "rajasthan",
            "SIKKIM": "sikkim",
            "TAMIL": "tamil_nadu",
            "TELANGANA": "telangana",
            "TRIPURA": "tripura",
            "UTTARAKHAND": "uttarakhand",
            "UTTAR": "uttar_pradesh",
            "WEST_BENGAL": "west_bengal",
            "SUPREME": "supreme_court"
        }
        
        for key, state in state_mappings.items():
            if key in path_upper:
                return state
                
        return None  # Return None instead of "default" to allow fallback to text detection
    
    def _detect_state_from_text(self, text: str) -> str:
        """Detect state from text content"""
        text_upper = text.upper()
        
        # Check for specialized tribunals first (they take priority over High Courts)
        tribunal_patterns = {
            "itat": ["INCOME TAX APPELLATE TRIBUNAL", "APPELLATE TRIBUNAL", "INCOME TAX APPELLATE TRI"]
        }
        
        for state, patterns in tribunal_patterns.items():
            for pattern in patterns:
                if pattern in text_upper:
                    return state
        
        # High Court patterns
        high_court_patterns = {
            "delhi": ["HIGH COURT OF DELHI", "DELHI HIGH COURT"],
            "andhra_pradesh": ["HIGH COURT OF ANDHRA PRADESH", "ANDHRA PRADESH HIGH COURT", "HIGH COURT OF ANDHRA PRADESH AT AMARAVATI"],
            "telangana": ["HIGH COURT OF TELANGANA", "TELANGANA HIGH COURT"],
            "arunachal_pradesh": ["HIGH COURT OF ARUNACHAL PRADESH", "ARUNACHAL PRADESH HIGH COURT", "GAUHATI HIGH COURT"],
            "karnataka": ["HIGH COURT OF KARNATAKA", "KARNATAKA HIGH COURT"],
            "tamil_nadu": ["MADRAS HIGH COURT", "HIGH COURT OF MADRAS"],
            "kerala": ["HIGH COURT OF KERALA", "KERALA HIGH COURT"],
            "maharashtra": ["BOMBAY HIGH COURT", "HIGH COURT OF BOMBAY"],
            "gujarat": ["HIGH COURT OF GUJARAT", "GUJARAT HIGH COURT"],
            "rajasthan": ["HIGH COURT OF RAJASTHAN", "RAJASTHAN HIGH COURT"],
            "punjab": ["HIGH COURT OF PUNJAB", "PUNJAB AND HARYANA HIGH COURT"],
            "west_bengal": ["CALCUTTA HIGH COURT", "HIGH COURT OF CALCUTTA"],
            "odisha": ["HIGH COURT OF ORISSA", "ORISSA HIGH COURT"],
            "bihar": ["PATNA HIGH COURT", "HIGH COURT OF JUDICATURE AT PATNA"],
            "supreme_court": ["SUPREME COURT OF INDIA", "SUPREME COURT"]
        }
        
        for state, patterns in high_court_patterns.items():
            for pattern in patterns:
                if pattern in text_upper:
                    return state
        
        # State-level patterns for lower courts (District, Sessions, etc.)
        state_patterns = {
            "arunachal_pradesh": ["ARUNACHAL PRADESH", "LEPARADA DISTRICT", "BASAR"],
            "andhra_pradesh": ["ANDHRA PRADESH"],
            "telangana": ["TELANGANA"],
            "assam": ["ASSAM"],
            "bihar": ["BIHAR"],
            "chandigarh": ["CHANDIGARH"],
            "delhi": ["DELHI"],
            "goa": ["GOA"],
            "gujarat": ["GUJARAT"],
            "haryana": ["HARYANA"],
            "jharkhand": ["JHARKHAND"],
            "karnataka": ["KARNATAKA"],
            "kerala": ["KERALA"],
            "maharashtra": ["MAHARASHTRA"],
            "manipur": ["MANIPUR"],
            "meghalaya": ["MEGHALAYA"],
            "mizoram": ["MIZORAM"],
            "nagaland": ["NAGALAND"],
            "odisha": ["ODISHA", "ORISSA"],
            "punjab": ["PUNJAB"],
            "rajasthan": ["RAJASTHAN"],
            "tamil_nadu": ["TAMIL NADU"],
            "uttarakhand": ["UTTARAKHAND"],
            "uttar_pradesh": ["UTTAR PRADESH"],
            "west_bengal": ["WEST BENGAL"]
        }
        
        for state, patterns in state_patterns.items():
            for pattern in patterns:
                if pattern in text_upper:
                    return state
        
        return "default"
    
    def get_patterns_for_state(self, state: str) -> Dict:
        """
        Get regex patterns for a specific state
        
        Args:
            state: State name
            
        Returns:
            Dictionary of regex patterns
        """
        patterns_file = os.path.join(self.state_patterns_dir, f"{state}_patterns.py")
        
        if os.path.exists(patterns_file):
            return self._load_patterns_from_file(patterns_file)
        else:
            # Create default pattern file if it doesn't exist
            self._create_default_patterns_file(state)
            return self._load_patterns_from_file(patterns_file)
    
    def _load_patterns_from_file(self, patterns_file: str) -> Dict:
        """Load patterns from Python file"""
        try:
            # Read the file and extract patterns
            with open(patterns_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Execute the file content to get patterns
            namespace = {}
            exec(content, namespace)
            return namespace.get('PATTERNS', {})
        except Exception as e:
            print(f"❌ Error loading patterns from {patterns_file}: {e}")
            return self._get_default_patterns()
    
    def _create_default_patterns_file(self, state: str):
        """Create a default patterns file for a state"""
        patterns_file = os.path.join(self.state_patterns_dir, f"{state}_patterns.py")
        
        default_content = f'''# Regex patterns for {state.upper().replace("_", " ")} courts

PATTERNS = {{
    "court_name": [
        r"IN THE HIGH COURT OF ([^\\n]+)",
        r"HIGH COURT OF ([^\\n]+)",
        r"([^\\n]*HIGH COURT[^\\n]*)",
        r"SUPREME COURT OF INDIA",
        r"IN THE COURT OF ([^\\n]+)"
    ],
    
    "case_number": [
        r"(?:WRIT PETITION|W\\.P\\.|WP|CRIMINAL PETITION|CIVIL APPEAL|SECOND APPEAL|MOTOR ACCIDENT)\\s*(?:NO\\.?|Number)?\\s*:?\\s*([\\d\\/]+\\s*(?:of|OF)\\s*\\d{{4}})",
        r"([A-Z\\.\\s]*\\d+\\s*(?:of|OF)\\s*\\d{{4}})",
        r"Case\\s*No\\.?\\s*([\\d\\/]+)",
        r"([A-Z][A-Z\\.\\s]*\\d+\\s*[\\d\\/]*\\s*(?:of|OF)\\s*\\d{{4}})"
    ],
    
    "order_date": [
        r"(?:FRIDAY|MONDAY|TUESDAY|WEDNESDAY|THURSDAY|SATURDAY|SUNDAY),?\\s*THE\\s*([^\\n]+TWO THOUSAND[^\\n]+)",
        r"(?:Order Date|Date of Order|Judgment|JUDGMENT)\\s*[:-]?\\s*([\\d{{1,2}}[\\.\\/\\-][\\d{{1,2}}][\\.\\/\\-]\\d{{4}})",
        r"([\\d{{1,2}}[\\.\\/\\-][\\d{{1,2}}][\\.\\/\\-]\\d{{4}})",
        r"Decided on\\s*[:-]?\\s*([\\d{{1,2}}[\\.\\/\\-][\\d{{1,2}}][\\.\\/\\-]\\d{{4}})"
    ],
    
    "judge_name": [
        r"PRESENT[^\\n]*\\n[^\\n]*JUSTICE\\s+([^\\n]+)",
        r"(?:HON\\'BLE|HONOURABLE)\\s*(?:MR\\.|MS\\.|MRS\\.)?\\s*JUSTICE\\s+([^\\n]+)",
        r"\\(Presided over by[^)]*([^)]+)\\)",
        r"BEFORE\\s+([^\\n]+JUSTICE[^\\n]+)",
        r"CORAM[^\\n]*\\n[^\\n]*JUSTICE\\s+([^\\n]+)"
    ],
    
    "counsel": [
        {{
            "pattern": r"Counsel for (?:the )?(?:Appellant|Petitioner)(?:s)?[^\\n]*[:-]\\s*([^\\n]+)",
            "for": "Appellant/Petitioner"
        }},
        {{
            "pattern": r"Counsel for (?:the )?(?:Respondent|State)(?:s)?[^\\n]*[:-]\\s*([^\\n]+)",
            "for": "Respondent/State"
        }},
        {{
            "pattern": r"For (?:the )?(?:Appellant|Petitioner)(?:s)?[^\\n]*[:-]\\s*([^\\n]+)",
            "for": "Appellant/Petitioner"
        }},
        {{
            "pattern": r"For (?:the )?(?:Respondent|State)(?:s)?[^\\n]*[:-]\\s*([^\\n]+)",
            "for": "Respondent/State"
        }}
    ],
    
    "parties": [
        {{
            "pattern": r"([A-Z][A-Z\\s]+),\\s*(?:S\\/O|W\\/O|D\\/O)\\.?\\s*[^,\\n]*[^\\n]*",
            "type": "individual"
        }},
        {{
            "pattern": r"([A-Z][A-Z\\s]*(?:COMPANY|CORPORATION|LTD|LIMITED|INSURANCE|BANK)[^\\n]*)",
            "type": "company"
        }},
        {{
            "pattern": r"(STATE OF [A-Z\\s]+|GOVERNMENT OF [A-Z\\s]+|UNION OF INDIA)",
            "type": "government"
        }}
    ]
}}
'''
        
        with open(patterns_file, 'w', encoding='utf-8') as f:
            f.write(default_content)
        
        print(f"✅ Created default patterns file: {patterns_file}")
    
    def _get_default_patterns(self) -> Dict:
        """Get basic default patterns"""
        return {
            "court_name": [r"HIGH COURT OF ([^\\n]+)"],
            "case_number": [r"([A-Z\\.\\s]*\\d+\\s*(?:of|OF)\\s*\\d{4})"],
            "order_date": [r"([\\d{1,2}[\\.\\/\\-][\\d{1,2}][\\.\\/\\-]\\d{4})"],
            "judge_name": [r"JUSTICE\\s+([^\\n]+)"],
            "counsel": [],
            "parties": []
        }
    
    def update_patterns_for_state(self, state: str, field: str, new_pattern: str):
        """
        Update patterns for a specific state and field
        
        Args:
            state: State name
            field: Field name (e.g., 'court_name', 'case_number')
            new_pattern: New regex pattern to add
        """
        patterns_file = os.path.join(self.state_patterns_dir, f"{state}_patterns.py")
        
        if os.path.exists(patterns_file):
            # Load existing patterns
            patterns = self._load_patterns_from_file(patterns_file)
            
            # Add new pattern
            if field not in patterns:
                patterns[field] = []
            
            if new_pattern not in patterns[field]:
                patterns[field].append(new_pattern)
                
                # Save updated patterns back to file
                self._save_patterns_to_file(patterns_file, patterns)
                print(f"✅ Added new pattern for {state} - {field}: {new_pattern}")
    
    def _save_patterns_to_file(self, patterns_file: str, patterns: Dict):
        """Save patterns back to file"""
        # This would need to be implemented to properly format and save
        # the patterns back to the Python file
        pass
