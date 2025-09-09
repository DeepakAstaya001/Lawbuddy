#!/usr/bin/env python3
"""
Clean wrapper for integrated processor to ensure JSON-only output
This wrapper redirects all non-JSON output to stderr and only outputs JSON to stdout
"""
import sys
import os
import json
import subprocess
import tempfile
import re

def clean_json_from_output(raw_output):
    """Extract clean JSON from mixed output"""
    try:
        # Try to find JSON object boundaries
        first_brace = raw_output.find('{')
        last_brace = raw_output.rfind('}')
        
        if first_brace != -1 and last_brace != -1 and first_brace < last_brace:
            json_part = raw_output[first_brace:last_brace + 1]
            
            # Validate it's proper JSON
            parsed = json.loads(json_part)
            return parsed
        else:
            raise ValueError("No JSON object found in output")
            
    except json.JSONDecodeError as e:
        # Try to find JSON line by line
        lines = raw_output.split('\n')
        json_lines = []
        in_json = False
        brace_count = 0
        
        for line in lines:
            line = line.strip()
            if line.startswith('{'):
                in_json = True
                brace_count = line.count('{') - line.count('}')
                json_lines.append(line)
            elif in_json:
                brace_count += line.count('{') - line.count('}')
                json_lines.append(line)
                if brace_count <= 0:
                    break
        
        if json_lines:
            json_text = '\n'.join(json_lines)
            return json.loads(json_text)
        else:
            raise ValueError(f"Could not extract JSON from output: {str(e)}")

def main():
    """Main wrapper function"""
    if len(sys.argv) < 3:
        error_result = {
            'error': 'Usage: python clean_processor.py <file_path> <options_json>',
            'extractedText': 'Invalid command line arguments',
            'summary': 'Script execution failed due to missing arguments',
            'metadata': {},
            'processingTime': 0,
            'success': False,
            'timestamp': '2025-08-31 00:00:00'
        }
        print(json.dumps(error_result, indent=2, ensure_ascii=False))
        sys.exit(1)
    
    file_path = sys.argv[1]
    options_json = sys.argv[2]
    
    # Get the path to the integrated processor
    script_dir = os.path.dirname(os.path.abspath(__file__))
    integrated_processor_path = os.path.join(script_dir, 'integrated_processor.py')
    
    if not os.path.exists(integrated_processor_path):
        error_result = {
            'error': f'Integrated processor not found: {integrated_processor_path}',
            'extractedText': 'Internal script error',
            'summary': 'Processing script not found',
            'metadata': {},
            'processingTime': 0,
            'success': False,
            'timestamp': '2025-08-31 00:00:00'
        }
        print(json.dumps(error_result, indent=2, ensure_ascii=False))
        sys.exit(1)
    
    try:
        # Run the integrated processor and capture all output
        result = subprocess.run([
            sys.executable, 
            integrated_processor_path, 
            file_path, 
            options_json
        ], capture_output=True, text=True, timeout=300)  # 5 minute timeout
        
        # Combine stdout and stderr for processing
        full_output = result.stdout
        
        if result.returncode == 0:
            try:
                # Try to extract clean JSON from the output
                json_data = clean_json_from_output(full_output)
                
                # Ensure required fields exist
                if not isinstance(json_data, dict):
                    raise ValueError("Output is not a JSON object")
                
                # Add success indicator if not present
                if 'success' not in json_data:
                    json_data['success'] = not json_data.get('error', False)
                
                # Output clean JSON
                print(json.dumps(json_data, indent=2, ensure_ascii=False))
                
            except Exception as e:
                # Fallback: create JSON from whatever we can extract
                fallback_result = {
                    'error': f'JSON extraction failed: {str(e)}',
                    'extractedText': full_output[-2000:] if len(full_output) > 2000 else full_output,  # Last 2000 chars
                    'summary': 'Processing completed but output format was invalid',
                    'metadata': {},
                    'processingTime': 0,
                    'success': False,
                    'extractionMethod': 'Fallback',
                    'documentType': 'unknown',
                    'wordCount': 0,
                    'characterCount': 0,
                    'timestamp': '2025-08-31 00:00:00',
                    'rawOutputLength': len(full_output),
                    'parseError': str(e)
                }
                print(json.dumps(fallback_result, indent=2, ensure_ascii=False))
        else:
            # Process failed
            error_result = {
                'error': f'Processing failed with exit code {result.returncode}',
                'extractedText': result.stderr if result.stderr else 'No error details available',
                'summary': 'Document processing failed',
                'metadata': {},
                'processingTime': 0,
                'success': False,
                'extractionMethod': 'Failed',
                'documentType': 'unknown',
                'wordCount': 0,
                'characterCount': 0,
                'timestamp': '2025-08-31 00:00:00',
                'exitCode': result.returncode,
                'stderr': result.stderr
            }
            print(json.dumps(error_result, indent=2, ensure_ascii=False))
            
    except subprocess.TimeoutExpired:
        timeout_result = {
            'error': 'Processing timed out after 5 minutes',
            'extractedText': 'Processing was taking too long and was terminated',
            'summary': 'Document processing timed out',
            'metadata': {},
            'processingTime': 300,
            'success': False,
            'extractionMethod': 'Timeout',
            'documentType': 'unknown',
            'wordCount': 0,
            'characterCount': 0,
            'timestamp': '2025-08-31 00:00:00'
        }
        print(json.dumps(timeout_result, indent=2, ensure_ascii=False))
        
    except Exception as e:
        exception_result = {
            'error': f'Unexpected error: {str(e)}',
            'extractedText': 'An unexpected error occurred during processing',
            'summary': 'Document processing encountered an unexpected error',
            'metadata': {},
            'processingTime': 0,
            'success': False,
            'extractionMethod': 'Error',
            'documentType': 'unknown',
            'wordCount': 0,
            'characterCount': 0,
            'timestamp': '2025-08-31 00:00:00',
            'exceptionType': type(e).__name__
        }
        print(json.dumps(exception_result, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
