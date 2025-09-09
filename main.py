import os
import sys
import time
import traceback
# from datetime import datetime
from ocr.ocr import AdvancedLegalOCR
from metadata.metadata_extractor import MetaDataExtractor
from utils.output_manager import OutputManager
from utils.llama import generate_court_order_summary
def main():
    """Enhanced main function with OCR, Metadata Extraction, and User-Confirmed Summarization"""
    
    print("🚀 COMPREHENSIVE LEGAL DOCUMENT PROCESSING SYSTEM")
    print("=" * 60)
    print("📋 Phase 1: OCR Text Extraction")
    print("🧠 Phase 2: Enhanced Metadata Extraction (Pattern + AI)")
    print("❓ User Confirmation for Summary Generation")
    print("📝 Phase 3: AI-Powered Document Summarization")
    print("=" * 60)

    pdf_path = "CourtOrder/Himachal_pradesh_high_court/HIMACHAL PRADESH High Court (8).pdf"

    # Initialize output manager
    output_manager = OutputManager()
    
    # Create output folder named after the PDF file
    filename_prefix = os.path.splitext(os.path.basename(pdf_path))[0]
    output_dir = output_manager.create_output_folder(pdf_path)
    
    # Check if PDF exists
    if not os.path.exists(pdf_path):
        print(f"❌ PDF not found: {pdf_path}")
        print("📁 Available files in scanned_pdf/:")
        if os.path.exists("scanned_pdf"):
            for file in os.listdir("scanned_pdf"):
                if file.endswith('.pdf'):
                    print(f"   📄 {file}")
        return
    
    try:
        start_time = time.time()
        # ===========================================
        # PHASE 1: OCR TEXT EXTRACTION
        # ===========================================
        print("\n📋 PHASE 1: OCR TEXT EXTRACTION")
        print("-" * 40)
        
        ocr_system = AdvancedLegalOCR(pdf_path, output_dir)
        full_text, raw_full_text= ocr_system.process_pdf()
        summary = generate_court_order_summary(full_text)
        # Save OCR results using output manager
        ocr_files = output_manager.save_ocr_results(output_dir, full_text, raw_full_text, summary)

        phase1_time = time.time() - start_time
        print(f"✅ Phase 1 completed in {phase1_time:.2f} seconds")
        
        # Check if text extraction was successful
        if not full_text.strip():
            print("❌ Text extraction failed - no text extracted")
            return
    except Exception as e:
        print(f"❌ Error during OCR processing: {e}")
        traceback.print_exc()
        return
    
    # ===========================================
    # PHASE 2: METADATA EXTRACTION
    # ===========================================
    print(f"\n🧠 PHASE 2: METADATA EXTRACTION")
    print("-" * 45)

    try:
        metadata_extractor = MetaDataExtractor(use_gpu=True, debug=True)
        
        # Extract metadata from the raw text directly
        print("🔍 Extracting metadata from text...")
        metadata_result = metadata_extractor.extract(raw_full_text)
        
        if metadata_result and "error" not in metadata_result:
            # Save metadata results using output manager
            metadata_files = output_manager.save_metadata_results(
                output_dir, filename_prefix, metadata_result
            )
            
            print(f"✅ Metadata extracted and saved to {output_dir}")
            print(f"📊 Found {metadata_result['extraction_summary']['extracted_fields']} fields")
            print(f"🎯 Average confidence: {metadata_result['extraction_summary']['average_confidence']:.1%}")
            
            phase2_time = time.time() - start_time - phase1_time
            print(f"✅ Phase 2 completed in {phase2_time:.2f} seconds")
        else:
            print(f"⚠️ Metadata extraction failed")
            
    except Exception as e:
        print(f"❌ Error during metadata extraction: {e}")
        traceback.print_exc()
    

if __name__ == "__main__":
    main()
