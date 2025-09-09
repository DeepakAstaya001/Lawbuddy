import os
import sys
from pathlib import Path

def initialize_ocr_offline():
    """Initialize PaddleOCR with offline models from models folder - GPU mode"""
    
    # Enable GPU mode
    os.environ['PADDLEOCR_USE_GPU'] = 'true'
    
    # Import PaddleOCR after setting environment variables
    try:
        from paddleocr import PaddleOCR
    except Exception as e:
        print(f"Error importing PaddleOCR: {e}")
        return None
    models_dir = Path("pp_ocr_models")
    
    if not models_dir.exists():
        print("Models folder not found!")
        return None
    
    # Set model paths to None initially
    det_model_dir = None
    rec_model_dir = None
    cls_model_dir = None
    
    # Find extracted model directories - match exact folder names
    print("Looking for models in:", models_dir)
    
    # Available models in your folder:
    available_models = {
        # 'mobile_det': 'PP-OCRv5_mobile_det_infer',
        # 'mobile_rec': 'en_PP-OCRv5_mobile_rec_infer', 
        'server_det': 'PP-OCRv5_server_det_infer',
        'server_rec': 'PP-OCRv5_server_rec_infer',
        'doc_ori': 'PP-LCNet_x1_0_doc_ori_infer',
        'textline_ori': 'PP-LCNet_x1_0_textline_ori_infer'
    }
    
    found_models = {}
    
    for item in models_dir.iterdir():
        print(f"Found: {item.name}")
        if item.is_dir():
            model_path = str(item)
            # Match exact folder names
            # if item.name == available_models['mobile_det']:
                # found_models['mobile_det'] = model_path
                # print(f"✓ Mobile detection model: {model_path}")
            # elif item.name == available_models['mobile_rec']:
                # found_models['mobile_rec'] = model_path
                # print(f"✓ Mobile recognition model: {model_path}")
            if item.name == available_models['server_det']:
                found_models['server_det'] = model_path
                print(f"✓ Server detection model: {model_path}")
            elif item.name == available_models['server_rec']:
                found_models['server_rec'] = model_path
                print(f"✓ Server recognition model: {model_path}")
            elif item.name == available_models['doc_ori']:
                found_models['doc_ori'] = model_path
                print(f"✓ Document orientation model: {model_path}")
            elif item.name == available_models['textline_ori']:
                found_models['textline_ori'] = model_path
                print(f"✓ Textline orientation model: {model_path}")
    
    # Use server models first (higher accuracy), fallback to mobile models  
    if 'server_det' in found_models and 'server_rec' in found_models:
        det_model_dir = found_models['server_det']
        rec_model_dir = found_models['server_rec']
        model_type = "server"
        print("🚀 Using server models for higher accuracy")
    elif 'mobile_det' in found_models and 'mobile_rec' in found_models:
        det_model_dir = found_models['mobile_det']
        rec_model_dir = found_models['mobile_rec']
        model_type = "mobile"
        print("🚀 Using mobile models for faster processing")
    else:
        print("❌ No matching model pairs found")
        det_model_dir = None
        rec_model_dir = None
        model_type = None
    
    # Skip classification models for now (they cause compatibility issues)
    cls_model_dir = None
    
    # Initialize OCR with local models
    try:
        if det_model_dir and rec_model_dir and model_type:
            print("Initializing PaddleOCR with local models...")
            print(f"Detection model: {det_model_dir}")
            print(f"Recognition model: {rec_model_dir}")
            
            # Set correct model names based on type
            # if model_type == "server":
            det_model_name = "PP-OCRv5_server_det"
            rec_model_name = "PP-OCRv5_server_rec"
            # else:  # mobile
            #     det_model_name = "PP-OCRv5_mobile_det"
            #     rec_model_name = "en_PP-OCRv5_mobile_rec"
            
            # Use offline models with GPU enabled (newer PaddleOCR automatically uses GPU if available)
            ocr = PaddleOCR(
                # use_gpu=True,                     # Removed - newer version auto-detects GPU
                text_detection_model_name=det_model_name,
                text_detection_model_dir=det_model_dir,
                text_recognition_model_name=rec_model_name,
                text_recognition_model_dir=rec_model_dir,
                use_textline_orientation=False,
                use_doc_orientation_classify=False,  # Disable doc orientation
                use_doc_unwarping=False,            # Disable document unwarping
                lang='en'                           # Set language explicitly
            )
            print(f"✓ PaddleOCR initialized with ONLY offline {model_type} models - no online downloads")
            return ocr
        else:
            print("Model directories not found. Using default PaddleOCR with GPU...")
            ocr = PaddleOCR(
                # use_gpu=True,                     # Removed - auto-detects GPU
                use_textline_orientation=True,
                lang='en'
            )
            return ocr
    except Exception as e:
        print(f"Error initializing OCR: {e}")
        print("Falling back to simple initialization...")
        try:
            ocr = PaddleOCR(lang='en')  # Auto-detects GPU
            return ocr
        except Exception as e2:
            print(f"Failed to initialize OCR: {e2}")
            return None