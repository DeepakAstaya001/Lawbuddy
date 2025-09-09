import os
import re
import json
import logging
import time
import warnings
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, asdict
from pathlib import Path
from text_processor import LegalTextProcessor

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

# AI/ML Libraries with flexible imports
AI_MODULES = {}

# LLaMA integration
try:
    from langchain_ollama.llms import OllamaLLM
    AI_MODULES['llama'] = True
except ImportError:
    AI_MODULES['llama'] = False

# SpaCy for NER
try:
    import spacy
    AI_MODULES['spacy'] = True
except ImportError:
    AI_MODULES['spacy'] = False

# Transformers for various models
try:
    import torch
    from transformers import (
        AutoTokenizer, AutoModelForTokenClassification,
        AutoModelForQuestionAnswering, pipeline,
        AutoModel, AutoConfig,
        BertTokenizer, BertForQuestionAnswering,
        RobertaTokenizer, RobertaForQuestionAnswering,
        DistilBertTokenizer, DistilBertForQuestionAnswering
    )
    AI_MODULES['transformers'] = True
except ImportError:
    AI_MODULES['transformers'] = False

# Advanced NLP libraries
try:
    import nltk
    from nltk.tokenize import sent_tokenize, word_tokenize, ne_chunk
    from nltk.tag import pos_tag
    from nltk.chunk import ne_chunk
    from nltk.tree import Tree
    # Download required NLTK data
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)
    try:
        nltk.data.find('taggers/averaged_perceptron_tagger')
    except LookupError:
        nltk.download('averaged_perceptron_tagger', quiet=True)
    try:
        nltk.data.find('chunkers/maxent_ne_chunker')
    except LookupError:
        nltk.download('maxent_ne_chunker', quiet=True)
    try:
        nltk.data.find('corpora/words')
    except LookupError:
        # self.text_processor = LegalTextProcessor()
        nltk.download('words', quiet=True)
    AI_MODULES['nltk'] = True
except ImportError:
    AI_MODULES['nltk'] = False

# Document embeddings and similarityelf.text_processor = LegalTextProcessor()
try:
    from sentence_transformers import SentenceTransformer
    AI_MODULES['sentence_transformers'] = True
except ImportError:
    AI_MODULES['sentence_transformers'] = False

# Additional NLP libraries
try:
    import dateparser
    AI_MODULES['dateparser'] = True
except ImportError:
    AI_MODULES['dateparser'] = False

# Import existing modules
from state_name import detect_state_from_text
from state_patterns import STATE_PATTERNS, GENERAL_PATTERNS


@dataclass
class ExtractionResult:
    """Stores extraction result with metadata"""
    field_name: str
    value: str
    confidence: float
    method: str
    source_text: str = ""


@dataclass
class AIModelConfig:
    """Configuration for AI models"""
    name: str
    type: str  # 'ner', 'qa', 'classification', 'generation'
    model_path: str
    enabled: bool = True
    min_confidence: float = 0.1


class MetaDataExtractor:
    
    def __init__(self, use_gpu: bool = False, debug: bool = True):
        self.use_gpu = use_gpu and torch.cuda.is_available() if AI_MODULES.get('transformers') else False
        self.device = "cuda" if self.use_gpu else "cpu"
        self.debug = debug
        # self.text_processor = LegalTextProcessor()
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO if debug else logging.WARNING,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Initialize extraction variables
        self.full_text = ""
        self.page_times = []
        self.output_dir = "output"
        
        # Field definitions - COMPREHENSIVE EXTRACTION for Maximum Accuracy
        self.extraction_fields = [
            # Core Case Information (CRITICAL)
            'case_number', 'order_date', 'judge_name', 'court_name',
            
            # Key Legal Parties (ESSENTIAL)
            'petitioner_name', 'respondent_name',
            
            # Party Details (COMPREHENSIVE)
            'party_type', 'official_designation', 'age', 'alias', 'relations',
            
            # Address Components (DETAILED)
            'address_apartment', 'address_street', 'address_village', 
            'address_city', 'address_district', 'address_state', 'address_zipcode',
            
            # Legal Core (IMPORTANT)
            'statutes_offences', 'judgment', 'decision',
            
            # Supporting Information (VALUABLE)
            'fir_crime_no', 'police_station', 'advocates', 'crime_details',
            
            # Additional Details for Complete Coverage
            'directions', 'disposition'
            
            # Strategy: Extract ALL relevant fields for comprehensive legal metadata
        ]
        
        # Initialize AI models
        self.ai_models = {}
        self._initialize_ai_models()
        
        self.logger.info(f"🤖 AI Enhanced Extractor initialized with {len(self.ai_models)} models")
        self.logger.info(f"📊 Available AI modules: {[k for k, v in AI_MODULES.items() if v]}")
    
    def _get_timestamp(self) -> str:
        """Get current timestamp as formatted string"""
        return datetime.now().isoformat()
    
    def _initialize_ai_models(self):
        """Initialize AI models in offline mode to avoid network hangs"""
        
        print("🔧 Initializing AI models in offline mode...")
        
        # Initialize only locally available models
        self.ai_models = {}
        
        # Try to load SpaCy model if available locally
        if AI_MODULES.get('spacy'):
            try:
                import spacy
                nlp = spacy.load("en_core_web_lg")
                self.ai_models['spacy_local'] = {
                    'model': nlp,
                    'type': 'ner',
                    'confidence_threshold': 0.3
                }
                print("✅ Loaded local SpaCy model")
            except OSError:
                print("⚠️ No local SpaCy model found")
        
        print(f"🎯 Initialized {len(self.ai_models)} AI models in offline mode")
    
    def _init_spacy_models(self):
        """Initialize SpaCy models"""
        spacy_models = ['en_core_web_sm', 'en_core_web_md', 'en_core_web_lg']
        
        for model_name in spacy_models:
            try:
                nlp = spacy.load(model_name)
                self.ai_models[f'spacy_{model_name}'] = {
                    'model': nlp,
                    'type': 'ner',
                    'confidence_threshold': 0.3
                }
                self.logger.info(f"✅ Loaded SpaCy model: {model_name}")
                break  # Use the first available model
            except OSError:
                self.logger.warning(f"⚠️ SpaCy model {model_name} not found")
                continue
    
    def _init_transformer_models(self):
        """Initialize various Transformer models"""
        
        # Question Answering Models - ALL MODELS for Maximum Accuracy
        qa_models = [
            {
                'name': 'law-ai/InLegalBERT',                    # BEST for Indian legal documents
                'description': 'Indian Legal BERT model',
                'priority': 1
            },
            {
                'name': 'deepset/roberta-base-squad2',           # High accuracy general QA
                'description': 'General purpose QA model',
                'priority': 2
            },
            {
                'name': 'deepset/bert-base-cased-squad2',        # BERT baseline
                'description': 'BERT-based QA model',
                'priority': 3
            },
            {
                'name': 'distilbert-base-cased-distilled-squad', # Fast but still accurate
                'description': 'Fast DistilBERT QA model',
                'priority': 4
            }
            # Strategy: Use ensemble of all models for maximum extraction accuracy
        ]
        
        for qa_config in qa_models:  # Load ALL QA models for maximum accuracy
            try:
                qa_pipeline = pipeline(
                    "question-answering",
                    model=qa_config['name'],
                    device=0 if self.use_gpu else -1,
                    return_all_scores=True
                )
                
                # Set confidence thresholds based on model capability
                if 'legal' in qa_config['name'].lower():
                    confidence_threshold = 0.05  # Very low threshold for legal models
                elif 'roberta' in qa_config['name'].lower():
                    confidence_threshold = 0.1   # Low threshold for RoBERTa
                else:
                    confidence_threshold = 0.15  # Standard threshold for others
                
                self.ai_models[f"qa_{qa_config['name'].split('/')[-1]}"] = {
                    'model': qa_pipeline,
                    'type': 'qa',
                    'confidence_threshold': confidence_threshold,
                    'description': qa_config['description'],
                    'priority': qa_config['priority'],
                    'accuracy_tier': 'high' if qa_config['priority'] <= 2 else 'medium'
                }
                self.logger.info(f"✅ Loaded HIGH-ACCURACY QA model: {qa_config['name']} (Priority: {qa_config['priority']})")
            except Exception as e:
                self.logger.warning(f"⚠️ Failed to load QA model {qa_config['name']}: {e}")
                continue  # Continue with other models
        
        # Named Entity Recognition Models - OPTIMIZED FOR MAXIMUM ACCURACY
        ner_models = [
            # TIER 1: Legal-specific NER (ESSENTIAL for court documents)
            'mudigosa/BERT_TOKEN_CLASSIFIER_LAW_COURT_PROCEEDING',
            
            # TIER 2: High-accuracy general NER models (comprehensive coverage)
            'Jean-Baptiste/roberta-large-ner-english',    # Highest accuracy (1.3GB but worth it)
            'dbmdz/bert-large-cased-finetuned-conll03-english',  # BERT Large, very accurate
            
            # TIER 3: Fast backup (if others fail)
            'dslim/bert-base-NER'
            
            # Strategy: Load all models for ensemble accuracy - better extraction quality
        ]
        
        for ner_model in ner_models[:3]:  # Load top 3 models for maximum accuracy
            try:
                ner_pipeline = pipeline(
                    "ner",
                    model=ner_model,
                    aggregation_strategy="simple",
                    device=0 if self.use_gpu else -1
                )
                
                # Assign accuracy-based priorities and confidence thresholds
                if 'LAW_COURT' in ner_model:
                    priority, confidence, specialization = 1, 0.1, 'legal'  # Lowest threshold for legal model
                elif 'roberta-large' in ner_model:
                    priority, confidence, specialization = 2, 0.15, 'high_accuracy'  # RoBERTa Large
                elif 'bert-large' in ner_model:
                    priority, confidence, specialization = 3, 0.2, 'bert_large'  # BERT Large  
                else:
                    priority, confidence, specialization = 4, 0.25, 'general'  # Base models
                
                self.ai_models[f"ner_{ner_model.split('/')[-1]}"] = {
                    'model': ner_pipeline,
                    'type': 'ner',
                    'confidence_threshold': confidence,
                    'priority': priority,
                    'specialization': specialization,
                    'accuracy_tier': 'high' if priority <= 3 else 'medium'
                }
                self.logger.info(f"✅ Loaded HIGH-ACCURACY NER model: {ner_model} (Priority: {priority})")
            except Exception as e:
                self.logger.warning(f"⚠️ Failed to load NER model {ner_model}: {e}")
                continue  # Try next model for fallback
        
        # Text Classification for legal document analysis
        legal_classifiers = [
            'nlpaueb/legal-bert-base-uncased',
            'zlucia/custom-legalbert',
            'nlpaueb/legal-bert-small-uncased'
        ]
        
        for legal_model in legal_classifiers[:2]:  # Load first 2
            try:
                classifier = pipeline(
                    "text-classification",
                    model=legal_model,
                    device=0 if self.use_gpu else -1
                )
                model_name = legal_model.split('/')[-1]
                self.ai_models[f'legal_classifier_{model_name}'] = {
                    'model': classifier,
                    'type': 'classification',
                    'confidence_threshold': 0.3
                }
                self.logger.info(f"✅ Loaded Legal classifier: {legal_model}")
            except Exception as e:
                self.logger.warning(f"⚠️ Failed to load Legal classifier {legal_model}: {e}")
        
        # Try specialized legal QA model
        try:
            legal_qa = pipeline(
                "question-answering",
                model="nlpaueb/legal-bert-base-uncased",
                device=0 if self.use_gpu else -1
            )
            self.ai_models['legal_qa_bert'] = {
                'model': legal_qa,
                'type': 'qa',
                'confidence_threshold': 0.2,
                'description': 'Legal domain QA model'
            }
            self.logger.info("✅ Loaded Legal QA BERT")
        except Exception as e:
            self.logger.warning(f"⚠️ Failed to load Legal QA BERT: {e}")
    
    def _init_nltk_models(self):
        """Initialize NLTK-based models"""
        try:
            # NLTK NER and POS tagging
            self.ai_models['nltk_ner'] = {
                'model': 'nltk_builtin',
                'type': 'ner',
                'confidence_threshold': 0.4
            }
            self.logger.info("✅ NLTK NER initialized")
        except Exception as e:
            self.logger.warning(f"⚠️ NLTK initialization failed: {e}")
    
    def _init_sentence_models(self):
        """Initialize Sentence Transformer models"""
        sentence_models = [
            'all-MiniLM-L6-v2',
            'all-mpnet-base-v2',
            'paraphrase-multilingual-MiniLM-L12-v2'
        ]
        
        for model_name in sentence_models[:1]:  # Load first one
            try:
                model = SentenceTransformer(model_name)
                self.ai_models[f'sentence_{model_name}'] = {
                    'model': model,
                    'type': 'similarity',
                    'confidence_threshold': 0.3
                }
                self.logger.info(f"✅ Loaded Sentence Transformer: {model_name}")
                break
            except Exception as e:
                self.logger.warning(f"⚠️ Failed to load Sentence Transformer {model_name}: {e}")
    
    def extract(self, text_input: str) -> Dict[str, Any]:
        """
        Main extraction method - extracts metadata from provided text
        Args:
            text_input: The text content to extract metadata from
        Returns:
            Dictionary containing extraction results
        """
        self.logger.info(f"🚀 Starting metadata extraction")
        
        # Use the provided text directly
        text = text_input.strip() if text_input else ""
        
        if not text:
            self.logger.error("No text provided for metadata extraction")
            return {}
        
        self.logger.info(f"📄 Processing text length: {len(text)} characters")
        
        # 2. Detect state/UT
        detected_state = detect_state_from_text(text)
        self.logger.info(f"🗺️ Detected state: {detected_state}")
        
        # 3. Extract using state-specific patterns
        self.logger.info("🔍 Applying state-specific regex patterns...")
        pattern_results = self.extract_with_patterns(text, detected_state)
        
        # 4. Identify missing fields
        missing_fields = [field for field in self.extraction_fields if field not in pattern_results]
        self.logger.info(f"❓ Missing fields after pattern extraction: {missing_fields}")
        
        # 5. Apply AI models sequentially for missing fields
        all_results = pattern_results.copy()
        
        if missing_fields:
            # 5a. SpaCy NER
            self.logger.info("🧠 Applying SpaCy NER models...")
            spacy_results = self.extract_with_spacy(text, missing_fields)
            self.logger.info(f"   🔍 SpaCy found: {list(spacy_results.keys()) if spacy_results else 'Nothing'}")
            for field, result in spacy_results.items():
                if field not in all_results:
                    all_results[field] = result
            
            # Update missing fields
            missing_fields = [field for field in missing_fields if field not in spacy_results]
            
            # 5b. Question-Answering models
            if missing_fields:
                self.logger.info("❓ Applying Question-Answering models...")
                qa_results = self.extract_with_qa_models(text, missing_fields)
                self.logger.info(f"   🔍 QA Models found: {list(qa_results.keys()) if qa_results else 'Nothing'}")
                for field, result in qa_results.items():
                    if field not in all_results:
                        all_results[field] = result
                
                # Update missing fields
                missing_fields = [field for field in missing_fields if field not in qa_results]
            
            # 5c. Specialized Legal Models
            if missing_fields:
                self.logger.info("🏛️ Applying Specialized Legal Models...")
                legal_results = self.extract_with_legal_models(text, missing_fields)
                self.logger.info(f"   🔍 Legal Models found: {list(legal_results.keys()) if legal_results else 'Nothing'}")
                for field, result in legal_results.items():
                    if field not in all_results:
                        all_results[field] = result
                
                # Update missing fields
                missing_fields = [field for field in missing_fields if field not in legal_results]
            
            # 5d. General NER models
            if missing_fields:
                self.logger.info("🏷️ Applying General NER models...")
                ner_results = self.extract_with_ner_models(text, missing_fields)
                self.logger.info(f"   🔍 NER Models found: {list(ner_results.keys()) if ner_results else 'Nothing'}")
                for field, result in ner_results.items():
                    if field not in all_results:
                        all_results[field] = result
                
                # Update missing fields
                missing_fields = [field for field in missing_fields if field not in ner_results]
            
            # 5e. Date parsing for dates
            if missing_fields:
                self.logger.info("📅 Applying date parsing...")
                date_results = self.extract_with_date_parser(text, missing_fields)
                for field, result in date_results.items():
                    if field not in all_results:
                        all_results[field] = result
        
        # 6. Compile final results
        final_results = {
            'detected_state': detected_state,
            'extraction_summary': {
                'total_fields': len(self.extraction_fields),
                'extracted_fields': len(all_results),
                'missing_fields': len([field for field in self.extraction_fields if field not in all_results]),
                'extraction_methods': list(set([result.method for result in all_results.values()]))
            },
            'extracted_data': {},
            'metadata': {
                'text_length': len(text),
                'available_ai_models': list(self.ai_models.keys()),
                'processing_timestamp': datetime.now().isoformat()
            },
            'raw_text': text  # Store the raw extracted text
        }
        
        # Convert results to dictionary format
        for field, result in all_results.items():
            final_results['extracted_data'][field] = {
                'value': result.value,
                'confidence': result.confidence,
                'method': result.method,
                'source_text': result.source_text[:100] + "..." if len(result.source_text) > 100 else result.source_text
            }
        
        # Calculate overall confidence
        if all_results:
            avg_confidence = sum([result.confidence for result in all_results.values()]) / len(all_results)
            final_results['extraction_summary']['average_confidence'] = avg_confidence
        else:
            final_results['extraction_summary']['average_confidence'] = 0.0
        
        self.logger.info(f"✅ Extraction completed!")
        self.logger.info(f"📊 Extracted {len(all_results)}/{len(self.extraction_fields)} fields")
        self.logger.info(f"🎯 Average confidence: {final_results['extraction_summary']['average_confidence']:.2%}")
        
        return final_results
    
    def extract_with_patterns(self, text: str, state: str) -> Dict[str, ExtractionResult]:
        """Extract using state-specific and general patterns"""
        results = {}
        
        # Get patterns for the detected state
        state_patterns = STATE_PATTERNS.get(state, {})
        
        # Combine with general patterns
        all_patterns = {**GENERAL_PATTERNS, **state_patterns}
        
        for field_name in self.extraction_fields:
            if field_name in all_patterns:
                patterns = all_patterns[field_name]
                if isinstance(patterns, dict):
                    # Handle nested patterns (like petitioner.name)
                    continue
                elif isinstance(patterns, list):
                    for pattern in patterns:
                        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
                        if match:
                            value = match.group(1) if match.groups() else match.group(0)
                            results[field_name] = ExtractionResult(
                                field_name=field_name,
                                value=value.strip(),
                                confidence=0.8,  # High confidence for pattern matches
                                method=f"regex_pattern_{state}",
                                source_text=match.group(0)
                            )
                            break
        
        # Handle nested patterns (petitioner, respondent details)
        self._extract_nested_patterns(text, state, results)
        
        return results
    
    def _extract_nested_patterns(self, text: str, state: str, results: Dict[str, ExtractionResult]):
        """Extract nested patterns like petitioner and respondent details"""
        state_patterns = STATE_PATTERNS.get(state, {})
        all_patterns = {**GENERAL_PATTERNS, **state_patterns}
        
        # Extract petitioner details
        if 'petitioner' in all_patterns:
            petitioner_patterns = all_patterns['petitioner']
            
            # Extract petitioner name
            if 'name' in petitioner_patterns:
                for pattern in petitioner_patterns['name']:
                    match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
                    if match:
                        results['petitioner_name'] = ExtractionResult(
                            field_name='petitioner_name',
                            value=match.group(1).strip(),
                            confidence=0.8,
                            method=f"regex_pattern_{state}",
                            source_text=match.group(0)
                        )
                        break
            
            # Extract petitioner age (store as additional info)
            if 'age' in petitioner_patterns:
                for pattern in petitioner_patterns['age']:
                    match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
                    if match:
                        # Store age as part of petitioner_details for reference
                        if 'petitioner_details' not in results:
                            results['petitioner_details'] = ExtractionResult(
                                field_name='petitioner_details',
                                value={},
                                confidence=0.8,
                                method=f"regex_pattern_{state}",
                                source_text=""
                            )
                        if isinstance(results['petitioner_details'].value, dict):
                            results['petitioner_details'].value['age'] = match.group(1).strip()
                        break
            
            # Extract petitioner relation (s/o, d/o, etc.)
            if 'relation' in petitioner_patterns:
                for pattern in petitioner_patterns['relation']:
                    match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
                    if match:
                        if 'petitioner_details' not in results:
                            results['petitioner_details'] = ExtractionResult(
                                field_name='petitioner_details',
                                value={},
                                confidence=0.8,
                                method=f"regex_pattern_{state}",
                                source_text=""
                            )
                        if isinstance(results['petitioner_details'].value, dict):
                            results['petitioner_details'].value['relation'] = f"{match.group(1)} {match.group(2).strip()}"
                        break
            
            # Extract petitioner address
            if 'address' in petitioner_patterns:
                address_parts = {}
                for addr_type, addr_patterns in petitioner_patterns['address'].items():
                    for pattern in addr_patterns:
                        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
                        if match:
                            address_parts[addr_type] = match.group(1).strip()
                            break
                
                if address_parts:
                    if 'petitioner_details' not in results:
                        results['petitioner_details'] = ExtractionResult(
                            field_name='petitioner_details',
                            value={},
                            confidence=0.8,
                            method=f"regex_pattern_{state}",
                            source_text=""
                        )
                    if isinstance(results['petitioner_details'].value, dict):
                        results['petitioner_details'].value['address'] = address_parts
        
        # Extract respondent details
        if 'respondent' in all_patterns:
            respondent_patterns = all_patterns['respondent']
            if 'name' in respondent_patterns:
                for pattern in respondent_patterns['name']:
                    match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
                    if match:
                        results['respondent_name'] = ExtractionResult(
                            field_name='respondent_name',
                            value=match.group(1).strip(),
                            confidence=0.8,
                            method=f"regex_pattern_{state}",
                            source_text=match.group(0)
                        )
                        break
    
    def extract_with_spacy(self, text: str, missing_fields: List[str]) -> Dict[str, ExtractionResult]:
        """Extract missing fields using SpaCy models"""
        results = {}
        
        for model_name, model_info in self.ai_models.items():
            if not model_name.startswith('spacy_') or model_info['type'] != 'ner':
                continue
            
            try:
                nlp = model_info['model']
                doc = nlp(text[:5000])  # Limit text length for performance
                
                # Extract entities
                persons = [ent.text.strip() for ent in doc.ents if ent.label_ == "PERSON"]
                orgs = [ent.text.strip() for ent in doc.ents if ent.label_ == "ORG"]
                dates = [ent.text.strip() for ent in doc.ents if ent.label_ == "DATE"]
                
                # Map to fields
                if 'judge_name' in missing_fields and persons:
                    # Look for judge in persons
                    for person in persons:
                        if any(title in text.lower() for title in ['justice', 'judge', 'hon']):
                            results['judge_name'] = ExtractionResult(
                                field_name='judge_name',
                                value=person,
                                confidence=0.6,
                                method=f"spacy_{model_name}",
                                source_text=person
                            )
                            break
                
                if 'petitioner_name' in missing_fields and persons:
                    results['petitioner_name'] = ExtractionResult(
                        field_name='petitioner_name',
                        value=persons[0],
                        confidence=0.5,
                        method=f"spacy_{model_name}",
                        source_text=persons[0]
                    )
                
                if 'order_date' in missing_fields and dates:
                    results['order_date'] = ExtractionResult(
                        field_name='order_date',
                        value=dates[0],
                        confidence=0.6,
                        method=f"spacy_{model_name}",
                        source_text=dates[0]
                    )
                
                if 'court_name' in missing_fields and orgs:
                    # Look for court in organizations
                    for org in orgs:
                        if 'court' in org.lower():
                            results['court_name'] = ExtractionResult(
                                field_name='court_name',
                                value=org,
                                confidence=0.6,
                                method=f"spacy_{model_name}",
                                source_text=org
                            )
                            break
                
            except Exception as e:
                self.logger.warning(f"SpaCy extraction failed with {model_name}: {e}")
        
        return results
    
    def extract_with_qa_models(self, text: str, missing_fields: List[str]) -> Dict[str, ExtractionResult]:
        """Extract missing fields using Question-Answering models"""
        results = {}
        
        # Define comprehensive questions for each field - Enhanced for maximum accuracy
        field_questions = {
            # CASE NUMBER - Multiple question variants for better extraction
            'case_number': [
                "What is the case number?",
                "What is the petition number?",
                "What is the bail application number?",
                "What is the writ petition number?",
                "What is the criminal petition number?",
                "What is the appeal number?",
                "What is the application number?",
                "What is the suit number?",
                "What is the civil revision number?",
                "What is the criminal revision number?"
            ],
            
            # ORDER DATE - Comprehensive date extraction
            'order_date': [
                "What is the order date?",
                "When was this order passed?",
                "What is the date of this judgment?",
                "On what date was this order issued?",
                "When was this decision made?",
                "What is the date mentioned in the order?",
                "When was this case decided?",
                "What is the judgment date?",
                "On which date was this order delivered?",
                "When was this ruling given?"
            ],
            
            # JUDGE NAME - Multiple variants for judge identification
            'judge_name': [
                "Who is the judge?",
                "What is the name of the justice?",
                "Who presided over this case?",
                "Which judge heard this case?",
                "Who is the presiding officer?",
                "What is the name of the magistrate?",
                "Who is the judicial officer?",
                "Which justice delivered this judgment?",
                "Who is the Hon'ble judge?",
                "What is the name of the sessions judge?"
            ],
            
            # COURT NAME - Comprehensive court identification
            'court_name': [
                "Which court is this?",
                "What is the name of the court?",
                "In which court was this case heard?",
                "Which judicial forum heard this case?",
                "What is the name of the tribunal?",
                "Which high court is this?",
                "What is the name of the sessions court?",
                "Which district court is this?",
                "What is the complete name of the court?",
                "Which judicial authority handled this case?"
            ],
            
            # PETITIONER/APPLICANT NAME - Comprehensive party identification
            'petitioner_name': [
                "Who is the petitioner?",
                "What is the name of the applicant?",
                "Who filed this petition?",
                "Who is the appellant?",
                "What is the name of the accused?",
                "Who is the complainant?",
                "What is the name of the plaintiff?",
                "Who is the party filing this application?",
                "What is the name of the person seeking relief?",
                "Who is the main party in this case?"
            ],
            
            # RESPONDENT NAME - Opposition party identification
            'respondent_name': [
                "Who is the respondent?",
                "Who is the opposite party?",
                "Against whom is this petition filed?",
                "Who is the defendant?",
                "What is the name of the state?",
                "Who is being challenged in this case?",
                "What is the name of the opposing party?",
                "Who is the party being sued?",
                "Against which authority is this case filed?",
                "Who is the counter party?"
            ],
            
            # PARTY TYPE - Classification questions
            'party_type': [
                "What type of party is the petitioner?",
                "Is the petitioner an individual or organization?",
                "What is the nature of the respondent?",
                "Is this a government party?",
                "What kind of entity is involved?",
                "Is this party a trust or NGO?",
                "What is the legal status of the party?",
                "Is this an individual or institutional party?",
                "What category does this party belong to?",
                "What is the organizational type of the party?"
            ],
            
            # OFFICIAL DESIGNATION - Position and titles
            'official_designation': [
                "What is the official designation?",
                "What is the title of the official?",
                "What position does the party hold?",
                "What is the official capacity?",
                "What is the professional designation?",
                "What office does the person hold?",
                "What is the official rank?",
                "What is the administrative position?",
                "What is the job title mentioned?",
                "What official role is mentioned?"
            ],
            
            # ADDRESS COMPONENTS - Detailed address extraction
            'address_apartment': [
                "What is the house name or apartment mentioned?",
                "What is the building name?",
                "What is the house number?",
                "What is the apartment address?",
                "What is the residential address?",
                "What building or house is mentioned?"
            ],
            
            'address_street': [
                "What is the street address?",
                "What road is mentioned?",
                "What is the street name?",
                "What lane or road is given?",
                "What is the street information?"
            ],
            
            'address_village': [
                "What village is mentioned?",
                "What is the village name?",
                "Which village does the party belong to?",
                "What is the rural address?",
                "What locality is mentioned?"
            ],
            
            'address_city': [
                "What city is mentioned?",
                "What is the city name?",
                "Which city does the party belong to?",
                "What is the urban area mentioned?",
                "What town is given in the address?"
            ],
            
            'address_district': [
                "What district is mentioned?",
                "Which district does the party belong to?",
                "What is the district name?",
                "What administrative district is given?",
                "Which district is mentioned in the address?"
            ],
            
            'address_state': [
                "What state is mentioned?",
                "Which state does the party belong to?",
                "What is the state name?",
                "Which Indian state is mentioned?",
                "What state is given in the address?"
            ],
            
            'address_zipcode': [
                "What is the PIN code?",
                "What is the postal code?",
                "What is the ZIP code mentioned?",
                "What is the pincode?",
                "What postal number is given?"
            ],
            
            # AGE - Age extraction
            'age': [
                "What is the age mentioned?",
                "How old is the person?",
                "What age is given?",
                "What is the person's age?",
                "How many years old?",
                "What age is mentioned in the document?"
            ],
            
            # ALIAS/OTHER NAMES
            'alias': [
                "What alias is mentioned?",
                "What other name is given?",
                "What is the also known as name?",
                "What alternative name is mentioned?",
                "What nickname or other name is given?",
                "What @ symbol name is mentioned?"
            ],
            
            # RELATIONS (Father, Son, etc.)
            'relations': [
                "What family relation is mentioned?",
                "Who is the father mentioned?",
                "What is the son of or daughter of relation?",
                "What family connection is given?",
                "What parental relation is mentioned?",
                "What S/O, D/O, W/O relation is given?"
            ],
            
            # ADVOCATES/COUNSEL - Legal representation
            'advocates': [
                "Who are the advocates?",
                "Who represents the petitioner?",
                "Which lawyers are mentioned?",
                "Who are the counsels in this case?",
                "What are the names of the legal representatives?",
                "Who is the senior counsel?",
                "Which advocates appeared for the parties?",
                "Who is the government pleader?",
                "What legal counsel is mentioned?",
                "Who are the arguing counsel?"
            ],
            
            # CRIME DETAILS - Criminal case information
            'crime_details': [
                "What is the crime described?",
                "What are the allegations?",
                "What criminal activities are mentioned?",
                "What offenses are described?",
                "What criminal charges are mentioned?",
                "What illegal activities are alleged?",
                "What violations are described?",
                "What criminal conduct is mentioned?"
            ],
            
            # LEGAL SECTIONS/STATUTES
            'statutes_offences': [
                "Which sections of law are mentioned?",
                "What statutes are referenced?",
                "Which legal provisions apply to this case?",
                "What IPC sections are mentioned?",
                "Which acts are referred to?",
                "What legal sections are cited?",
                "Which criminal law provisions are mentioned?",
                "What statutory provisions are referenced?"
            ],
            
            # FIR/CRIME NUMBER
            'fir_crime_no': [
                "What is the FIR number?",
                "What is the crime number?",
                "What is the police case number?",
                "What is the first information report number?",
                "What case number is registered with police?",
                "What is the complaint number?"
            ],
            
            # POLICE STATION
            'police_station': [
                "Which police station is mentioned?",
                "What is the name of the police station?",
                "Which PS is referenced?",
                "What police station registered the case?",
                "Which police jurisdiction is mentioned?"
            ],
            
            # JUDGMENT/DECISION - Final outcome
            'judgment': [
                "What is the final judgment?",
                "What did the court conclude?",
                "What is the court's final decision?",
                "What is the outcome of this case?",
                "What ruling did the court give?",
                "What is the court's verdict?",
                "What final order was passed?",
                "What decision was reached?"
            ],
            
            # DECISION - Court's ruling
            'decision': [
                "What is the court's decision?",
                "What did the court decide?",
                "What is the court's ruling?",
                "What determination was made?",
                "What conclusion did the court reach?",
                "What order was passed?",
                "What was the court's finding?"
            ],
            
            # DIRECTIONS - Court instructions
            'directions': [
                "What directions did the court give?",
                "What orders were issued by the court?",
                "What instructions were provided?",
                "What mandates were given?",
                "What directives were issued?",
                "What guidance did the court provide?"
            ],
            
            # DISPOSITION - Final disposal
            'disposition': [
                "How was the case disposed of?",
                "What is the final disposal?",
                "How was the matter concluded?",
                "What was the final outcome?",
                "How was the case resolved?",
                "What is the ultimate disposition?"
            ]
        }
        
        for model_name, model_info in self.ai_models.items():
            if model_info['type'] != 'qa':
                continue
            
            qa_pipeline = model_info['model']
            
            for field in missing_fields:
                if field in field_questions and field not in results:
                    questions = field_questions[field]
                    
                    best_answer = None
                    best_score = 0
                    
                    for question in questions:
                        try:
                            # Use larger context for better accuracy (increased from 2000)
                            context = text[:4000] if 'legal' in model_name.lower() else text[:3000]
                            answer = qa_pipeline(question=question, context=context)
                            
                            if isinstance(answer, list):
                                answer = answer[0] if answer else {'answer': '', 'score': 0}
                            
                            if answer['score'] > best_score and answer['score'] > model_info['confidence_threshold']:
                                best_answer = answer
                                best_score = answer['score']
                        
                        except Exception as e:
                            self.logger.warning(f"QA failed for {question} with {model_name}: {e}")
                            continue
                    
                    if best_answer and best_score > model_info['confidence_threshold']:
                        results[field] = ExtractionResult(
                            field_name=field,
                            value=best_answer['answer'].strip(),
                            confidence=best_score,
                            method=f"qa_{model_name}",
                            source_text=best_answer.get('context', '')[:100]
                        )
        
        return results
    
    def extract_with_ner_models(self, text: str, missing_fields: List[str]) -> Dict[str, ExtractionResult]:
        """Extract missing fields using NER models"""
        results = {}
        
        for model_name, model_info in self.ai_models.items():
            if model_info['type'] != 'ner' or model_name.startswith('spacy_'):
                continue
            
            try:
                if model_name == 'nltk_ner':
                    # NLTK NER
                    if AI_MODULES.get('nltk'):
                        sentences = sent_tokenize(text[:3000])
                        entities = []
                        
                        for sentence in sentences[:5]:  # Limit sentences
                            tokens = word_tokenize(sentence)
                            pos_tags = pos_tag(tokens)
                            chunks = ne_chunk(pos_tags)
                            
                            for chunk in chunks:
                                if isinstance(chunk, Tree):
                                    entity_name = ' '.join([token for token, pos in chunk.leaves()])
                                    entity_type = chunk.label()
                                    entities.append((entity_name, entity_type))
                        
                        # Map entities to fields
                        for entity_name, entity_type in entities:
                            if entity_type == 'PERSON' and 'judge_name' in missing_fields:
                                if 'justice' in text.lower() or 'judge' in text.lower():
                                    results['judge_name'] = ExtractionResult(
                                        field_name='judge_name',
                                        value=entity_name,
                                        confidence=0.5,
                                        method="nltk_ner",
                                        source_text=entity_name
                                    )
                
                else:
                    # Transformer NER
                    ner_pipeline = model_info['model']
                    entities = ner_pipeline(text[:2000])  # Limit text length
                    
                    for entity in entities:
                        if entity['score'] < model_info['confidence_threshold']:
                            continue
                        
                        entity_text = entity['word'].replace('##', '').strip()
                        entity_type = entity['entity_group'] if 'entity_group' in entity else entity['entity']
                        
                        # Map entities to fields
                        if entity_type in ['PERSON', 'PER'] and 'petitioner_name' in missing_fields:
                            results['petitioner_name'] = ExtractionResult(
                                field_name='petitioner_name',
                                value=entity_text,
                                confidence=entity['score'],
                                method=f"ner_{model_name}",
                                source_text=entity_text
                            )
                        
                        elif entity_type in ['ORG', 'ORGANIZATION'] and 'court_name' in missing_fields:
                            if 'court' in entity_text.lower():
                                results['court_name'] = ExtractionResult(
                                    field_name='court_name',
                                    value=entity_text,
                                    confidence=entity['score'],
                                    method=f"ner_{model_name}",
                                    source_text=entity_text
                                )
            
            except Exception as e:
                self.logger.warning(f"NER extraction failed with {model_name}: {e}")
        
        return results
    
    def extract_with_date_parser(self, text: str, missing_fields: List[str]) -> Dict[str, ExtractionResult]:
        """Extract dates using dateparser library"""
        results = {}
        
        if 'order_date' not in missing_fields or not AI_MODULES.get('dateparser'):
            return results
        
        try:
            if AI_MODULES.get('dateparser'):
                import dateparser
                
                # Look for date patterns in text
                date_patterns = [
                    r'\b\d{1,2}(?:st|nd|rd|th)?\s+(?:day\s+of\s+)?\w+,?\s+\d{4}\b',
                    r'\b\d{1,2}[-/\.]\d{1,2}[-/\.]\d{4}\b',
                    r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b'
                ]
                
                for pattern in date_patterns:
                    matches = re.finditer(pattern, text, re.IGNORECASE)
                    for match in matches:
                        date_text = match.group(0)
                        parsed_date = dateparser.parse(date_text)
                        
                        if parsed_date:
                            results['order_date'] = ExtractionResult(
                                field_name='order_date',
                                value=parsed_date.strftime('%Y-%m-%d'),
                                confidence=0.7,
                                method="dateparser",
                                source_text=date_text
                            )
                            break
                    
                    if 'order_date' in results:
                        break
        
        except Exception as e:
            self.logger.warning(f"Date parsing failed: {e}")
        
        return results
    
    def extract_with_legal_models(self, text: str, missing_fields: List[str]) -> Dict[str, ExtractionResult]:
        """Extract missing fields using specialized legal models"""
        results = {}
        
        # Legal-specific field questions
        legal_questions = {
            'advocates': [
                "Who are the advocates representing the parties?",
                "Which lawyers are mentioned in this case?",
                "Who represents the petitioner and respondent?"
            ],
            'crime_details': [
                "What criminal activities are described?",
                "What are the charges mentioned?",
                "What offenses are listed in this case?"
            ],
            'judgment': [
                "What is the final judgment of the court?",
                "What did the court rule in this matter?",
                "What is the court's decision and reasoning?"
            ],
            'statutes_offences': [
                "Which sections of law are mentioned?",
                "What statutes are referenced?",
                "Which legal provisions apply to this case?"
            ],
            'directions': [
                "What directions did the court give?",
                "What orders were issued by the court?",
                "What instructions were provided?"
            ]
        }
        
        # Use legal QA models for these fields
        for model_name, model_info in self.ai_models.items():
            if 'legal' in model_name and model_info['type'] == 'qa':
                qa_pipeline = model_info['model']
                
                for field in missing_fields:
                    if field in legal_questions and field not in results:
                        questions = legal_questions[field]
                        
                        best_answer = None
                        best_score = 0
                        
                        for question in questions:
                            try:
                                # Use larger context for legal documents
                                context = text[:3000]  # Increased from 2000
                                answer = qa_pipeline(question=question, context=context)
                                
                                if isinstance(answer, list):
                                    answer = answer[0] if answer else {'answer': '', 'score': 0}
                                
                                if answer['score'] > best_score and answer['score'] > model_info['confidence_threshold']:
                                    best_answer = answer
                                    best_score = answer['score']
                            
                            except Exception as e:
                                self.logger.warning(f"Legal QA failed for {question}: {e}")
                                continue
                        
                        if best_answer and best_score > model_info['confidence_threshold']:
                            results[field] = ExtractionResult(
                                field_name=field,
                                value=best_answer['answer'].strip(),
                                confidence=best_score,
                                method=f"legal_qa_{model_name}",
                                source_text=best_answer.get('context', '')[:100]
                            )
                            self.logger.info(f"   🏛️ Legal model found {field}: {best_answer['answer'][:50]}...")
        
        return results
    
    def format_structured_output(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Format extraction results in a clean, structured format"""
        extracted_data = results.get('extracted_data', {})
        
        # Helper function to clean and format dates
        def format_date(date_str):
            if not date_str:
                return ""
            # Convert "2nd day of February, 2024" to "02-02-2024"
            try:
                import re
                # Handle specific patterns
                if "day of" in date_str.lower():
                    # Pattern: "2nd day of February, 2024"
                    pattern = r'(\d{1,2})(?:st|nd|rd|th)?\s+day\s+of\s+(\w+),?\s+(\d{4})'
                    match = re.search(pattern, date_str, re.IGNORECASE)
                    if match:
                        day, month_name, year = match.groups()
                        month_map = {
                            'january': '01', 'february': '02', 'march': '03', 'april': '04',
                            'may': '05', 'june': '06', 'july': '07', 'august': '08',
                            'september': '09', 'october': '10', 'november': '11', 'december': '12'
                        }
                        month = month_map.get(month_name.lower(), '01')
                        return f"{year}-{month}-{day.zfill(2)}"
                
                # Try dateparser as fallback
                if AI_MODULES.get('dateparser'):
                    import dateparser
                    parsed_date = dateparser.parse(date_str)
                    if parsed_date:
                        return parsed_date.strftime("%d-%m-%Y")
                return date_str
            except Exception as e:
                return date_str
        
        # Helper function to extract value from field
        def get_field_value(field_name, default="Not found"):
            field_data = extracted_data.get(field_name, {})
            if isinstance(field_data, dict):
                value = field_data.get('value', '')
                return value if value else default
            return field_data if field_data else default
        
        # Helper function to get petitioner details
        def get_petitioner_details():
            petitioner_details = get_field_value('petitioner_details')
            if isinstance(petitioner_details, dict):
                address_info = petitioner_details.get('address', {})
                return {
                    "type": get_field_value('party_type', 'individual'),
                    "role": "petitioner",
                    "name": get_field_value('petitioner_name'),
                    "age": int(get_field_value('age', 0)) if str(get_field_value('age', '')).isdigit() else "Not found",
                    "father_name": get_field_value('relations', '').replace('S/O ', '').replace('s/o ', '') if get_field_value('relations') != "Not found" else "Not found",
                    "address": {
                        "house_name": get_field_value('apartment_house'),
                        "street": get_field_value('street'),
                        "village": get_field_value('village'),
                        "district": get_field_value('district'),
                        "state": results.get('detected_state', 'Not found'),
                        "pincode": get_field_value('zipcode')
                    }
                }
            else:
                return {
                    "type": get_field_value('party_type', 'individual'),
                    "role": "petitioner",
                    "name": get_field_value('petitioner_name'),
                    "age": int(get_field_value('age', 0)) if str(get_field_value('age', '')).isdigit() else "Not found",
                    "father_name": get_field_value('relations'),
                    "address": {
                        "house_name": get_field_value('apartment_house'),
                        "street": get_field_value('street'),
                        "village": get_field_value('village'),
                        "district": get_field_value('district'),
                        "state": results.get('detected_state', 'Not found'),
                        "pincode": get_field_value('zipcode')
                    }
                }
        
        # Helper function to get respondent details
        def get_respondents():
            respondents = []
            respondent_name = get_field_value('respondent_name')
            
            if respondent_name != "Not found" and 'STATE OF' in respondent_name.upper():
                # Get state from detected state or respondent name
                state_name = results.get('detected_state', 'Not found')
                if state_name == "Not found" and 'STATE OF' in respondent_name:
                    state_name = respondent_name.replace('STATE OF', '').strip().title()
                
                respondents.append({
                    "type": "government",
                    "role": "respondent",
                    "name": respondent_name,
                    "representative": f"Public Prosecutor, High Court of {state_name}" if state_name != "Not found" else "Not found",
                    "address": {
                        "district": get_field_value('district'),
                        "state": state_name,
                        "pincode": get_field_value('zipcode')
                    }
                })
            
            # Add police station if mentioned
            police_station = get_field_value('police_station')
            if police_station != "Not found":
                respondents.append({
                    "type": "government",
                    "role": "respondent",
                    "name": f"Station House Officer, {police_station} Police Station",
                    "designation": f"{police_station} Police Station",
                    "address": {
                        "district": get_field_value('district'),
                        "state": results.get('detected_state', 'Not found'),
                        "pincode": get_field_value('zipcode')
                    }
                })
            
            return respondents
        
        # Helper function to extract sections and acts
        def get_acts_sections():
            acts_sections = []
            
            # First try to get from extracted data
            sections = get_field_value('sections')
            acts = get_field_value('acts')
            statutes = get_field_value('statutes')
            
            # If we have structured section/act data, use it
            if sections or acts:
                if isinstance(sections, list):
                    for section in sections:
                        acts_sections.append(section)
                elif sections:
                    acts_sections.append(sections)
                    
                if isinstance(acts, list):
                    for act in acts:
                        acts_sections.append(act)
                elif acts:
                    acts_sections.append(acts)
            
            # If we have statutes data, use it
            if statutes:
                if isinstance(statutes, list):
                    acts_sections.extend(statutes)
                else:
                    acts_sections.append(statutes)
            
            # If no structured data, extract from raw text
            if not acts_sections:
                text = results.get('raw_text', '')
                
                # Common patterns for sections
                section_patterns = [
                    r'Section\s+(\d+[a-z]*(?:\([a-z0-9]+\))?)\s+of\s+the\s+([^,\n.]+)',
                    r'under\s+Section\s+(\d+[a-z]*(?:\([a-z0-9]+\))?)\s+of\s+the\s+([^,\n.]+)',
                    r'offences\s+punishable\s+under\s+Section\s+(\d+[a-z]*)\s+of\s+the\s+([^,\n.]+)',
                ]
                
                for pattern in section_patterns:
                    matches = re.findall(pattern, text, re.IGNORECASE)
                    for match in matches:
                        if len(match) == 2:
                            section_num, act_name = match
                            # Clean up act name
                            act_name = act_name.strip()
                            if act_name.endswith('and'):
                                act_name = act_name[:-3].strip()
                            acts_sections.append(f"Section {section_num} {act_name}")
            
            # Remove duplicates while preserving order
            seen = set()
            unique_acts = []
            for act in acts_sections:
                if act not in seen:
                    seen.add(act)
                    unique_acts.append(act)
            
            return unique_acts if unique_acts else []
        
        # Detect document type from the text
        def detect_document_type():
            text = results.get('raw_text', '').lower() if results.get('raw_text') else ""
            
            if 'writ petition' in text or 'w.p(c)' in text or 'wp(c)' in text:
                if 'judgment' in text:
                    return "Writ petition (civil) judgment"
                else:
                    return "Writ Petition (Civil)"
            elif 'bail application' in text or 'b.a.' in text or 'anticipatory bail' in text:
                return "Anticipatory bail order (Section 438 CrPC)"
            elif 'criminal petition' in text or 'crl.p' in text:
                return "Criminal Petition"
            elif 'civil revision' in text or 'c.r.p' in text:
                return "Civil Revision Petition"
            elif 'appeal' in text:
                return "Appeal"
            else:
                return "Court Order"
        
        # Get document type
        doc_type = detect_document_type()
        
        # Determine case prefix based on actual case number extracted
        extracted_case_number = get_field_value('case_number')
        if extracted_case_number != "Not found":
            case_prefix = ""  # Use extracted as-is
        elif 'writ petition' in doc_type.lower():
            case_prefix = "W.P(C) No."
        elif 'bail' in doc_type.lower():
            case_prefix = "B.A. No."
        elif 'criminal reference' in doc_type.lower():
            case_prefix = "CRIMINAL REFERENCE No."
        else:
            case_prefix = "Not found"
        
        # Get statutes based on document type and extracted data
        def get_statutes_for_doc_type(doc_type):
            # First try to get from extracted data
            extracted_statutes = get_acts_sections()
            if extracted_statutes:
                return extracted_statutes
            
            # Fallback based on document type if no extraction
            if 'writ petition' in doc_type.lower():
                return [
                    "Article 226 Constitution of India",
                    "Article 227 Constitution of India"
                ]
            elif 'bail' in doc_type.lower():
                return [
                    "Section 438 Code of Criminal Procedure, 1973"
                ]
            else:
                return []
        
        # Extract and format case number properly
        def format_case_number():
            case_num = get_field_value('case_number')
            if case_num == "Not found":
                return "Not found", "Not found"
            
            # Try to extract case number from the text more accurately
            import re
            raw_text = results.get('raw_text', '')
            
            # Look for W.P(C) patterns first
            writ_match = re.search(r'W\.P\(C\)\s*(?:NO\.?)?\s*(\d+)\/(\d{2,4})', raw_text, re.IGNORECASE)
            if writ_match:
                case_no, year = writ_match.groups()
                if len(year) == 2:
                    year = "20" + year
                case_number = f"W.P.(C) No. {case_no} of {year}"
                alternate = f"{case_no}/{year}"
                return case_number, alternate
            
            # Look for standard WP(C) patterns
            writ_match2 = re.search(r'WP\(C\)\s*(?:NO\.?)?\s*(\d+)\s*OF\s*(\d{4})', raw_text, re.IGNORECASE)
            if writ_match2:
                case_no, year = writ_match2.groups()
                case_number = f"W.P.(C) No. {case_no} of {year}"
                alternate = f"{case_no}/{year}"
                return case_number, alternate
            
            # Fallback for other cases
            if case_prefix != "Not found":
                return f"{case_prefix} {case_num} of 2024", case_num
            else:
                return case_num, case_num
        
        case_number, alternate_case_number = format_case_number()
        
        # Get dynamic court name based on detected state
        def get_court_name():
            detected_state = results.get('detected_state', 'Not found')
            court_name = get_field_value('court_name')
            
            if court_name != "Not found":
                return court_name
            elif detected_state == 'Kerala':
                return "High Court of Kerala at Ernakulam"
            elif detected_state == 'Uttar Pradesh':
                return "High Court of Judicature at Allahabad"
            elif detected_state == 'Delhi':
                return "High Court of Delhi"
            elif detected_state == 'Maharashtra':
                return "Bombay High Court"
            elif detected_state == 'Gujarat':
                return "High Court of Gujarat"
            elif detected_state == 'Karnataka':
                return "High Court of Karnataka"
            elif detected_state == 'Tamil Nadu':
                return "Madras High Court"
            elif detected_state == 'Arunachal Pradesh':
                return "Gauhati High Court at Naharlagun"
            elif detected_state != "Not found":
                return f"High Court of {detected_state}"
            else:
                return "Not found"
        
        # Determine bench type dynamically
        def get_bench_type():
            bench_info = get_field_value('bench', get_field_value('bench_type'))
            if bench_info != "Not found":
                return bench_info
            
            # Try to detect from judge names
            judge_names = get_field_value('judge_name')
            if judge_names != "Not found":
                if isinstance(judge_names, list):
                    if len(judge_names) > 1:
                        return "Division Bench"
                    else:
                        return "Single Judge"
                elif judge_names and (',' in judge_names or ' and ' in judge_names.lower()):
                    return "Division Bench"
                else:
                    return "Single Judge"
            else:
                return "Not found"
        
        # Format the main structure - Enhanced professional version
        structured_output = {
            "court_name": get_court_name(),
            "case_number": case_number,
            "alternate_case_number": alternate_case_number,
            "crime_number": None,  # Default to null, will be updated for criminal cases
            "order_date": format_date(get_field_value('order_date')),
            "judge_name": get_field_value('judge_name'),
            "bench": get_bench_type(),
            "document_type": doc_type,
            "statutes_sections": get_statutes_for_doc_type(doc_type),
            "parties": self._format_professional_parties(results, doc_type)
        }
        
        # Add crime number only for criminal cases (bail applications, criminal petitions)
        if 'bail' in doc_type.lower() or 'criminal' in doc_type.lower():
            crime_no = get_field_value('fir_crime_no', get_field_value('crime_number'))
            police_station = get_field_value('police_station')
            district = get_field_value('district')
            
            if crime_no != "Not found" and police_station != "Not found":
                structured_output["crime_number"] = f"Crime No. {crime_no}, {police_station} Police Station"
                if district != "Not found":
                    structured_output["crime_number"] += f", {district}"
            elif crime_no != "Not found":
                structured_output["crime_number"] = f"Crime No. {crime_no}"
            else:
                structured_output["crime_number"] = "Not found"
        
        # Add production summary if available
        if 'production_summary' in results:
            structured_output['summary'] = results['production_summary']
        
        return structured_output
    
    def extract_metadata_with_llama(self, text):
        """
        Multi-stage metadata extraction: State Detection → Regex → LLaMA → Other Models
        """
        print("🚀 Starting multi-stage metadata extraction...")
        
        # Stage 0: State Detection
        print("🗺️ Stage 0: Detecting state/jurisdiction...")
        detected_state = detect_state_from_text(text)
        print(f"   Detected state: {detected_state}")
        
        # Stage 1: Regex Extraction using State Patterns
        print("🔍 Stage 1: Regex extraction using state-specific patterns...")
        regex_results = self.extract_with_patterns(text, detected_state)
        print(f"   Regex extracted: {len(regex_results)} fields")
        
        # Identify missing fields
        missing_fields = [field for field in self.extraction_fields if field not in regex_results]
        print(f"   Missing after regex: {missing_fields}")
        
        all_results = regex_results.copy()
        
        # Stage 2: LLaMA Extraction for missing fields
        if missing_fields and AI_MODULES['llama']:
            print(f"🦙 Stage 2: LLaMA extraction for {len(missing_fields)} missing fields...")
            try:
                llm = OllamaLLM(
                    model="llama3.1:8b",
                    temperature=0.1,
                    timeout=300
                )
                
                # Create focused prompt for missing fields only
                missing_fields_str = ", ".join(missing_fields)
                
                prompt = f"""
                You are a legal document expert. Extract ONLY the following missing information from this legal document.
                Return a JSON object with these specific fields. If a field is not found, use "Not found".
                
                Missing fields to extract: {missing_fields_str}
                
                Document text:
                {text[:8000]}
                
                Return only valid JSON with the requested fields:
                """
                
                llama_response = llm.invoke(prompt)
                
                # Parse LLaMA response
                try:
                    json_match = re.search(r'\{.*\}', llama_response, re.DOTALL)
                    if json_match:
                        llama_data = json.loads(json_match.group())
                    else:
                        llama_data = json.loads(llama_response)
                    
                    # Convert LLaMA results to ExtractionResult format
                    llama_count = 0
                    for field in missing_fields:
                        if field in llama_data and llama_data[field] and llama_data[field] != "Not found":
                            all_results[field] = ExtractionResult(
                                field_name=field,
                                value=llama_data[field],
                                confidence=0.7,
                                method="llama",
                                source_text=llama_data[field][:100]
                            )
                            llama_count += 1
                    
                    print(f"   LLaMA extracted: {llama_count} additional fields")
                    
                except json.JSONDecodeError:
                    print(f"   ⚠️ Could not parse LLaMA JSON response")
                    
            except Exception as e:
                print(f"   ❌ LLaMA extraction error: {e}")
        
        # Update missing fields after LLaMA
        missing_fields = [field for field in self.extraction_fields if field not in all_results]
        
        # Stage 3: Other Models for remaining missing fields
        if missing_fields:
            print(f"🧠 Stage 3: Other models for {len(missing_fields)} remaining missing fields...")
            
            # 3a. SpaCy NER
            if missing_fields:
                print(f"   🔍 Trying SpaCy for: {missing_fields[:5]}...")
                spacy_results = self.extract_with_spacy(text, missing_fields)
                spacy_count = 0
                for field, result in spacy_results.items():
                    if field not in all_results:
                        all_results[field] = result
                        spacy_count += 1
                        print(f"      ✅ SpaCy found {field}: {result.value[:50]}...")
                if spacy_count > 0:
                    print(f"   SpaCy extracted: {spacy_count} additional fields")
                else:
                    print(f"   SpaCy extracted: 0 additional fields")
                
                # Update missing fields after SpaCy
                missing_fields = [field for field in self.extraction_fields if field not in all_results]
            
            # 3b. Question-Answering models
            if missing_fields:
                print(f"   🤔 Trying QA Models for: {missing_fields[:5]}...")
                qa_results = self.extract_with_qa_models(text, missing_fields)
                qa_count = 0
                for field, result in qa_results.items():
                    if field not in all_results:
                        all_results[field] = result
                        qa_count += 1
                        print(f"      ✅ QA found {field}: {result.value[:50]}...")
                if qa_count > 0:
                    print(f"   QA Models extracted: {qa_count} additional fields")
                else:
                    print(f"   QA Models extracted: 0 additional fields")
                
                # Update missing fields after QA
                missing_fields = [field for field in self.extraction_fields if field not in all_results]
            
            # 3c. NER models
            if missing_fields:
                print(f"   🏷️ Trying NER Models for: {missing_fields[:5]}...")
                ner_results = self.extract_with_ner_models(text, missing_fields)
                ner_count = 0
                for field, result in ner_results.items():
                    if field not in all_results:
                        all_results[field] = result
                        ner_count += 1
                        print(f"      ✅ NER found {field}: {result.value[:50]}...")
                if ner_count > 0:
                    print(f"   NER Models extracted: {ner_count} additional fields")
                else:
                    print(f"   NER Models extracted: 0 additional fields")
            
            # Final missing count
            final_missing = [field for field in self.extraction_fields if field not in all_results]
            if final_missing:
                print(f"   Still missing: {len(final_missing)} fields - {final_missing[:3]}...")
            else:
                print(f"   🎉 All fields extracted successfully!")
        
        # Final results compilation
        final_results = {
            'detected_state': detected_state,
            'extraction_summary': {
                'total_fields': len(self.extraction_fields),
                'extracted_fields': len(all_results),
                'missing_fields': len(self.extraction_fields) - len(all_results),
                'extraction_methods': list(set([result.method for result in all_results.values()]))
            },
            'extracted_data': {},
            'metadata': {
                'text_length': len(text),
                'processing_timestamp': datetime.now().isoformat()
            },
            'raw_text': text
        }
        
        # Convert results to dictionary format
        for field, result in all_results.items():
            final_results['extracted_data'][field] = {
                'value': result.value,
                'confidence': result.confidence,
                'method': result.method,
                'source_text': result.source_text[:100] + "..." if len(result.source_text) > 100 else result.source_text
            }
        
        print(f"✅ Multi-stage extraction completed!")
        print(f"📊 Final results: {len(all_results)}/{len(self.extraction_fields)} fields extracted")
        
        # Debug: Show what was extracted
        print(f"📋 Extraction breakdown:")
        regex_fields = [field for field, result in all_results.items() if 'regex' in result.method]
        llama_fields = [field for field, result in all_results.items() if 'llama' in result.method]
        other_fields = [field for field, result in all_results.items() if 'regex' not in result.method and 'llama' not in result.method]
        
        if regex_fields:
            print(f"   🔍 Regex: {regex_fields}")
        if llama_fields:
            print(f"   🦙 LLaMA: {llama_fields}")
        if other_fields:
            print(f"   🧠 Other: {other_fields}")
        
        formatted_output = self.format_structured_output(final_results)
        print(f"📄 Structured output created successfully")
        return formatted_output
    
    def _get_enhanced_statutes(self) -> List[str]:
        """Get enhanced statutes sections in professional format"""
        # This should be called with document type context and extraction results
        # Return empty list as statutes should come from extraction results
        return []
    
    def _format_professional_parties(self, results: Dict[str, Any], doc_type: str = "") -> List[Dict]:
        """Format parties in professional structure based on document type"""
        extracted_data = results.get('extracted_data', {})
        parties = []
        
        # Helper function to get field value
        def get_field_value(field_name, default="Not found"):
            field_data = extracted_data.get(field_name, {})
            if isinstance(field_data, dict):
                value = field_data.get('value', '')
                return value if value else default
            return field_data if field_data else default
        
        # Check if this is a writ petition - different party structure
        if 'writ petition' in doc_type.lower():
            # For writ petitions - usually institutions vs government
            petitioner_name = get_field_value('petitioner_name', 'Petitioner')
            
            # Determine party type based on name or extracted data
            def get_party_type(name):
                extracted_type = get_field_value('party_type')
                if extracted_type != "Not found":
                    return extracted_type
                    
                if name == "Not found":
                    return "Not found"
                    
                name_lower = name.lower()
                if 'trust' in name_lower:
                    return "trust"
                elif 'college' in name_lower or 'school' in name_lower or 'university' in name_lower:
                    return "educational_institution" 
                elif 'company' in name_lower or 'corporation' in name_lower or 'ltd' in name_lower:
                    return "company"
                else:
                    return "institution"
            
            # Extract petitioner counsels from extracted data or text
            counsels = []
            extracted_counsels = get_field_value('petitioner_counsels')
            if extracted_counsels != "Not found":
                if isinstance(extracted_counsels, list):
                    counsels = extracted_counsels
                else:
                    counsels = [extracted_counsels]
            else:
                counsels = ["Not found"]
            
            parties.append({
                "role": "petitioner",
                "party_type": get_party_type(petitioner_name),
                "name": petitioner_name,
                "official_designation": get_field_value('official_designation', 'Petitioner'),
                "address": {
                    "apartment_house": get_field_value('apartment_house'),
                    "street": get_field_value('street'),
                    "village": get_field_value('village'),
                    "post_office": get_field_value('post_office'),
                    "city": get_field_value('city'),
                    "district": get_field_value('district'),
                    "state": results.get('detected_state', 'Not found'),
                    "zipcode": get_field_value('zipcode')
                },
                "age": int(get_field_value('age', 0)) if str(get_field_value('age', '')).isdigit() else "Not found",
                "alias": get_field_value('alias', "Not found"),
                "relations": get_field_value('relations'),
                "other_details": "Not found",
                "counsels": counsels
            })
            
            # Add respondents based on extracted data
            respondent_name = get_field_value('respondent_name', 'Respondent')
            respondent_counsels = []
            extracted_resp_counsels = get_field_value('respondent_counsels')
            if extracted_resp_counsels != "Not found":
                if isinstance(extracted_resp_counsels, list):
                    respondent_counsels = extracted_resp_counsels
                else:
                    respondent_counsels = [extracted_resp_counsels]
            else:
                respondent_counsels = ["Not found"]
            
            if respondent_name != "Not found" and ('union of india' in respondent_name.lower() or 'government' in respondent_name.lower()):
                parties.append({
                    "role": "respondent",
                    "party_type": "government",
                    "name": respondent_name,
                    "official_designation": get_field_value('respondent_official_designation', 'Government Representative'),
                    "address": {
                        "apartment_house": "Not found",
                        "street": get_field_value('respondent_street', "Not found"),
                        "village": "Not found",
                        "city": get_field_value('respondent_city', 'New Delhi'),
                        "district": get_field_value('respondent_district', 'New Delhi'),
                        "state": get_field_value('respondent_state', 'Delhi'),
                        "zipcode": get_field_value('respondent_zipcode')
                    },
                    "age": "Not found",
                    "alias": "Not found",
                    "relations": "Not found",
                    "counsels": respondent_counsels
                })
            
            # Add additional respondents if found
            additional_respondents = get_field_value('additional_respondents')
            if additional_respondents != "Not found":
                if isinstance(additional_respondents, list):
                    for resp in additional_respondents:
                        parties.append({
                            "role": "respondent",
                            "party_type": get_field_value('additional_respondent_type', 'statutory_body'),
                            "name": resp.get('name', resp) if isinstance(resp, dict) else resp,
                            "official_designation": resp.get('designation', 'Not found') if isinstance(resp, dict) else 'Not found',
                            "address": resp.get('address', {"apartment_house": "Not found", "street": "Not found", "village": "Not found", "city": "Not found", "district": "Not found", "state": "Not found", "zipcode": "Not found"}) if isinstance(resp, dict) else {"apartment_house": "Not found", "street": "Not found", "village": "Not found", "city": "Not found", "district": "Not found", "state": "Not found", "zipcode": "Not found"},
                            "age": "Not found",
                            "alias": "Not found",
                            "relations": "Not found",
                            "counsels": resp.get('counsels', ["Not found"]) if isinstance(resp, dict) else ["Not found"]
                        })
            
            return parties
        
        # For criminal cases (bail applications) - individuals vs state
        petitioner_details = get_field_value('petitioner_details')
        
        # Get petitioner counsels
        petitioner_counsels = []
        extracted_pet_counsels = get_field_value('petitioner_counsels')
        if extracted_pet_counsels != "Not found":
            if isinstance(extracted_pet_counsels, list):
                petitioner_counsels = extracted_pet_counsels
            else:
                petitioner_counsels = [extracted_pet_counsels]
        else:
            petitioner_counsels = ["Not found"]
        
        if isinstance(petitioner_details, dict):
            address_info = petitioner_details.get('address', {})
            parties.append({
                "role": "petitioner",
                "party_type": get_field_value('party_type', 'individual'),
                "name": get_field_value('petitioner_name'),
                "official_designation": get_field_value('official_designation', 'Petitioner'),
                "address": {
                    "apartment_house": get_field_value('apartment_house'),
                    "street": get_field_value('street'),
                    "village": get_field_value('village'),
                    "post_office": get_field_value('post_office'),
                    "city": get_field_value('city'),
                    "district": get_field_value('district'),
                    "state": results.get('detected_state', 'Not found'),
                    "zipcode": get_field_value('zipcode')
                },
                "age": int(get_field_value('age', 0)) if str(get_field_value('age', '')).isdigit() else "Not found",
                "alias": get_field_value('alias', "Not found"),
                "relations": get_field_value('relations'),
                "other_details": "Not found",
                "counsels": petitioner_counsels
            })
        else:
            # Fallback if detailed petitioner info not available
            parties.append({
                "role": "petitioner",
                "party_type": get_field_value('party_type', 'individual'),
                "name": get_field_value('petitioner_name'),
                "official_designation": get_field_value('official_designation', 'Petitioner'),
                "address": {
                    "apartment_house": get_field_value('apartment_house'),
                    "street": get_field_value('street'),
                    "village": get_field_value('village'),
                    "post_office": get_field_value('post_office'),
                    "city": get_field_value('city'),
                    "district": get_field_value('district'),
                    "state": results.get('detected_state', 'Not found'),
                    "zipcode": get_field_value('zipcode')
                },
                "age": int(get_field_value('age', 0)) if str(get_field_value('age', '')).isdigit() else "Not found",
                "alias": get_field_value('alias', "Not found"),
                "relations": get_field_value('relations'),
                "other_details": "Not found",
                "counsels": petitioner_counsels
            })
        
        # State respondent
        state_name = results.get('detected_state', 'Not found')
        state_counsels = []
        extracted_state_counsels = get_field_value('state_counsels')
        if extracted_state_counsels != "Not found":
            if isinstance(extracted_state_counsels, list):
                state_counsels = extracted_state_counsels
            else:
                state_counsels = [extracted_state_counsels]
        else:
            state_counsels = ["Not found"]
        
        parties.append({
            "role": "respondent",
            "party_type": "government",
            "name": f"State of {state_name}" if state_name != "Not found" else "Not found",
            "official_designation": f"Represented by Public Prosecutor, High Court of {state_name}" if state_name != "Not found" else "Not found",
            "address": {
                "apartment_house": "Not found",
                "street": "Not found",
                "village": "Not found",
                "city": get_field_value('district', get_field_value('city')),
                "district": get_field_value('district'),
                "state": results.get('detected_state', 'Not found'),
                "zipcode": get_field_value('zipcode')
            },
            "age": "Not found",
            "alias": "Not found",
            "relations": "Not found",
            "counsels": state_counsels
        })
        
        # Police Station
        police_station = get_field_value('police_station')
        if police_station != "Not found":
            parties.append({
                "role": "respondent",
                "party_type": "police_station",
                "name": f"Station House Officer, {police_station} Police Station",
                "official_designation": "Station House Officer",
                "address": {
                    "apartment_house": "Not found",
                    "street": "Not found",
                    "village": "Not found",
                    "city": get_field_value('city', police_station),
                    "district": get_field_value('district'),
                    "state": results.get('detected_state', 'Not found'),
                    "zipcode": get_field_value('zipcode')
                },
                "age": "Not found",
                "alias": "Not found",
                "relations": "Not found",
                "counsels": ["Not found"]
            })
        
        return parties
    
    def format_output(self, results: Dict[str, Any]) -> str:
        """Format extraction results for display - Clean version"""
        # Get the clean structured output
        structured_data = self.format_structured_output(results)
        
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
                    address_parts.append(addr['apartment_house'])
                if addr.get('village'):
                    address_parts.append(addr['village'])
                if addr.get('district'):
                    address_parts.append(addr['district'])
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
        
        # Add Production Summary if available
        if 'production_summary' in results:
            output += "\n📄 Production Summary:\n"
            output += "=" * 60 + "\n"
            output += results['production_summary']
            output += "\n" + "=" * 60 + "\n"
        
        output += "\n" + "=" * 50 + "\n"
        
        return output
    
    def save_results(self, results: Dict[str, Any], output_dir: str, filename_prefix: str, raw_text: str = None):
        """Save extraction results and raw text in organized folder structure"""
        
        # Create main output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Create subdirectory for this specific file
        file_output_dir = os.path.join(output_dir, filename_prefix)
        os.makedirs(file_output_dir, exist_ok=True)
        
        # Save formatted text output
        text_output = self.format_output(results)
        text_file = os.path.join(file_output_dir, "extraction_report.txt")
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(text_output)
        
        # Save ONLY the clean structured output (remove old technical JSON)
        structured_output = self.format_structured_output(results)
        json_file = os.path.join(file_output_dir, f"{filename_prefix}.json")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(structured_output, f, indent=2, ensure_ascii=False)
        
        # Save raw extracted text if provided
        raw_text_file = None
        if raw_text:
            raw_text_file = os.path.join(file_output_dir, f"{filename_prefix}_original_text.txt")
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
            
            self.logger.info(f"💾 Original text saved to: {raw_text_file}")
        
        self.logger.info(f"� All files saved in folder: {file_output_dir}")
        self.logger.info(f"📄 Clean extraction report: {text_file}")
        self.logger.info(f"📋 Structured JSON data: {json_file}")
        
        return text_file, json_file, raw_text_file, file_output_dir
    
    def process_multiple_pdfs(self, pdf_directory: str, output_dir: str = "output"):
        """
        Process multiple PDF files from a directory
        
        Args:
            pdf_directory: Directory containing PDF files
            output_dir: Base output directory
        """
        import glob
        
        # Find all PDF files
        pdf_pattern = os.path.join(pdf_directory, "*.pdf")
        pdf_files = glob.glob(pdf_pattern)
        
        if not pdf_files:
            self.logger.error(f"❌ No PDF files found in: {pdf_directory}")
            return []
        
        self.logger.info(f"📁 Found {len(pdf_files)} PDF files to process")
        self.logger.info(f"💾 Base output directory: {output_dir}")
        self.logger.info("=" * 60)
        
        results = []
        success_count = 0
        error_count = 0
        
        for i, pdf_file in enumerate(pdf_files, 1):
            filename = os.path.basename(pdf_file)
            filename_prefix = os.path.splitext(filename)[0]
            
            self.logger.info(f"[{i}/{len(pdf_files)}] Processing: {filename}")
            
            try:
                # Extract information using the main extraction pipeline
                result = self.extract(pdf_file)
                
                if result:
                    # Save all results in organized folder structure
                    raw_text = result.get('raw_text', '')
                    text_file, json_file, raw_text_file, file_output_dir = self.save_results(
                        result, output_dir, filename_prefix, raw_text
                    )
                    
                    results.append({
                        'pdf_file': pdf_file,
                        'filename': filename,
                        'success': True,
                        'output_folder': file_output_dir,
                        'files': {
                            'extraction_report': text_file,
                            'structured_data': json_file,
                            'raw_text': raw_text_file
                        },
                        'summary': result['extraction_summary']
                    })
                    
                    success_count += 1
                    self.logger.info(f"   ✅ Processed successfully - Files saved in: {file_output_dir}")
                else:
                    error_count += 1
                    self.logger.warning(f"   ⚠️  No data extracted from: {filename}")
                    
            except Exception as e:
                error_count += 1
                self.logger.error(f"   ❌ Error processing {filename}: {e}")
                results.append({
                    'pdf_file': pdf_file,
                    'filename': filename,
                    'success': False,
                    'error': str(e)
                })
        
        # Create batch summary
        self.logger.info("\n" + "=" * 60)
        self.logger.info("📊 BATCH PROCESSING SUMMARY")
        self.logger.info("=" * 60)
        self.logger.info(f"✅ Successfully processed: {success_count} files")
        self.logger.info(f"❌ Errors encountered: {error_count} files")
        self.logger.info(f"📁 All outputs saved in: {output_dir}")
        self.logger.info("=" * 60)
        
        # Save batch summary
        batch_summary = {
            'processing_timestamp': datetime.now().isoformat(),
            'input_directory': pdf_directory,
            'output_directory': output_dir,
            'total_files': len(pdf_files),
            'successful_extractions': success_count,
            'failed_extractions': error_count,
            'results': results
        }
        
        summary_file = os.path.join(output_dir, "batch_processing_summary.json")
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(batch_summary, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"📋 Batch summary saved to: {summary_file}")
        
        return results


def main():
    """Enhanced main function with single and batch processing options"""
    import sys
    
    if len(sys.argv) < 2:
        print("🤖 AI-Enhanced Court Order Extractor")
        print("=" * 50)
        print("Usage:")
        print("  Single file: python ai_enhanced_extractor.py <pdf_file>")
        print("  Batch mode:  python ai_enhanced_extractor.py <pdf_directory> --batch")
        print("\nExamples:")
        print("  python ai_enhanced_extractor.py \"../CourtOrder/Kerala High Court (8).pdf\"")
        print("  python ai_enhanced_extractor.py \"../CourtOrder\" --batch")
        print("\nDefault (no args): Process Kerala High Court (8).pdf")
        
        # Default behavior - process single test file
        pdf_path = "../CourtOrder/Kerala High Court (8).pdf"
        
        if not os.path.exists(pdf_path):
            print(f"❌ Test file not found: {pdf_path}")
            return
        
        print(f"\n🚀 Running default test with: {os.path.basename(pdf_path)}")
        extractor = MetaDataExtractor(use_gpu=False, debug=True)
        results = extractor.extract(pdf_path)
        
        # Save results including raw text
        output_dir = "output"
        filename_prefix = os.path.splitext(os.path.basename(pdf_path))[0]
        raw_text = results.get('raw_text', '')
        text_file, json_file, raw_text_file, file_output_dir = extractor.save_results(results, output_dir, filename_prefix, raw_text)
        
        print(extractor.format_output(results))
        return results
    
    # Command line processing
    input_path = sys.argv[1]
    batch_mode = len(sys.argv) > 2 and sys.argv[2] == "--batch"
    
    print("🚀 Initializing AI-Enhanced Court Order Extractor...")
    extractor = MetaDataExtractor(use_gpu=False, debug=True)
    
    if batch_mode:
        # Batch processing mode
        print(f"� Batch processing directory: {input_path}")
        results = extractor.process_multiple_pdfs(input_path)
        print(f"\n🎉 Batch processing completed! Processed {len(results)} files.")
        return results
    else:
        # Single file processing mode
        if not os.path.exists(input_path):
            print(f"❌ File not found: {input_path}")
            return None
        
        print(f"📄 Processing single file: {os.path.basename(input_path)}")
        results = extractor.extract(input_path)
        
        # Save results including raw text
        output_dir = "output"
        filename_prefix = os.path.splitext(os.path.basename(input_path))[0]
        raw_text = results.get('raw_text', '')
        text_file, json_file, raw_text_file, file_output_dir = extractor.save_results(results, output_dir, filename_prefix, raw_text)
        
        print(extractor.format_output(results))
        return results


if __name__ == "__main__":
    # This main function is disabled since we're using this module 
    # as an import in main.py. If you need to run this file directly,
    # uncomment the line below:
    # main()
    pass
