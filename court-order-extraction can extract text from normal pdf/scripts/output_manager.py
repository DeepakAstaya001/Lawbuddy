import os
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

class OutputManager:
    """Centralized output management for all processing phases"""
    
    def __init__(self, base_output_dir: str = "output"):
        self.base_output_dir = base_output_dir
        
    def create_output_folder(self, input_file_path: str) -> str:
        """Create output folder for a specific file"""
        try:
            # Create base output directory if it doesn't exist
            base_dir = Path(self.base_output_dir)
            base_dir.mkdir(exist_ok=True)
            
            # Get the base name without extension
            input_path = Path(input_file_path)
            base_name = input_path.stem
            
            # Create folder name
            folder_name = base_name
            folder_path = base_dir / folder_name
            
            # Handle naming conflicts by adding timestamp
            if folder_path.exists():
                shutil.rmtree(folder_path)
                print(f"🧹 Removed old folder: {folder_path}")
            
            # Create the folder
            folder_path.mkdir(parents=True, exist_ok=True)
            
            print(f"📁 Created output folder: {folder_path}")
            return str(folder_path)
            
        except Exception as e:
            print(f"❌ Error creating folder for {input_file_path}: {e}")
            # Fallback to base output directory
            return self.base_output_dir
    
    def save_ocr_results(self, output_dir: str, full_text: str, raw_full_text: str, summary:str,
                        processing_stats: Optional[Dict] = None) -> Dict[str, str]:
        """Save OCR processing results"""
        saved_files = {}
        
        try:
            # Save full text
            full_text_path = os.path.join(output_dir, "full_text.txt")
            with open(full_text_path, "w", encoding="utf-8") as f:
                f.write(full_text.strip())
            saved_files['full_text'] = full_text_path
            
            # Save raw full text
            raw_full_text_path = os.path.join(output_dir, "raw_full_text.txt")
            with open(raw_full_text_path, "w", encoding="utf-8") as f:
                f.write(raw_full_text.strip())
            saved_files['raw_full_text'] = raw_full_text_path

            # Save summary
            summary_path = os.path.join(output_dir, "summary.txt")
            with open(summary_path, "w", encoding="utf-8") as f:
                f.write(summary.strip())
            saved_files['summary'] = summary_path

            # Save processing stats if provided
            if processing_stats:
                stats_path = os.path.join(output_dir, "processing_stats.json")
                with open(stats_path, "w", encoding="utf-8") as f:
                    json.dump(processing_stats, f, indent=2)
                saved_files['processing_stats'] = stats_path
            
            print(f"✅ OCR results saved to: {output_dir}")
            return saved_files
            
        except Exception as e:
            print(f"❌ Error saving OCR results: {e}")
            return {}
    
    def save_metadata_results(self, output_dir: str, filename_prefix: str, 
                            metadata_results: Dict[str, Any], raw_text: str = None) -> Dict[str, str]:
        """Save metadata extraction results using enhanced professional formatting"""
        saved_files = {}
        
        try:
            # Format output for display in the exact format specified
            text_output = self._format_metadata_output(metadata_results, output_dir)
            text_file = os.path.join(output_dir, "extraction_report.txt")
            with open(text_file, 'w', encoding='utf-8') as f:
                f.write(text_output)
            saved_files['extraction_report'] = text_file
            
            # Use the enhanced professional structured output from metadata_extractor
            # Import the MetaDataExtractor to use its enhanced formatting
            from metadata_extractor import MetaDataExtractor
            temp_extractor = MetaDataExtractor(use_gpu=False, debug=False)
            structured_output = temp_extractor.format_structured_output(metadata_results)
            
            json_file = os.path.join(output_dir, f"{filename_prefix}.json")
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(structured_output, f, indent=2, ensure_ascii=False)
            saved_files['structured_json'] = json_file
            
            # Save raw extracted text if provided
            if raw_text:
                raw_text_file = os.path.join(output_dir, f"{filename_prefix}_original_text.txt")
                with open(raw_text_file, 'w', encoding='utf-8') as f:
                    f.write("=" * 80 + "\n")
                    f.write(f"ORIGINAL TEXT EXTRACTED FROM: {filename_prefix}.pdf\n")
                    f.write("=" * 80 + "\n")
                    f.write(f"Text Length: {len(raw_text)} characters\n")
                    f.write(f"Extraction Timestamp: {datetime.now().isoformat()}\n")
                    f.write("=" * 80 + "\n\n")
                    f.write(raw_text)
                    f.write("\n\n" + "=" * 80 + "\n")
                    f.write("END OF EXTRACTED TEXT\n")
                    f.write("=" * 80 + "\n")
                saved_files['original_text'] = raw_text_file
            
            print(f"✅ Metadata results saved to: {output_dir}")
            print(f"📄 Extraction report: {text_file}")
            print(f"📋 Structured JSON: {json_file}")
            
            return saved_files
            
        except Exception as e:
            print(f"❌ Error saving metadata results: {e}")
            return {}
    
    def _format_metadata_output(self, results: Dict[str, Any]) -> str:
        """Format extraction results in the exact format specified"""
        # Get the structured output for detailed information
        from metadata_extractor import MetaDataExtractor
        temp_extractor = MetaDataExtractor(use_gpu=False, debug=False)
        structured_data = temp_extractor.format_structured_output(results)
        
        output = "🤖 Court Order Extraction Report\n"
        output += "=" * 50 + "\n\n"
        
        # Basic summary
        summary = results['extraction_summary']
        output += f"📊 Summary:\n"
        output += f"   🗺️ Detected State: {results['detected_state']}\n"
        output += f"   📈 Fields Extracted: {summary['extracted_fields']}/{summary['total_fields']}\n"
        output += f"   🎯 Success Rate: {(summary['extracted_fields']/summary['total_fields']*100):.1f}%\n\n"
        
        # Case Information
        output += "📋 Case Information:\n"
        output += "-" * 30 + "\n"
        output += f"   Court: {structured_data.get('court_name', '')}\n"
        output += f"   Case Number: {structured_data.get('case_number', '')}\n"
        if structured_data.get('crime_number'):
            output += f"   Crime Number: {structured_data.get('crime_number', '')}\n"
        output += f"   Order Date: {structured_data.get('order_date', '')}\n"
        output += f"   Judge: {structured_data.get('judge_name', '')}\n"
        output += f"   Document Type: {structured_data.get('document_type', '')}\n\n"
        
        # Parties
        output += "👥 Parties:\n"
        output += "-" * 30 + "\n"
        for party in structured_data.get('parties', []):
            output += f"   {party['role'].title()}: {party['name']}\n"
            if party['party_type'] == 'individual' and party.get('age'):
                output += f"      Age: {party['age']}, {party.get('relations', '')}\n"
                addr = party.get('address', {})
                address_parts = []
                if addr.get('apartment_house'):
                    address_parts.append(addr['apartment_house'].upper())
                if addr.get('village'):
                    address_parts.append(addr['village'])
                if addr.get('district'):
                    address_parts.append(addr['district'].upper())
                if addr.get('state'):
                    address_parts.append(addr['state'])
                if addr.get('zipcode'):
                    address_parts.append(addr['zipcode'])
                output += f"      Address: {', '.join(address_parts)}\n"
                if party.get('counsels'):
                    output += f"      Counsels: {', '.join(party['counsels'][:3])}...\n"
            elif party['party_type'] in ['government', 'police_station']:
                if 'official_designation' in party:
                    output += f"      Designation: {party['official_designation']}\n"
        
    def _format_metadata_output(self, results: Dict[str, Any], output_dir: str = None) -> str:
        """Format extraction results in the exact format specified"""
        # Get the structured output for detailed information
        from metadata_extractor import MetaDataExtractor
        temp_extractor = MetaDataExtractor(use_gpu=False, debug=False)
        structured_data = temp_extractor.format_structured_output(results)
        
        output = "🤖 Court Order Extraction Report\n"
        output += "=" * 50 + "\n\n"
        
        # Basic summary
        summary = results['extraction_summary']
        output += f"📊 Summary:\n"
        output += f"   🗺️ Detected State: {results['detected_state']}\n"
        output += f"   📈 Fields Extracted: {summary['extracted_fields']}/{summary['total_fields']}\n"
        output += f"   🎯 Success Rate: {(summary['extracted_fields']/summary['total_fields']*100):.1f}%\n\n"
        
        # Case Information
        output += "📋 Case Information:\n"
        output += "-" * 30 + "\n"
        output += f"   Court: {structured_data.get('court_name', '')}\n"
        output += f"   Case Number: {structured_data.get('case_number', '')}\n"
        if structured_data.get('crime_number'):
            output += f"   Crime Number: {structured_data.get('crime_number', '')}\n"
        output += f"   Order Date: {structured_data.get('order_date', '')}\n"
        output += f"   Judge: {structured_data.get('judge_name', '')}\n"
        output += f"   Document Type: {structured_data.get('document_type', '')}\n\n"
        
        # Parties
        output += "👥 Parties:\n"
        output += "-" * 30 + "\n"
        for party in structured_data.get('parties', []):
            output += f"   {party['role'].title()}: {party['name']}\n"
            if party['party_type'] == 'individual' and party.get('age'):
                output += f"      Age: {party['age']}, {party.get('relations', '')}\n"
                addr = party.get('address', {})
                address_parts = []
                if addr.get('apartment_house'):
                    address_parts.append(addr['apartment_house'].upper())
                if addr.get('village'):
                    address_parts.append(addr['village'])
                if addr.get('district'):
                    address_parts.append(addr['district'].upper())
                if addr.get('state'):
                    address_parts.append(addr['state'])
                if addr.get('zipcode'):
                    address_parts.append(addr['zipcode'])
                output += f"      Address: {', '.join(address_parts)}\n"
                if party.get('counsels'):
                    output += f"      Counsels: {', '.join(party['counsels'][:3])}...\n"
            elif party['party_type'] in ['government', 'police_station']:
                if 'official_designation' in party:
                    output += f"      Designation: {party['official_designation']}\n"
        
        # Legal Details
        output += "\n⚖️ Legal Details:\n"
        output += "-" * 30 + "\n"
        output += f"   Statutes & Sections:\n"
        for statute in structured_data.get('statutes_sections', []):
            output += f"     • {statute}\n"
        output += f"   Document Type: {structured_data.get('document_type', '')}\n"
        output += f"   Bench: {structured_data.get('bench', '')}\n"
        
        # Add Case Summary from summary.txt if it exists
        if output_dir:
            summary_file = os.path.join(output_dir, 'summary.txt')
            if os.path.exists(summary_file):
                try:
                    with open(summary_file, 'r', encoding='utf-8') as f:
                        summary_content = f.read().strip()
                    if summary_content:
                        output += "\n📄 Case Summary:\n"
                        output += "-" * 30 + "\n"
                        output += summary_content + "\n"
                except Exception as e:
                    print(f"⚠️ Could not read summary file: {e}")
        
        output += "\n" + "=" * 50 + "\n"
        
        return output


# Legacy function for backward compatibility
def create_output_folder(input_file_path, base_output_dir="output"):
    """Legacy function - use OutputManager class instead"""
    manager = OutputManager(base_output_dir)
    return manager.create_output_folder(input_file_path)
