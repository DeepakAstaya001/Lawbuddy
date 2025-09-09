from langchain_ollama.llms import OllamaLLM # type: ignore
import json
import re
from typing import Dict, Any, List, Optional
import os

def generate_court_order_summary(document_text: str) -> str:
    """
    Generate a clear and concise summary of a court order following specific format requirements.
    Creates a 100-120 word summary covering essential elements.
    """
    llm = OllamaLLM(model="llama3.1:8b")
    
    # Special prompt for court order summarization
    prompt = f"""
You are a legal document summarization expert. Create a clear and concise summary of the court order provided below.

SUMMARIZATION REQUIREMENTS:
- Generate a summary of 100-120 words that captures essential elements
- Include details from the final judgement including fines, penalties, prison sentences with exact numbers
- Mention any contingencies mentioned in the judgement
- Cover any directions issued or acquittals
- Use simple and understandable language
- Focus on key facts: date, case number, parties, charges, court decision, and specific outcomes

COURT ORDER DOCUMENT:
{document_text}

EXAMPLE FORMAT (for reference):
"On 2 February 2024, Bail Application No. 41 of 2024 filed by Ibrahim, aged 36 accused in Crime No. 922/2023 of Vengara Police Station. He is charged under Section 286 IPC and Sections 4(b) & 5 of the Explosive Substances Act, 1908. for allegedly conducting illegal quarrying and blasting granite without a license, endangering life and property. The court noted his ownership of the site, a pending similar offence, the need for proper investigation. Anticipatory bail was denied. but directions were issued for him to surrender within two weeks. after which his bail request could be considered on merits."

Please provide a summary following this style and format, ensuring it's clear, factual, and within 100-120 words:
"""
    
    response = llm.invoke(prompt)
    return response

def answer_from_data(data_text: str, question: str) -> str:
    """
    Answer questions based on provided data using Llama
    """
    llm = OllamaLLM(model="llama3.1:8b")
    
    # Create a prompt that includes the data and question
    prompt = f"""
Based on the following data, please answer the question accurately. Only use information from the provided data.

DATA:
{data_text}

QUESTION: {question}

ANSWER: Please provide a clear, accurate answer based only on the information in the data above. If the answer cannot be found in the data, say "The information is not available in the provided data."
"""
    
    response = llm.invoke(prompt)
    return response

def interactive_qa_session(document_text: str = None):
    """
    Enhanced Interactive Q&A session with both document-specific and general chat capabilities
    """
    # Load the legal document
    if document_text is None:
        try:
            with open("raw_full_text.txt", 'r') as file:
                document_text = file.read()
            print("📄 Legal document loaded successfully from file!")
            print("=" * 60)
            print("📋 Document Preview:")
            print(document_text[:300] + "..." if len(document_text) > 300 else document_text)
            print("=" * 60)
        except FileNotFoundError:
            print("⚠️ No raw_full_text.txt found - Starting in General Chat Mode")
            print("💡 You can still ask general legal questions and discuss case scenarios!")
            document_text = None
    else:
        print("📄 Legal document loaded successfully from memory!")
        print("=" * 60)
        print("📋 Document Preview:")
        print(document_text[:300] + "..." if len(document_text) > 300 else document_text)
        print("=" * 60)
    
    print("\n🤖 Enhanced Legal AI Assistant")
    print("=" * 60)
    print("🎯 AVAILABLE MODES:")
    if document_text and document_text.strip():
        print("1. 📄 Document Q&A - Ask questions about the loaded legal document")
        print("2. 💬 General Chat - General legal discussions and case scenarios")
        current_mode = "document"  # Default to document mode if document available
    else:
        print("1. 💬 General Chat - Legal discussions and case scenarios")
        print("2. 📚 Legal Guidance - Get explanations about laws and procedures")
        current_mode = "general"  # Default to general mode if no document
    
    print("")
    print("💡 SPECIAL COMMANDS:")
    print("   'summary' - Generate document summary (if document available)")
    print("   'mode document' - Switch to document-specific Q&A")
    print("   'mode general' - Switch to general legal chat")
    print("   'help' - Show available commands")
    print("   'exit' or 'quit' - End session")
    print("=" * 60)
    
    while True:
        mode_indicator = "📄 DOC" if current_mode == "document" else "💬 CHAT"
        question = input(f"\n[{mode_indicator}] ❓ Your Question: ").strip()
        
        if question.lower() in ['exit', 'quit', '']:
            print("👋 Session ended. Goodbye!")
            break
        
        # Handle special commands
        if question.lower() == 'help':
            print("\n🆘 HELP - Available Commands:")
            print("=" * 40)
            if document_text and document_text.strip():
                print("📄 DOCUMENT MODE:")
                print("   • Ask any question about the loaded legal document")
                print("   • 'summary' - Get court order summary")
                print("   • 'mode general' - Switch to general chat")
            print("")
            print("💬 GENERAL MODE:")
            print("   • Discuss legal concepts and case scenarios")
            print("   • Get legal advice and explanations")
            if document_text and document_text.strip():
                print("   • 'mode document' - Switch back to document Q&A")
            print("")
            print("🔧 SYSTEM COMMANDS:")
            print("   • 'help' - Show this help")
            print("   • 'exit' or 'quit' - End session")
            continue
        
        if question.lower() == 'mode document':
            if document_text and document_text.strip():
                current_mode = "document"
                print("🔄 Switched to Document Q&A Mode")
                print("💡 You can now ask questions about the loaded legal document")
            else:
                print("❌ No document available! Please process a PDF first or use general chat mode.")
            continue
        
        if question.lower() == 'mode general':
            current_mode = "general"
            print("🔄 Switched to General Legal Chat Mode")
            print("💡 You can now discuss general legal topics and case scenarios")
            continue
        
        # Handle summary request
        if question.lower() in ['summary', 'summarize', 'give me summary', 'court order summary','give me a summary of this document','give me the summary of this document','summarize this document','summarize this court order']:
            if document_text and document_text.strip():
                print("\n📝 GENERATING COURT ORDER SUMMARY...")
                print("=" * 60)
                print("🤔 Processing document...")
                
                try:
                    summary = generate_court_order_summary(document_text)
                    
                    print("\n📋 COURT ORDER SUMMARY:")
                    print("=" * 60)
                    print(summary)
                    print("=" * 60)
                    
                    # Optionally save summary to file
                    save_choice = input("\n💾 Save summary to file? (y/n): ").strip().lower()
                    if save_choice in ['y', 'yes']:
                        with open("court_order_summary.txt", 'w') as f:
                            f.write(summary)
                        print("✅ Summary saved to 'court_order_summary.txt'")
                        
                except Exception as e:
                    print(f"❌ Error generating summary: {e}")
                    print("💡 Please check if the LLaMA model is running properly")
            else:
                print("❌ No document available for summarization!")
                print("💡 Please process a PDF first or ask general legal questions")
        
        # Handle document-specific questions
        elif current_mode == "document":
            if document_text and document_text.strip():
                print("\n🤔 Analyzing document...")
                try:
                    answer = answer_from_data(document_text, question)
                    print("✅ Answer:")
                    print("-" * 40)
                    print(answer)
                    print("-" * 40)
                    
                except Exception as e:
                    print(f"❌ Error processing document question: {e}")
                    print("💡 Please check if the LLaMA model is running properly")
            else:
                print("❌ No document available! Switching to general chat mode...")
                current_mode = "general"
                # Process as general question
                print("\n🤔 Thinking about your legal question...")
                try:
                    general_answer = general_legal_chat(question)
                    print("✅ Legal Assistant Response:")
                    print("-" * 40)
                    print(general_answer)
                    print("-" * 40)
                    
                except Exception as e:
                    print(f"❌ Error in general chat: {e}")
                    print("💡 Please check if the LLaMA model is running properly")
        
        # Handle general chat questions
        elif current_mode == "general":
            print("\n🤔 Thinking about your legal question...")
            try:
                general_answer = general_legal_chat(question)
                print("✅ Legal Assistant Response:")
                print("-" * 40)
                print(general_answer)
                print("-" * 40)
                
            except Exception as e:
                print(f"❌ Error in general chat: {e}")
                print("💡 Please check if the LLaMA model is running properly")

def general_legal_chat(question: str) -> str:
    """
    General legal chat for discussing legal concepts, case scenarios, and providing legal information
    """
    llm = OllamaLLM(model="llama3.1:8b")
    
    # Create a prompt for general legal discussion
    prompt = f"""
You are an expert legal AI assistant with comprehensive knowledge of Indian law, legal procedures, and case law. You provide helpful, accurate, and informative responses about legal topics.

GUIDELINES:
- Provide clear, accurate legal information
- Reference relevant laws, acts, and sections when applicable
- Explain legal concepts in simple terms
- For case scenarios, provide step-by-step legal analysis
- Always mention that this is for informational purposes and suggest consulting a qualified lawyer for specific legal advice
- Be professional and helpful in your responses

USER QUESTION: {question}

LEGAL ASSISTANT RESPONSE:
"""
    
    response = llm.invoke(prompt)
    return response


def extract_metadata_comprehensive(document_text: str, output_file: str = None) -> Dict[str, Any]:
    """
    Comprehensive metadata extraction using multi-stage approach:
    1. Regex patterns for basic field extraction
    2. LLaMA model for complex field extraction
    3. Other models as fallback for missing data
    
    Returns detailed JSON with extraction sources for each field.
    """
    
    print("🔍 Starting comprehensive metadata extraction...")
    print("=" * 60)
    
    # Initialize result structure
    extraction_result = {
        "extraction_metadata": {
            "extraction_methods": ["regex", "llama", "fallback_models"],
            "total_fields_attempted": 23,
            "extraction_timestamp": None,
            "processing_stages": []
        },
        "extracted_data": {},
        "extraction_sources": {}
    }
    
    # Define all target fields
    target_fields = {
        "case_number": "",
        "order_date": "",
        "judge_name": "",
        "court_name": "",
        "document_type": "",
        "parties": [],
        "petitioner_name": "",
        "petitioner_type": "",
        "petitioner_designation": "",
        "petitioner_address": {
            "apartment_house": "",
            "street": "",
            "village": "",
            "city": "",
            "district": "",
            "state": "",
            "zipcode": ""
        },
        "petitioner_age": "",
        "petitioner_alias": "",
        "petitioner_relations": "",
        "petitioner_other_details": "",
        "petitioner_counsels": [],
        "respondent_name": "",
        "respondent_type": "",
        "respondent_designation": "",
        "respondent_address": {
            "apartment_house": "",
            "street": "",
            "village": "",
            "city": "",
            "district": "",
            "state": "",
            "zipcode": ""
        },
        "respondent_age": "",
        "respondent_alias": "",
        "respondent_relations": "",
        "respondent_other_details": "",
        "respondent_counsels": [],
        "additional_respondents": [],
        "police_station": "",
        "crime_number": "",
        "fir_number": "",
        "sections_acts": [],
        "all_counsels": []
    }
    
    # Stage 1: Regex-based extraction
    print("📋 Stage 1: Regex Pattern Extraction")
    print("-" * 40)
    
    regex_results = _extract_with_regex(document_text)
    extraction_result["extraction_metadata"]["processing_stages"].append({
        "stage": "regex",
        "fields_extracted": len([k for k, v in regex_results.items() if v]),
        "success": True
    })
    
    for field, value in regex_results.items():
        if value:
            extraction_result["extracted_data"][field] = value
            extraction_result["extraction_sources"][field] = "regex"
            print(f"   ✅ {field}: Found via regex")
        else:
            print(f"   ❌ {field}: Not found via regex")
    
    # Stage 2: LLaMA-based extraction for missing fields
    print("\n🦙 Stage 2: LLaMA Model Extraction")
    print("-" * 40)
    
    missing_fields = [field for field in target_fields.keys() 
                     if field not in extraction_result["extracted_data"] 
                     or not extraction_result["extracted_data"].get(field)]
    
    if missing_fields:
        llama_results = _extract_with_llama(document_text, missing_fields)
        extraction_result["extraction_metadata"]["processing_stages"].append({
            "stage": "llama",
            "fields_attempted": len(missing_fields),
            "fields_extracted": len([k for k, v in llama_results.items() if v]),
            "success": True
        })
        
        for field, value in llama_results.items():
            if value:
                extraction_result["extracted_data"][field] = value
                extraction_result["extraction_sources"][field] = "llama"
                print(f"   ✅ {field}: Found via LLaMA")
            else:
                print(f"   ❌ {field}: Not found via LLaMA")
    else:
        print("   ℹ️ All fields already extracted via regex")
    
    # Stage 3: Fallback models for remaining missing fields
    print("\n🔧 Stage 3: Fallback Model Extraction")
    print("-" * 40)
    
    still_missing = [field for field in target_fields.keys() 
                    if field not in extraction_result["extracted_data"] 
                    or not extraction_result["extracted_data"].get(field)]
    
    if still_missing:
        fallback_results = _extract_with_fallback_models(document_text, still_missing)
        extraction_result["extraction_metadata"]["processing_stages"].append({
            "stage": "fallback",
            "fields_attempted": len(still_missing),
            "fields_extracted": len([k for k, v in fallback_results.items() if v]),
            "success": True
        })
        
        for field, value in fallback_results.items():
            if value:
                extraction_result["extracted_data"][field] = value
                extraction_result["extraction_sources"][field] = "fallback_model"
                print(f"   ✅ {field}: Found via fallback model")
            else:
                extraction_result["extraction_sources"][field] = "not_found"
                print(f"   ❌ {field}: Not found in any method")
    else:
        print("   ℹ️ All fields already extracted")
    
    # Add timestamp and summary
    import datetime
    extraction_result["extraction_metadata"]["extraction_timestamp"] = datetime.datetime.now().isoformat()
    extraction_result["extraction_metadata"]["total_fields_extracted"] = len([
        k for k, v in extraction_result["extracted_data"].items() if v
    ])
    extraction_result["extraction_metadata"]["extraction_success_rate"] = (
        extraction_result["extraction_metadata"]["total_fields_extracted"] / 
        extraction_result["extraction_metadata"]["total_fields_attempted"] * 100
    )
    
    # Save to file if specified
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(extraction_result, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Results saved to: {output_file}")
    
    # Print summary
    print("\n📊 EXTRACTION SUMMARY")
    print("=" * 60)
    print(f"Total Fields Attempted: {extraction_result['extraction_metadata']['total_fields_attempted']}")
    print(f"Total Fields Extracted: {extraction_result['extraction_metadata']['total_fields_extracted']}")
    print(f"Success Rate: {extraction_result['extraction_metadata']['extraction_success_rate']:.1f}%")
    print("\nExtraction Sources:")
    for source in ["regex", "llama", "fallback_model", "not_found"]:
        count = list(extraction_result["extraction_sources"].values()).count(source)
        if count > 0:
            print(f"   {source.title()}: {count} fields")
    
    return extraction_result

def _extract_with_regex(text: str) -> Dict[str, Any]:
    """Extract fields using comprehensive regex patterns"""
    
    results = {}
    
    # Case Number patterns
    case_patterns = [
        r'(?:W\.P\(C\)|WP\(C\))\s*(?:NO\.?)?\s*(\d+)\/(\d{2,4})',
        r'(?:B\.A\.|BA|BAIL APPLICATION)\s*(?:NO\.?)?\s*(\d+)\/(\d{4})',
        r'(?:CRIMINAL REFERENCE|CR\.REF)\s*(?:NO\.?)?\s*(\d+)\/(\d{4})',
        r'Case\s*(?:No\.?)?\s*(\d+)\/(\d{4})'
    ]
    
    for pattern in case_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            if len(match.groups()) == 2:
                case_no, year = match.groups()
                results["case_number"] = f"{case_no}/{year}"
                break
    
    # Order Date patterns
    date_patterns = [
        r'(?:dated?|order\s+dated?|decided\s+on|on)\s+(\d{1,2}(?:st|nd|rd|th)?\s+\w+,?\s+\d{4})',
        r'(\d{1,2}[-./]\d{1,2}[-./]\d{2,4})',
        r'(\d{1,2}\s+\w+\s+\d{4})'
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            results["order_date"] = match.group(1)
            break
    
    # Judge Name patterns
    judge_patterns = [
        r'(?:HONOURABLE|HON\'BLE|HON\.)\s+(?:MR\.?|MS\.?|MRS\.?)?\s*JUSTICE\s+([A-Z][A-Z\s\.]+?)(?:\s+J\.?)?(?:\s|$|\n)',
        r'(?:JUDGE|J\.)\s*:?\s*([A-Z][A-Z\s\.]+?)(?:\s+J\.?)?(?:\s|$|\n)',
        r'BEFORE\s*:?\s*(?:THE\s+)?(?:HONOURABLE\s+)?(?:MR\.?|MS\.?|MRS\.?)?\s*JUSTICE\s+([A-Z][A-Z\s\.]+)'
    ]
    
    for pattern in judge_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            results["judge_name"] = match.group(1).strip()
            break
    
    # Petitioner Name patterns
    petitioner_patterns = [
        r'PETITIONER[\/]?(?:\(S\))?\s*:?\s*([A-Z][A-Za-z\s\.]+?)(?:\s+\.{3}|\s+VS\.?|\s+V\/S|\n|$)',
        r'APPLICANT[\/]?(?:\(S\))?\s*:?\s*([A-Z][A-Za-z\s\.]+?)(?:\s+\.{3}|\s+VS\.?|\s+V\/S|\n|$)'
    ]
    
    for pattern in petitioner_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            results["petitioner_name"] = match.group(1).strip()
            break
    
    # Respondent Name patterns (enhanced)
    respondent_patterns = [
        r'RESPONDENT[\/]?(?:\(S\))?\s*:?\s*([A-Z][A-Za-z\s\.]+?)(?:\s+\.{3}|\s*\n|$)',
        r'(?:VS\.?|V\/S)\s+([A-Z][A-Za-z\s\.]+?)(?:\s+\.{3}|\s*\n|$)',
        r'(?:STATE\s+OF\s+)([A-Z][A-Za-z\s]+)',
        r'(?:UNION\s+OF\s+INDIA|GOVERNMENT\s+OF\s+[A-Z\s]+)'
    ]
    
    for pattern in respondent_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            if len(match.groups()) >= 1:
                results["respondent_name"] = match.group(1).strip()
            else:
                results["respondent_name"] = match.group(0).strip()
            break
    
    # Respondent Type detection
    respondent_name = results.get("respondent_name", "")
    if respondent_name:
        if "state of" in respondent_name.lower() or "union of india" in respondent_name.lower():
            results["respondent_type"] = "government"
        elif "police station" in respondent_name.lower():
            results["respondent_type"] = "police"
        elif "corporation" in respondent_name.lower() or "company" in respondent_name.lower():
            results["respondent_type"] = "corporate"
        elif "trust" in respondent_name.lower():
            results["respondent_type"] = "trust"
        else:
            results["respondent_type"] = "individual"
    
    # Respondent Address patterns
    respondent_addr_patterns = [
        r'(?:RESPONDENT[^:]*:.*?)([A-Z][A-Za-z\s]+?)\s+House[,\s]+([A-Z][A-Za-z\s]+?)[,\s]+([A-Z][A-Za-z\s]+?)\s+District[,\s]+PIN[:\-\s]*(\d{6})',
        r'(?:represented\s+by[^,]*,?\s*)([A-Z][A-Za-z\s]+)[,\s]+([A-Z][A-Za-z\s]+)[,\s]+([A-Z][A-Za-z\s]+)\s*[-\s]*(\d{6})?'
    ]
    
    for pattern in respondent_addr_patterns:
        addr_match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if addr_match and len(addr_match.groups()) >= 3:
            results["respondent_address"] = {
                "apartment_house": addr_match.group(1).strip() if addr_match.group(1) else "",
                "village": addr_match.group(2).strip() if len(addr_match.groups()) > 1 and addr_match.group(2) else "",
                "district": addr_match.group(3).strip() if len(addr_match.groups()) > 2 and addr_match.group(3) else "",
                "zipcode": addr_match.group(4).strip() if len(addr_match.groups()) > 3 and addr_match.group(4) else ""
            }
            break
    
    # Respondent Age pattern
    resp_age_pattern = r'(?:respondent[^,]*,?\s*aged?\s+(\d{1,3})\s+years?)'
    resp_age_match = re.search(resp_age_pattern, text, re.IGNORECASE)
    if resp_age_match:
        results["respondent_age"] = resp_age_match.group(1)
    
    # Respondent Relations pattern
    resp_relations_patterns = [
        r'(?:respondent[^,]*,?\s*(?:S\/O|D\/O|W\/O)\s+([A-Z][A-Za-z\s\.]+?)(?:,|\s|$|\n))',
        r'(?:(?:S\/O|D\/O|W\/O)\s+([A-Z][A-Za-z\s\.]+?)(?:.*?respondent))'
    ]
    
    for pattern in resp_relations_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            results["respondent_relations"] = match.group(1).strip()
            break
    
    # Additional Respondents (multiple respondents)
    additional_resp_pattern = r'(?:RESPONDENT\s+(?:NO\.?\s*)?(\d+)[:\s]*([A-Z][A-Za-z\s\.]+?)(?:\s+\.{3}|\s*\n|$))'
    add_respondents = re.findall(additional_resp_pattern, text, re.IGNORECASE)
    if add_respondents:
        results["additional_respondents"] = [
            {"number": num, "name": name.strip()} for num, name in add_respondents
        ]
    
    # Counsels extraction (enhanced for both parties)
    counsel_patterns = [
        r'(?:FOR\s+PETITIONER[^:]*:?\s*)([A-Z][A-Za-z\s,\.]+?)(?:\n|$)',
        r'(?:FOR\s+RESPONDENT[^:]*:?\s*)([A-Z][A-Za-z\s,\.]+?)(?:\n|$)',
        r'(?:ADVOCATES?[^:]*:?\s*)([A-Z][A-Za-z\s,\.]+?)(?:\n|$)',
        r'(?:COUNSEL[^:]*:?\s*)([A-Z][A-Za-z\s,\.]+?)(?:\n|$)'
    ]
    
    petitioner_counsels = []
    respondent_counsels = []
    all_counsels = []
    
    # Extract petitioner counsels
    pet_counsel_match = re.search(r'(?:FOR\s+PETITIONER[^:]*:?\s*)([A-Z][A-Za-z\s,\.]+?)(?:\n|FOR\s+RESPONDENT)', text, re.IGNORECASE | re.DOTALL)
    if pet_counsel_match:
        counsels_text = pet_counsel_match.group(1)
        # Split by common separators
        counsels = re.split(r'[,\n]+', counsels_text)
        petitioner_counsels = [c.strip() for c in counsels if c.strip() and len(c.strip()) > 2]
        results["petitioner_counsels"] = petitioner_counsels
    
    # Extract respondent counsels
    resp_counsel_match = re.search(r'(?:FOR\s+RESPONDENT[^:]*:?\s*)([A-Z][A-Za-z\s,\.]+?)(?:\n|$)', text, re.IGNORECASE | re.DOTALL)
    if resp_counsel_match:
        counsels_text = resp_counsel_match.group(1)
        counsels = re.split(r'[,\n]+', counsels_text)
        respondent_counsels = [c.strip() for c in counsels if c.strip() and len(c.strip()) > 2]
        results["respondent_counsels"] = respondent_counsels
    
    # Combine all counsels
    all_counsels.extend(petitioner_counsels)
    all_counsels.extend(respondent_counsels)
    if all_counsels:
        results["all_counsels"] = list(set(all_counsels))  # Remove duplicates
    
    # Police Station patterns
    police_patterns = [
        r'([A-Z][A-Za-z\s]+?)\s+Police\s+Station',
        r'P\.?S\.?\s+([A-Z][A-Za-z\s]+)',
        r'Station\s+House\s+Officer[,\s]+([A-Z][A-Za-z\s]+)\s+Police\s+Station'
    ]
    
    for pattern in police_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            results["police_station"] = match.group(1).strip()
            break
    
    # Crime Number patterns
    crime_patterns = [
        r'Crime\s+(?:No\.?|Number)\s*(\d+\/\d{2,4})',
        r'F\.?I\.?R\.?\s+(?:No\.?|Number)\s*(\d+\/\d{2,4})'
    ]
    
    for pattern in crime_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            results["crime_number"] = match.group(1)
            break
    
    # Address patterns
    address_pattern = r'([A-Z][A-Za-z\s]+?)\s+House[,\s]+([A-Z][A-Za-z\s]+?)[,\s]+([A-Z][A-Za-z\s]+?)\s+District[,\s]+PIN[:\-\s]*(\d{6})'
    address_match = re.search(address_pattern, text, re.IGNORECASE)
    if address_match:
        results["petitioner_address"] = {
            "apartment_house": address_match.group(1).strip(),
            "village": address_match.group(2).strip(),
            "district": address_match.group(3).strip(),
            "zipcode": address_match.group(4)
        }
    
    # Age pattern
    age_pattern = r'(?:aged?|age)\s+(\d{1,3})\s+years?'
    age_match = re.search(age_pattern, text, re.IGNORECASE)
    if age_match:
        results["petitioner_age"] = age_match.group(1)
    
    # Section/Act patterns
    section_patterns = [
        r'Section\s+(\d+[a-z]*(?:\([a-z0-9]+\))?)\s+(?:of\s+the\s+)?([^,\n\.]+)',
        r'under\s+Section\s+(\d+[a-z]*(?:\([a-z0-9]+\))?)\s+(?:of\s+the\s+)?([^,\n\.]+)'
    ]
    
    sections = []
    for pattern in section_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            if len(match) == 2:
                section, act = match
                sections.append(f"Section {section} {act.strip()}")
    
    if sections:
        results["sections_acts"] = list(set(sections))  # Remove duplicates
    
    return results

def _extract_with_llama(text: str, missing_fields: List[str]) -> Dict[str, Any]:
    """Extract missing fields using LLaMA model with detailed prompts"""
    
    llm = OllamaLLM(model="llama3.1:8b")
    results = {}
    
    # Create comprehensive extraction prompt
    prompt = f"""
You are an expert legal document analyzer. Extract the following specific information from the court document below. 

EXTRACTION REQUIREMENTS:
- Return ONLY the requested information in a clear, structured format
- If information is not found, return "NOT_FOUND" for that field
- Be precise and accurate
- Extract exact text as it appears in the document

FIELDS TO EXTRACT:
{', '.join(missing_fields)}

DETAILED FIELD DESCRIPTIONS:
- case_number: Complete case number (e.g., W.P.(C) No. 123/2024, B.A. No. 456/2023)
- order_date: Date when the order was passed (e.g., 15th January, 2024)
- judge_name: Full name of the presiding judge
- court_name: Name of the court (e.g., High Court of Kerala)
- document_type: Type of legal document (e.g., Writ Petition, Bail Application)

PETITIONER INFORMATION:
- petitioner_name: Name of the person/entity filing the case
- petitioner_type: Type of petitioner (individual, government, NGO, company, trust, etc.)
- petitioner_designation: Official designation if any
- petitioner_address: Complete address with components (apartment, street, village, city, district, state, zipcode)
- petitioner_age: Age in years
- petitioner_alias: Any alias names mentioned
- petitioner_relations: Father's/husband's/mother's name (S/o, D/o, W/o relationships)
- petitioner_other_details: Any other relevant details about petitioner
- petitioner_counsels: Names of lawyers representing petitioner

RESPONDENT INFORMATION:
- respondent_name: Name of the responding party
- respondent_type: Type of respondent (government, individual, police, corporate, trust, etc.)
- respondent_designation: Official designation of respondent
- respondent_address: Complete address of respondent (apartment, street, village, city, district, state, zipcode)
- respondent_age: Age of respondent in years
- respondent_alias: Any alias names of respondent
- respondent_relations: Father's/husband's/mother's name of respondent (S/o, D/o, W/o relationships)
- respondent_other_details: Any other relevant details about respondent
- respondent_counsels: Names of lawyers representing respondent
- additional_respondents: List of additional respondents if multiple parties

CASE DETAILS:
- police_station: Name of police station if mentioned
- crime_number: Crime number or FIR number
- fir_number: FIR registration number
- sections_acts: List of legal sections and acts mentioned
- all_counsels: Complete list of all lawyers mentioned in the case

DOCUMENT TEXT:
{text}

EXTRACTION RESULTS:
Please provide the extracted information in this exact format:
field_name: extracted_value
"""
    
    try:
        response = llm.invoke(prompt)
        
        # Parse the response
        lines = response.strip().split('\n')
        for line in lines:
            if ':' in line:
                field, value = line.split(':', 1)
                field = field.strip().lower()
                value = value.strip()
                
                if field in missing_fields and value and value != "NOT_FOUND":
                    results[field] = value
        
        # Special handling for complex fields
        if 'petitioner_address' in missing_fields and 'petitioner_address' not in results:
            address_prompt = f"""
Extract the complete address of the petitioner from this legal document. 
Provide the address components separately:

DOCUMENT: {text[:2000]}...

Extract these address components for PETITIONER:
- apartment_house: House/apartment name or number
- street: Street name
- village: Village name
- city: City name
- district: District name
- state: State name  
- zipcode: PIN code/zip code

Format: component_name: value (or NOT_FOUND if not available)
"""
            
            addr_response = llm.invoke(address_prompt)
            address_dict = {}
            for line in addr_response.split('\n'):
                if ':' in line:
                    comp, val = line.split(':', 1)
                    comp = comp.strip().lower()
                    val = val.strip()
                    if val and val != "NOT_FOUND":
                        address_dict[comp] = val
            
            if address_dict:
                results['petitioner_address'] = address_dict
        
        # Special handling for respondent address
        if 'respondent_address' in missing_fields and 'respondent_address' not in results:
            resp_address_prompt = f"""
Extract the complete address of the respondent from this legal document. 
Provide the address components separately:

DOCUMENT: {text[:2000]}...

Extract these address components for RESPONDENT:
- apartment_house: House/apartment name or number
- street: Street name
- village: Village name
- city: City name
- district: District name
- state: State name  
- zipcode: PIN code/zip code

Format: component_name: value (or NOT_FOUND if not available)
"""
            
            resp_addr_response = llm.invoke(resp_address_prompt)
            resp_address_dict = {}
            for line in resp_addr_response.split('\n'):
                if ':' in line:
                    comp, val = line.split(':', 1)
                    comp = comp.strip().lower()
                    val = val.strip()
                    if val and val != "NOT_FOUND":
                        resp_address_dict[comp] = val
            
            if resp_address_dict:
                results['respondent_address'] = resp_address_dict
        
        # Special handling for multiple respondents
        if 'additional_respondents' in missing_fields and 'additional_respondents' not in results:
            multiple_resp_prompt = f"""
Extract information about all respondents from this legal document.
Look for multiple respondents numbered as Respondent 1, 2, 3, etc.

DOCUMENT: {text[:2000]}...

For each respondent, extract:
- Respondent number
- Name
- Type (government/individual/corporate/etc.)
- Any other details

Format: 
respondent_1: Name - Type - Details
respondent_2: Name - Type - Details
(or NOT_FOUND if no additional respondents)
"""
            
            mult_resp_response = llm.invoke(multiple_resp_prompt)
            additional_respondents = []
            for line in mult_resp_response.split('\n'):
                if 'respondent_' in line.lower() and ':' in line:
                    parts = line.split(':', 1)
                    if len(parts) == 2:
                        resp_info = parts[1].strip()
                        if resp_info != "NOT_FOUND":
                            additional_respondents.append(resp_info)
            
            if additional_respondents:
                results['additional_respondents'] = additional_respondents
                
    except Exception as e:
        print(f"   ⚠️ LLaMA extraction error: {e}")
    
    return results

def _extract_with_fallback_models(text: str, missing_fields: List[str]) -> Dict[str, Any]:
    """Extract remaining fields using fallback models (simulated for now)"""
    
    results = {}
    
    # This is where you would integrate other models like BERT, RoBERTa, etc.
    # For now, implementing enhanced pattern matching as fallback
    
    print("   🔄 Using enhanced pattern matching as fallback...")
    
    # Enhanced patterns for difficult extractions
    if 'court_name' in missing_fields:
        court_patterns = [
            r'(?:IN\s+THE\s+)?(?:HIGH\s+COURT\s+OF\s+)([A-Z\s]+?)(?:\s+AT\s+([A-Z\s]+))?',
            r'(?:BEFORE\s+THE\s+)?([A-Z\s]+?HIGH\s+COURT)',
            r'(HIGH\s+COURT\s+OF\s+[A-Z\s]+)'
        ]
        
        for pattern in court_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                results['court_name'] = match.group(0).strip()
                break
    
    if 'document_type' in missing_fields:
        # Detect document type from content
        if re.search(r'writ\s+petition|w\.p\(c\)|wp\(c\)', text, re.IGNORECASE):
            results['document_type'] = "Writ Petition (Civil)"
        elif re.search(r'bail\s+application|b\.a\.|anticipatory\s+bail', text, re.IGNORECASE):
            results['document_type'] = "Anticipatory Bail Application"
        elif re.search(r'criminal\s+petition|crl\.p', text, re.IGNORECASE):
            results['document_type'] = "Criminal Petition"
        elif re.search(r'appeal', text, re.IGNORECASE):
            results['document_type'] = "Appeal"
    
    # Add more fallback logic for other fields
    
    return results


if __name__ == "__main__":
    print("🚀 ENHANCED LEGAL DOCUMENT AI SYSTEM")
    print("=" * 60)
    print("Choose an option:")
    print("1. Interactive Q&A Session (Enhanced with General Chat)")
    print("2. Test with predefined questions")
    print("3. Single question mode")
    print("4. Generate Court Order Summary")
    print("5. Comprehensive Metadata Extraction")
    print("6. General Legal Chat (No document required)")
    
    choice = input("\nEnter your choice (1/2/3/4/5/6): ").strip()
    
    if choice == "1":
        print("\n🤖 Starting Enhanced Interactive Q&A Session...")
        print("💡 This session supports both document analysis and general legal chat!")
        interactive_qa_session()
    elif choice == "6":
        print("\n💬 Starting General Legal Chat Mode...")
        print("💡 You can discuss legal concepts, case scenarios, and get legal guidance!")
        interactive_qa_session()  # Will automatically switch to general mode if no document
    elif choice == "2":
        try:
            with open("raw_full_text.txt", 'r') as file:
                document_text = file.read()
            
            predefined_questions = [
                "What is the case number?",
                "Who are the parties involved?",
                "What is the main legal issue?",
                "What was the court's decision?",
                "What are the legal provisions mentioned?"
            ]
            
            print("\n🧪 Testing with predefined questions...")
            for i, question in enumerate(predefined_questions, 1):
                print(f"\n{i}. Question: {question}")
                answer = answer_from_data(document_text, question)
                print(f"   Answer: {answer}")
                
        except FileNotFoundError:
            print("❌ Error: raw_full_text.txt not found!")
            print("💡 Switching to general legal chat mode...")
            interactive_qa_session()
    elif choice == "3":
        try:
            with open("raw_full_text.txt", 'r') as file:
                document_text = file.read()
            
            question = input("Enter your question about the document: ")
            answer = answer_from_data(document_text, question)
            print(f"\nAnswer: {answer}")
            
        except FileNotFoundError:
            print("❌ Error: raw_full_text.txt not found!")
            question = input("Enter your general legal question: ")
            answer = general_legal_chat(question)
            print(f"\nLegal Assistant Response: {answer}")
    elif choice == "4":
        try:
            with open("raw_full_text.txt", 'r') as file:
                document_text = file.read()
            
            print("\n📝 GENERATING COURT ORDER SUMMARY...")
            print("=" * 60)
            print("🤔 Processing document...")
            
            summary = generate_court_order_summary(document_text)
            
            print("\n📋 COURT ORDER SUMMARY:")
            print("=" * 60)
            print(summary)
            print("=" * 60)
            
            # Optionally save summary to file
            save_choice = input("\n💾 Save summary to file? (y/n): ").strip().lower()
            if save_choice in ['y', 'yes']:
                with open("court_order_summary.txt", 'w') as f:
                    f.write(summary)
                print("✅ Summary saved to 'court_order_summary.txt'")
                
        except FileNotFoundError:
            print("❌ Error: raw_full_text.txt not found!")
            print("💡 Please process a PDF file first using main.py")
        except Exception as e:
            print(f"❌ Error generating summary: {e}")
    elif choice == "5":
        try:
            with open("raw_full_text.txt", 'r', encoding='utf-8') as file:
                document_text = file.read()
            
            print("\n🔍 STARTING COMPREHENSIVE METADATA EXTRACTION...")
            print("=" * 60)
            
            # Get output filename
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            default_filename = f"metadata_extraction_{timestamp}.json"
            output_file = input(f"💾 Output filename (default: {default_filename}): ").strip()
            if not output_file:
                output_file = default_filename
            
            # Run comprehensive extraction
            results = extract_metadata_comprehensive(document_text, output_file)
            
            print("\n✅ Metadata extraction completed!")
            print(f"📁 Results saved to: {output_file}")
            
            # Show detailed results
            show_details = input("\n📋 Show detailed extraction results? (y/n): ").strip().lower()
            if show_details in ['y', 'yes']:
                print("\n📊 DETAILED EXTRACTION RESULTS:")
                print("=" * 60)
                
                for field, value in results["extracted_data"].items():
                    source = results["extraction_sources"].get(field, "unknown")
                    print(f"🔹 {field}: {value}")
                    print(f"   📌 Source: {source}")
                    print()
            
        except FileNotFoundError:
            print("❌ Error: raw_full_text.txt not found!")
            print("💡 Please ensure you have processed a PDF and have the raw text file available.")
        except Exception as e:
            print(f"❌ Error during metadata extraction: {e}")
    else:
        print("Invalid choice. Running interactive session by default.")
        print("💡 Starting in general chat mode since no specific choice was made...")
        interactive_qa_session()