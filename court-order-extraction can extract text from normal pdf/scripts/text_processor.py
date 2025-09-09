import re
import os
import json
import datetime
from pathlib import Path
from typing import Dict, List, Tuple

class LegalTextProcessor:
    """Process and clean extracted OCR text for legal documents"""
    
    def __init__(self):
        self.case_patterns = {
            'case_title': r'(.+?)\s+vs\s+(.+?)\s+on\s+(\d{1,2}\s+\w+,\s+\d{4})',
            'case_number': r'(?:WRIT PETITION|W\.P\.|WP|CIVIL APPLICATION)\s+NO\.?\s*(\d+)\s+OF?\s+(\d{4})',
            'court_name': r'(HIGH COURT|SUPREME COURT|DISTRICT COURT)',
            'judge_name': r'(?:CORAM|BEFORE|J\.|JUSTICE)\s*:?\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            'date_pattern': r'(\d{1,2}[/-]\d{1,2}[/-]\d{4}|\d{1,2}\s+\w+,?\s+\d{4})',
            'respondent': r'(\d+\.)\s*([^}]+?)(?=\d+\.|$)',
            'parties': r'(?:Petitioner|Applicant|Respondent)s?',
            'section_reference': r'Section\s+(\d+(?:\([a-z]\))?)',
            'act_reference': r'([A-Z][a-zA-Z\s]+Act,?\s+\d{4})',
        }
    
    def clean_raw_text(self, raw_text: str) -> str:
        """Clean raw OCR text by removing artifacts and formatting issues"""
        
        # Remove standalone braces and brackets
        text = re.sub(r'^\s*[}\]]\s*$', '', raw_text, flags=re.MULTILINE)
        
        # Remove repeated spaces and newlines
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n\s*\n', '\n', text)
        
        # Fix common OCR errors
        ocr_corrections = {
            r'0F': 'OF',
            r'Parasde': 'Parade',
            r'Downloa': 'Download',
            r'Appollo': 'Apollo',
            r'Kanoon': 'Kanun',
            r'M/s\.': 'M/s',
            r'\.\.': '.',
            r'\s+vs\s+': ' vs ',
            r'\s+on\s+': ' on ',
        }
        
        for pattern, replacement in ocr_corrections.items():
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        # Clean up formatting artifacts
        text = re.sub(r':::\s*', '', text)
        text = re.sub(r'Indian Kanoon.*?doc/\d+/', '', text)
        
        # Remove page numbers and document references
        text = re.sub(r'\d+/\d+\s*$', '', text, flags=re.MULTILINE)
        text = re.sub(r'3-WP-\d+-\d+.*?\.doc', '', text)
        
        return text.strip()
    
    def extract_case_information(self, text: str) -> Dict:
        """Extract structured information from legal text"""
        
        case_info = {
            'case_title': '',
            'case_numbers': [],
            'parties': {
                'petitioners': [],
                'respondents': []
            },
            'dates': [],
            'court': '',
            'judges': [],
            'acts_referenced': [],
            'sections_referenced': [],
            'addresses': [],
            'summary': ''
        }
        
        # Extract case title
        title_match = re.search(self.case_patterns['case_title'], text, re.IGNORECASE)
        if title_match:
            case_info['case_title'] = f"{title_match.group(1).strip()} vs {title_match.group(2).strip()}"
            case_info['dates'].append(title_match.group(3))
        
        # Extract case numbers
        case_numbers = re.findall(self.case_patterns['case_number'], text, re.IGNORECASE)
        for num, year in case_numbers:
            case_info['case_numbers'].append(f"{num}/{year}")
        
        # Extract respondents with addresses
        respondent_pattern = r'(\d+\.)\s*([^}]+?)(?=\d+\.|WITH|IN THE MATTER|$)'
        respondents = re.findall(respondent_pattern, text, re.DOTALL)
        
        for num, details in respondents:
            # Clean the details
            details = re.sub(r'\s+', ' ', details.strip())
            details = re.sub(r'^[}\]]+|[}\]]+$', '', details)
            
            if details:
                case_info['parties']['respondents'].append({
                    'number': num.strip(),
                    'details': details
                })
                
                # Extract addresses
                address_match = re.search(r'(?:office|residing)\s+at\s+([^,]+(?:,[^,]+)*)', details, re.IGNORECASE)
                if address_match:
                    case_info['addresses'].append(address_match.group(1).strip())
        
        # Extract acts referenced
        acts = re.findall(self.case_patterns['act_reference'], text)
        case_info['acts_referenced'] = list(set(acts))
        
        # Extract dates
        dates = re.findall(self.case_patterns['date_pattern'], text)
        case_info['dates'].extend(dates)
        case_info['dates'] = list(set(case_info['dates']))
        
        return case_info
    
    def generate_summary(self, case_info: Dict, original_text: str) -> str:
        """Generate a structured summary of the case"""
        
        summary_parts = []
        
        # Case title and number
        if case_info['case_title']:
            summary_parts.append(f"Case: {case_info['case_title']}")
        
        if case_info['case_numbers']:
            summary_parts.append(f"Case Numbers: {', '.join(case_info['case_numbers'])}")
        
        # Parties involved
        if case_info['parties']['respondents']:
            summary_parts.append("\nParties Involved:")
            for i, respondent in enumerate(case_info['parties']['respondents'], 1):
                summary_parts.append(f"{respondent['number']} {respondent['details']}")
        
        # Key dates
        if case_info['dates']:
            summary_parts.append(f"\nKey Dates: {', '.join(case_info['dates'])}")
        
        # Legal references
        if case_info['acts_referenced']:
            summary_parts.append(f"\nLegal Acts Referenced: {', '.join(case_info['acts_referenced'])}")
        
        # Addresses
        if case_info['addresses']:
            summary_parts.append(f"\nAddresses: {'; '.join(case_info['addresses'])}")
        
        return '\n'.join(summary_parts)
    
    def process_ocr_file(self, file_path: str) -> Dict:
        """Process an OCR text file and return structured data"""
        
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_text = f.read()
        
        # Clean the text
        cleaned_text = self.clean_raw_text(raw_text)
        
        # Extract structured information
        case_info = self.extract_case_information(cleaned_text)
        
        # Generate summary
        summary = self.generate_summary(case_info, cleaned_text)
        
        return {
            'original_text': raw_text,
            'cleaned_text': cleaned_text,
            'case_info': case_info,
            'summary': summary,
            'processed_date': datetime.datetime.now().isoformat()
        }
    
    def save_processed_data(self, processed_data: Dict, output_path: str):
        """Save processed data to files"""
        
        output_dir = Path(output_path).parent
        output_dir.mkdir(exist_ok=True)
        
        base_name = Path(output_path).stem
        
        # Save cleaned text
        with open(output_dir / f"{base_name}_cleaned.txt", 'w', encoding='utf-8') as f:
            f.write(processed_data['cleaned_text'])
        
        # Save summary
        with open(output_dir / f"{base_name}_summary.txt", 'w', encoding='utf-8') as f:
            f.write(processed_data['summary'])
        
        # Save structured data as JSON
        with open(output_dir / f"{base_name}_structured.json", 'w', encoding='utf-8') as f:
            json.dump(processed_data['case_info'], f, indent=2, ensure_ascii=False)
        
        # Save complete processed data
        with open(output_dir / f"{base_name}_complete.json", 'w', encoding='utf-8') as f:
            json.dump(processed_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Processed data saved to: {output_dir}")
        return output_dir

def main():
    """Main function to process OCR text files"""
    
    processor = LegalTextProcessor()
if __name__ == "__main__":
    main()
