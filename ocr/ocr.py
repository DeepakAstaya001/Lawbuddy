from paddleocr import PaddleOCR
from pdf2image import convert_from_path
from PIL import Image
import fitz  # PyMuPDF
import os
import re
import json
import time
import statistics
import shutil
import datetime
from typing import Dict, List
from ocr.text_processor import LegalTextProcessor
from ocr.loading_ocr_models import initialize_ocr_offline

class AdvancedLegalOCR:
    """Advanced OCR system for legal documents with text processing"""
    
    def __init__(self, pdf_path: str, output_dir: str = "output", dpi: int = 500, max_size: tuple = (1500, 1500)):
        self.pdf_path = pdf_path
        self.output_dir = output_dir
        self.dpi = dpi
        self.max_size = max_size
        
        # Initialize processors
        print("🚀 Initializing offline OCR models...")
        self.ocr = initialize_ocr_offline()
        if not self.ocr:
            print("❌ Failed to initialize offline OCR, falling back to default")
            self.ocr = PaddleOCR(use_textline_orientation=False, lang='en')  # Auto-detects GPU
        self.text_processor = LegalTextProcessor()
        
        # Stats trackers
        self.start_time = time.time()
        self.page_times = []
        self.ocr_confidences = []
        self.full_text = ""
        self.raw_full_text = ""

        # Setup output directory
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
            print(f"🧹 Removed old folder: {output_dir}")
        os.makedirs(output_dir, exist_ok=True)
        Image.MAX_IMAGE_PIXELS = None
        
        print(f"🚀 Advanced Legal OCR initialized")
        print(f"📄 Source: {pdf_path}")
        print(f"📁 Output: {output_dir}")
    
    def process_pdf(self):
        """Main method to process PDF with OCR and legal text processing"""
        
        print("\n📄 Reading PDF...")
        doc = fitz.open(self.pdf_path)
        page_count = len(doc)
        print(f"✅ Found {page_count} page(s)")
        
        # Process each page
        for i in range(page_count):
            page_start = time.time()
            page = doc.load_page(i)
            try:
                page_text = page.get_text().strip()
            except AttributeError:
                # Fallback for different PyMuPDF versions
                page_text = page.getText().strip() if hasattr(page, 'getText') else ""
            
            if page_text:
                method = "PyMuPDF"
                print(f"📖 Page {i+1}: Using direct text extraction")
            else:
                method = "OCR"
                print(f"🔍 Page {i+1}: Using OCR (scanned page)")
                # Fallback: render image + run OCR
                pix = page.get_pixmap(matrix=fitz.Matrix(2.1, 2.1))
                img_path = os.path.join(self.output_dir, f"page_{i+1}.png")
                pix.save(img_path)
                result = self.ocr.predict(img_path)
                os.remove(img_path)  # Clean up image file 
                texts = result[0]['rec_texts']
                scores = result[0]['rec_scores']
                self.ocr_confidences.extend(scores)
                page_text = "\n".join(texts)
                
                # Show OCR confidence for this page
                avg_conf = sum(scores) / len(scores) if scores else 0
                print(f"   📊 OCR Confidence: {avg_conf:.2%}")
            
            # Clean the page text using legal processor
            cleaned_page_text = self.text_processor.clean_raw_text(page_text)
            self.raw_full_text += page_text + "\n"
            self.full_text += cleaned_page_text + "\n"
            self.page_times.append(time.time() - page_start)
            print(f"✅ Page {i+1}: {method} in {self.page_times[-1]:.2f} sec")
        
        doc.close()
        
        # Save full text
        with open(os.path.join(self.output_dir, "full_text.txt"), "w", encoding="utf-8") as f:
            f.write(self.full_text.strip())
        
        # Save raw full text
        with open(os.path.join(self.output_dir, "raw_full_text.txt"), "w", encoding="utf-8") as f:
            f.write(self.raw_full_text.strip())
        
        # Generate and return stats
        # processing_stats = self._generate_stats()
        
        # Return the required values
        return self.full_text.strip(), self.raw_full_text.strip()

    def _generate_stats(self):
        """Generate and display final statistics"""
        
        total_time = time.time() - self.start_time
        avg_page_time = sum(self.page_times) / len(self.page_times) if self.page_times else 0
        avg_ocr_score = statistics.mean(self.ocr_confidences) if self.ocr_confidences else 0
        
        stats = {
            'processing_time': {
                'total_seconds': total_time,
                'avg_page_seconds': avg_page_time,
                'pages_processed': len(self.page_times)
            },
            'ocr_performance': {
                'words_processed': len(self.ocr_confidences),
                'avg_confidence': avg_ocr_score,
                'low_confidence_words': len([c for c in self.ocr_confidences if c < 0.8])
            },
            'text_metrics': {
                'total_characters': len(self.full_text),
                'total_words': len(self.full_text.split()),
                'total_lines': len(self.full_text.split('\n'))
            }
        }
        
        # Save stats
        with open(os.path.join(self.output_dir, "processing_stats.json"), "w", encoding="utf-8") as f:
            json.dump(stats, f, indent=2)
        
        # Display summary
        print(f"\n{'='*60}")
        print(f"🎯 PROCESSING SUMMARY")
        print(f"{'='*60}")
        print(f"🕒 Total Time: {total_time:.2f} sec")
        print(f"📄 Pages Processed: {len(self.page_times)}")
        print(f"⏱️ Avg Time/Page: {avg_page_time:.2f} sec")
        print(f"🔤 Total Words: {len(self.full_text.split())}")
        
        if self.ocr_confidences:
            print(f"🔎 OCR Words: {len(self.ocr_confidences)}")
            print(f"📊 Avg OCR Confidence: {avg_ocr_score:.2%}")
            low_conf = len([c for c in self.ocr_confidences if c < 0.8])
            if low_conf > 0:
                print(f"⚠️ Low Confidence Words: {low_conf}")
        else:
            print(f"📖 No OCR needed (all text extracted directly)")
        
        print(f"📁 All outputs saved in: {self.output_dir}")
        print(f"{'='*60}")
        
        return stats

