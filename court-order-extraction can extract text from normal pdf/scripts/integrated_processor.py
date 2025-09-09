#!/usr/bin/env python3
"""
Integrated Court Order Processing System for Frontend Integration
Combines OCR, Metadata Extraction, and AI Summarization in a single pipeline
"""
import os
import sys
import json
import time
import traceback
from pathlib import Path

# Add the scripts directory to Python path to import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def log_debug(message):
    """Log debug messages to stderr for debugging"""
    print(f"DEBUG: {message}", file=sys.stderr, flush=True)

def safe_import():
    """Safely import all required modules with fallback handling"""
    modules = {}
    
    try:
        from ocr import AdvancedLegalOCR
        modules['ocr'] = AdvancedLegalOCR
        log_debug("✅ OCR module imported successfully")
    except ImportError as e:
        log_debug(f"❌ Failed to import OCR module: {e}")
        modules['ocr'] = None
    
    try:
        from metadata_extractor import MetaDataExtractor
        modules['metadata'] = MetaDataExtractor
        log_debug("✅ Metadata extractor imported successfully")
    except ImportError as e:
        log_debug(f"❌ Failed to import metadata extractor: {e}")
        modules['metadata'] = None
    
    try:
        from output_manager import OutputManager
        modules['output'] = OutputManager
        log_debug("✅ Output manager imported successfully")
    except ImportError as e:
        log_debug(f"❌ Failed to import output manager: {e}")
        modules['output'] = None
    
    try:
        from llama import generate_court_order_summary
        modules['llama_summary'] = generate_court_order_summary
        log_debug("✅ LLaMA summarization imported successfully")
    except ImportError as e:
        log_debug(f"❌ Failed to import LLaMA module: {e}")
        modules['llama_summary'] = None
    
    return modules

def create_output_directory(pdf_path):
    """Create output directory for processing results"""
    try:
        filename_prefix = os.path.splitext(os.path.basename(pdf_path))[0]
        output_base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp_output")
        output_dir = os.path.join(output_base, filename_prefix)
        
        # Remove existing directory if it exists
        if os.path.exists(output_dir):
            import shutil
            shutil.rmtree(output_dir)
        
        os.makedirs(output_dir, exist_ok=True)
        log_debug(f"📁 Created output directory: {output_dir}")
        return output_dir
    except Exception as e:
        log_debug(f"❌ Failed to create output directory: {e}")
        return None

def extract_text_fallback(pdf_path):
    """Fallback text extraction using basic libraries"""
    log_debug("🔄 Using fallback text extraction method")
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(pdf_path)
        full_text = ""
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text()
            full_text += text + "\n"
        
        doc.close()
        log_debug(f"✅ Fallback extraction: {len(full_text)} characters")
        return full_text.strip(), "PyMuPDF Fallback"
    
    except Exception as e:
        log_debug(f"❌ Fallback extraction failed: {e}")
        return "", "Extraction Failed"

def generate_basic_summary(text, length='medium'):
    """Generate basic summary using extractive method"""
    log_debug(f"📝 Generating basic summary ({length})")
    
    if not text or len(text.strip()) < 50:
        return "Insufficient text content for summary generation."
    
    import re
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    
    if not sentences:
        return "Unable to generate summary from the provided text."
    
    # Score sentences based on legal keywords
    legal_keywords = [
        'court', 'judge', 'order', 'judgment', 'appeal', 'petition', 'case',
        'plaintiff', 'defendant', 'appellant', 'respondent', 'section',
        'act', 'law', 'legal', 'ruled', 'decided', 'ordered', 'dismissed',
        'allowed', 'granted', 'denied', 'fine', 'penalty', 'compensation'
    ]
    
    scored_sentences = []
    for sentence in sentences[:20]:
        score = sum(1 for keyword in legal_keywords if keyword.lower() in sentence.lower())
        position_score = max(0, 5 - sentences.index(sentence) // 4)
        total_score = score + position_score
        
        if total_score > 0:
            scored_sentences.append((total_score, sentence))
    
    scored_sentences.sort(reverse=True, key=lambda x: x[0])
    
    target_sentences = {'brief': 2, 'medium': 4, 'detailed': 6}.get(length, 4)
    selected_sentences = [sentence for _, sentence in scored_sentences[:target_sentences]]
    
    if not selected_sentences:
        selected_sentences = sentences[:target_sentences]
    
    summary = '. '.join(selected_sentences)
    if not summary.endswith('.'):
        summary += '.'
    
    return summary

def extract_basic_metadata(text):
    """Extract basic metadata using regex patterns"""
    log_debug("🧠 Extracting basic metadata")
    
    import re
    metadata = {
        'case_number': 'Not found',
        'court_name': 'Not found',
        'judge_name': 'Not found',
        'order_date': 'Not found',
        'document_type': 'Legal Document',
        'petitioner_name': 'Not found',
        'respondent_name': 'Not found',
        'parties': [],
        'statutes_sections': []
    }
    
    if not text:
        return metadata
    
    # Case number patterns
    case_patterns = [
        r'(?:case|petition|appeal)\s*(?:no\.?|number)\s*:?\s*([A-Z0-9\/\-\.]+)',
        r'(?:crl\.?a\.?|criminal appeal)\s*no\.?\s*(\d+/\d+)',
        r'(?:civil suit|c\.s\.)\s*no\.?\s*(\d+/\d+)',
        r'(?:writ petition|w\.p\.)\s*no\.?\s*(\d+/\d+)',
    ]
    
    for pattern in case_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            metadata['case_number'] = match.group(1).strip()
            break
    
    # Court name patterns
    court_patterns = [
        r'(high court of [a-zA-Z\s]+)',
        r'(supreme court of india)',
        r'([a-zA-Z\s]+ high court)',
        r'(district court [a-zA-Z\s]+)',
    ]
    
    for pattern in court_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            metadata['court_name'] = match.group(1).strip().title()
            break
    
    # Date patterns
    date_patterns = [
        r'(?:dated|on|date)\s*:?\s*(\d{1,2}[\-\.\/]\d{1,2}[\-\.\/]\d{2,4})',
        r'(\d{1,2}[\-\.\/]\d{1,2}[\-\.\/]\d{2,4})',
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            metadata['order_date'] = match.group(1).strip()
            break
    
    # Judge name patterns
    judge_patterns = [
        r'(?:hon\'?ble|honourable)\s+(?:mr\.|ms\.|justice)\s+([a-zA-Z\s\.]+)',
        r'before\s*:?\s*(?:hon\'?ble)?\s*(?:mr\.|ms\.|justice)\s+([a-zA-Z\s\.]+)',
    ]
    
    for pattern in judge_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            metadata['judge_name'] = match.group(1).strip().title()
            break
    
    # Document type classification
    text_lower = text.lower()
    if any(keyword in text_lower for keyword in ['criminal appeal', 'crl.a']):
        metadata['document_type'] = 'Criminal Appeal'
    elif any(keyword in text_lower for keyword in ['civil suit', 'civil appeal']):
        metadata['document_type'] = 'Civil Case'
    elif any(keyword in text_lower for keyword in ['writ petition', 'w.p.']):
        metadata['document_type'] = 'Writ Petition'
    elif any(keyword in text_lower for keyword in ['judgment', 'judgement']):
        metadata['document_type'] = 'Judgment'
    elif any(keyword in text_lower for keyword in ['order', 'court order']):
        metadata['document_type'] = 'Court Order'
    
    log_debug(f"✅ Basic metadata extracted: {sum(1 for v in metadata.values() if v != 'Not found')} fields")
    return metadata

def process_document_complete(pdf_path, options):
    """Complete document processing pipeline"""
    log_debug(f"🚀 Starting complete processing for: {pdf_path}")
    log_debug(f"Options: {options}")
    
    start_time = time.time()
    result = {
        'success': False,
        'extractedText': '',
        'rawText': '',
        'summary': '',
        'metadata': {},
        'extractionMethod': 'Unknown',
        'documentType': 'unknown',
        'processingTime': 0,
        'wordCount': 0,
        'characterCount': 0,
        'pageCount': 0,
        'documentAnalysis': {
            'type': 'Unknown',
            'confidence': 0.0,
            'complexity': 'medium',
            'keyEntities': {}
        },
        'structureAnalysis': {},
        'options': options,
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'outputFiles': {},
        'processingStages': {
            'text_extraction': False,
            'metadata_extraction': False,
            'summarization': False,
            'file_output': False
        }
    }
    
    # Import modules
    modules = safe_import()
    
    # Create output directory
    output_dir = create_output_directory(pdf_path)
    if not output_dir:
        result['error'] = "Failed to create output directory"
        return result
    
    try:
        # ===========================================
        # PHASE 1: TEXT EXTRACTION
        # ===========================================
        log_debug("📋 PHASE 1: TEXT EXTRACTION")
        
        full_text = ""
        raw_full_text = ""
        method = "Unknown"
        
        # Try advanced OCR processing first
        if modules['ocr']:
            try:
                log_debug("🔍 Attempting advanced OCR processing...")
                ocr_system = modules['ocr'](pdf_path, output_dir)
                full_text, raw_full_text = ocr_system.process_pdf()
                method = "Advanced OCR (PaddleOCR)"
                log_debug(f"✅ Advanced OCR successful: {len(full_text)} characters")
                result['processingStages']['text_extraction'] = True
            except Exception as e:
                log_debug(f"❌ Advanced OCR failed: {e}")
                # Fall back to basic extraction
                full_text, method = extract_text_fallback(pdf_path)
                raw_full_text = full_text
        else:
            # Use fallback method
            full_text, method = extract_text_fallback(pdf_path)
            raw_full_text = full_text
        
        result['extractedText'] = full_text
        result['rawText'] = raw_full_text
        result['extractionMethod'] = method
        result['wordCount'] = len(full_text.split()) if full_text else 0
        result['characterCount'] = len(full_text) if full_text else 0
        
        if not full_text or len(full_text.strip()) < 10:
            result['error'] = "No meaningful text could be extracted from the document"
            result['processingTime'] = round(time.time() - start_time, 2)
            return result
        
        # ===========================================
        # PHASE 2: METADATA EXTRACTION
        # ===========================================
        log_debug("🧠 PHASE 2: METADATA EXTRACTION")
        
        metadata_result = {}
        
        # Try advanced metadata extraction
        if modules['metadata']:
            try:
                log_debug("🦙 Attempting advanced metadata extraction...")
                extractor = modules['metadata'](use_gpu=True, debug=False)
                metadata_result = extractor.extract_metadata_with_llama(raw_full_text)
                
                if metadata_result and metadata_result.get("extracted_data"):
                    log_debug("✅ Advanced metadata extraction successful")
                    result['processingStages']['metadata_extraction'] = True
                    
                    # Convert to frontend-friendly format
                    extracted_data = metadata_result.get("extracted_data", {})
                    result['metadata'] = {
                        'case_number': extracted_data.get('case_number', 'Not found'),
                        'court_name': extracted_data.get('court_name', 'Not found'),
                        'judge_name': extracted_data.get('judge_name', 'Not found'),
                        'order_date': extracted_data.get('order_date', 'Not found'),
                        'document_type': extracted_data.get('document_type', 'Legal Document'),
                        'petitioner_name': extracted_data.get('petitioner_name', 'Not found'),
                        'respondent_name': extracted_data.get('respondent_name', 'Not found'),
                        'parties': metadata_result.get('parties', []),
                        'statutes_sections': metadata_result.get('statutes_sections', []),
                        'extraction_confidence': metadata_result.get('extraction_metadata', {}).get('extraction_success_rate', 0),
                        'total_fields_extracted': metadata_result.get('extraction_metadata', {}).get('total_fields_extracted', 0)
                    }
                else:
                    raise Exception("Advanced metadata extraction returned no data")
                    
            except Exception as e:
                log_debug(f"❌ Advanced metadata extraction failed: {e}")
                # Fall back to basic metadata extraction
                result['metadata'] = extract_basic_metadata(raw_full_text)
        else:
            # Use basic metadata extraction
            result['metadata'] = extract_basic_metadata(raw_full_text)
        
        # Set document type from metadata
        result['documentType'] = result['metadata'].get('document_type', 'Legal Document').lower().replace(' ', '_')
        
        # ===========================================
        # PHASE 3: SUMMARIZATION
        # ===========================================
        log_debug("📝 PHASE 3: SUMMARIZATION")
        
        summary = ""
        summary_length = options.get('summaryLength', 'medium')
        
        # Try AI summarization first
        if modules['llama_summary']:
            try:
                log_debug("🤖 Attempting AI-powered summarization...")
                summary = modules['llama_summary'](full_text)
                if summary and len(summary.strip()) > 20:
                    log_debug("✅ AI summarization successful")
                    result['processingStages']['summarization'] = True
                else:
                    raise Exception("AI summary was empty or too short")
            except Exception as e:
                log_debug(f"❌ AI summarization failed: {e}")
                summary = generate_basic_summary(full_text, summary_length)
        else:
            summary = generate_basic_summary(full_text, summary_length)
        
        result['summary'] = summary
        
        # ===========================================
        # PHASE 4: SAVE OUTPUT FILES
        # ===========================================
        log_debug("💾 PHASE 4: SAVING OUTPUT FILES")
        
        if modules['output']:
            try:
                output_manager = modules['output']()
                
                # Save OCR results
                ocr_files = output_manager.save_ocr_results(
                    output_dir, full_text, raw_full_text, summary
                )
                
                # Convert metadata to expected format for output manager
                filename_prefix = os.path.splitext(os.path.basename(pdf_path))[0]
                converted_results = {
                    'detected_state': 'General',
                    'extraction_summary': {
                        'total_fields': len(result['metadata']),
                        'extracted_fields': sum(1 for v in result['metadata'].values() if v != 'Not found'),
                        'missing_fields': sum(1 for v in result['metadata'].values() if v == 'Not found'),
                        'extraction_methods': ['regex', 'ai']
                    },
                    'extracted_data': {k: {'value': v} for k, v in result['metadata'].items()},
                    'raw_text': raw_full_text
                }
                
                # Save metadata results
                metadata_files = output_manager.save_metadata_results(
                    output_dir, filename_prefix, converted_results, raw_full_text
                )
                
                result['outputFiles'] = {**ocr_files, **metadata_files}
                result['outputDirectory'] = output_dir
                result['processingStages']['file_output'] = True
                log_debug("✅ Output files saved successfully")
                
            except Exception as e:
                log_debug(f"❌ Failed to save output files: {e}")
                result['outputFiles'] = {}
        
        # ===========================================
        # FINAL PROCESSING
        # ===========================================
        
        # Document analysis
        result['documentAnalysis'] = {
            'type': result['metadata'].get('document_type', 'Legal Document'),
            'confidence': 0.85 if result['processingStages']['metadata_extraction'] else 0.6,
            'complexity': 'high' if result['wordCount'] > 2000 else 'medium' if result['wordCount'] > 500 else 'low',
            'keyEntities': {
                'case_numbers': [result['metadata']['case_number']] if result['metadata']['case_number'] != 'Not found' else [],
                'courts': [result['metadata']['court_name']] if result['metadata']['court_name'] != 'Not found' else [],
                'judges': [result['metadata']['judge_name']] if result['metadata']['judge_name'] != 'Not found' else [],
                'parties': result['metadata'].get('parties', []),
                'dates': [result['metadata']['order_date']] if result['metadata']['order_date'] != 'Not found' else []
            }
        }
        
        # Structure analysis
        import re
        result['structureAnalysis'] = {
            'sentence_count': len(re.split(r'[.!?]+', full_text)),
            'paragraph_count': full_text.count('\n\n') + 1,
            'entities_found': sum(len(v) if isinstance(v, list) else 1 
                                for v in result['documentAnalysis']['keyEntities'].values()
                                if v),
            'processing_stages_completed': sum(result['processingStages'].values()),
            'total_processing_stages': len(result['processingStages'])
        }
        
        result['success'] = True
        result['processingTime'] = round(time.time() - start_time, 2)
        
        log_debug(f"🎉 Complete processing finished successfully in {result['processingTime']} seconds")
        log_debug(f"📊 Processing stages completed: {result['structureAnalysis']['processing_stages_completed']}/{result['structureAnalysis']['total_processing_stages']}")
        
        return result
        
    except Exception as e:
        log_debug(f"❌ Complete processing failed: {e}")
        traceback.print_exc(file=sys.stderr)
        
        result['error'] = f"Complete processing failed: {str(e)}"
        result['extractedText'] = f"Processing error: {str(e)}"
        result['summary'] = "Document processing encountered an unexpected error."
        result['processingTime'] = round(time.time() - start_time, 2)
        
        return result

def main():
    """Main entry point for the integrated processor"""
    log_debug("🚀 Integrated Court Order Processor Started")
    log_debug(f"Command line args: {sys.argv}")
    
    if len(sys.argv) < 3:
        error_result = {
            'error': 'Usage: python integrated_processor.py <file_path> <options_json>',
            'extractedText': 'Invalid command line arguments',
            'summary': 'Script execution failed due to missing arguments',
            'metadata': {},
            'processingTime': 0,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        print(json.dumps(error_result, indent=2, ensure_ascii=False), flush=True)
        sys.exit(1)
    
    file_path = sys.argv[1]
    options_json = sys.argv[2]
    
    log_debug(f"📄 File path: {file_path}")
    log_debug(f"⚙️ Options JSON: {options_json}")
    
    try:
        options = json.loads(options_json)
        log_debug(f"✅ Parsed options: {options}")
    except json.JSONDecodeError as e:
        log_debug(f"❌ JSON decode error: {e}")
        options = {}
    
    if not os.path.exists(file_path):
        error_result = {
            'error': f'File not found: {file_path}',
            'extractedText': 'The specified file could not be found',
            'summary': 'File processing failed - file not found',
            'metadata': {},
            'processingTime': 0,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        print(json.dumps(error_result, indent=2, ensure_ascii=False), flush=True)
        sys.exit(1)
    
    # Process the document using the complete pipeline
    result = process_document_complete(file_path, options)
    
    # Ensure result is properly JSON serializable
    try:
        # Test if the result can be JSON serialized
        json.dumps(result)
        
        # Output result as clean JSON only to stdout
        print(json.dumps(result, indent=2, ensure_ascii=False), flush=True)
        log_debug("✅ Processing completed, result sent to stdout")
        
    except (TypeError, ValueError) as e:
        log_debug(f"❌ JSON serialization error: {e}")
        
        # Create a clean fallback result
        clean_result = {
            'error': f'JSON serialization failed: {str(e)}',
            'success': False,
            'extractedText': str(result.get('extractedText', '')),
            'summary': str(result.get('summary', 'Processing failed')),
            'metadata': result.get('metadata', {}),
            'processingTime': result.get('processingTime', 0),
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        print(json.dumps(clean_result, indent=2, ensure_ascii=False), flush=True)

if __name__ == '__main__':
    main()
