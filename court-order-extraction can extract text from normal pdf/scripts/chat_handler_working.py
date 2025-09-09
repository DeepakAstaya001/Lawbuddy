#!/usr/bin/env python3
"""
Enhanced Chat Handler for Legal AI Assistant with LLaMA Integration
Processes chat requests and uses extracted document text with LLaMA model.
Supports both document-specific and general legal questions.
"""

import sys
import json
import os
import time
import signal
from pathlib import Path

# Add timeout handling
class TimeoutError(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutError("Operation timed out")

def with_timeout(func, timeout_seconds=30):
    """
    Execute function with timeout
    """
    def wrapper(*args, **kwargs):
        # Set timeout signal
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(timeout_seconds)
        
        try:
            result = func(*args, **kwargs)
            signal.alarm(0)  # Cancel alarm
            return result
        except TimeoutError:
            return "⏱️ **Response timeout**: The AI is taking longer than expected. Please try a simpler question or try again later."
        except Exception as e:
            signal.alarm(0)  # Cancel alarm
            raise e
    
    return wrapper

# Add the scripts directory to Python path
scripts_dir = Path(__file__).parent
sys.path.insert(0, str(scripts_dir))

# Import LLaMA functions
try:
    from llama import answer_from_data, generate_court_order_summary
    LLAMA_AVAILABLE = True
except ImportError as e:
    print(f"Warning: LLaMA not available: {e}", file=sys.stderr)
    LLAMA_AVAILABLE = False

def general_legal_chat_llama(question):
    """
    Handle general legal questions using LLaMA AI model with timeout
    """
    @with_timeout
    def _llama_query():
        if not LLAMA_AVAILABLE:
            return general_legal_chat_simple(question)
        
        # Import LLaMA for general legal assistance
        from langchain_ollama.llms import OllamaLLM
        
        llm = OllamaLLM(model="llama3.1:8b")
        
        # Enhanced prompt for legal assistance
        prompt = f"""
You are an expert legal AI assistant specializing in Indian law and legal procedures. Provide accurate, helpful, and informative responses to legal questions.

GUIDELINES:
- Provide clear, accurate legal information based on Indian law
- Explain legal concepts in simple, understandable language
- Include relevant sections, acts, or procedures when applicable
- If asked about specific cases, provide general legal guidance
- Always mention that this is for informational purposes and recommend consulting a qualified lawyer for specific legal advice

LEGAL QUESTION: {question}

Please provide a comprehensive and helpful response:
"""
        
        response = llm.invoke(prompt)
        
        # Add disclaimer
        disclaimer = "\n\n⚖️ **Legal Disclaimer**: This information is for educational purposes only. Please consult with a qualified legal professional for advice specific to your situation."
        
        return response + disclaimer
    
    try:
        return _llama_query()
    except Exception as e:
        print(f"LLaMA general chat error: {e}", file=sys.stderr)
        return general_legal_chat_simple(question)

def document_qa_llama(document_text, question):
    """
    Advanced document Q&A using LLaMA AI model with timeout
    """
    @with_timeout
    def _llama_document_query():
        if not LLAMA_AVAILABLE:
            return document_qa_simple(document_text, question)
        
        # Check for special summary request
        if any(word in question.lower() for word in ['summary', 'summarize', 'overview']):
            try:
                summary = generate_court_order_summary(document_text)
                return f"📄 **Document Summary:**\n\n{summary}"
            except Exception as e:
                print(f"Summary generation error: {e}", file=sys.stderr)
                # Fall back to simple summary
                return document_qa_simple(document_text, question)
        
        # Use LLaMA for document-specific questions
        try:
            response = answer_from_data(document_text, question)
            return f"📄 **Based on your document:**\n\n{response}"
        except Exception as e:
            print(f"LLaMA document Q&A error: {e}", file=sys.stderr)
            return document_qa_simple(document_text, question)
    
    try:
        return _llama_document_query()
    except Exception as e:
        print(f"Document Q&A error: {e}", file=sys.stderr)
        return document_qa_simple(document_text, question)

def document_qa_simple(document_text, question):
    """
    Simple document Q&A without external dependencies
    """
    try:
        question_lower = question.lower()
        response_parts = []
        
        # Enhanced petitioner/party detection
        if any(word in question_lower for word in ['petitioner', 'petitioners', 'plaintiff', 'parties', 'party', 'appellant', 'applicant']):
            response_parts.append("👥 **Parties Information:**")
            
            # Look for common patterns
            petitioner_patterns = [
                r'(?i)petitioner[s]?\s*[:–-]\s*([^\n\r\.]+)',
                r'(?i)plaintiff[s]?\s*[:–-]\s*([^\n\r\.]+)', 
                r'(?i)applicant[s]?\s*[:–-]\s*([^\n\r\.]+)',
                r'(?i)appellant[s]?\s*[:–-]\s*([^\n\r\.]+)',
                r'(?i)vs?\.\s*([^\n\r\.]+)',
                r'(?i)v/s\s*([^\n\r\.]+)',
                r'(?i)between\s+([^\n\r\.]+?)\s+and',
                r'(?i)([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:petitioner|plaintiff|applicant|appellant)',
            ]
            
            import re
            found_parties = []
            
            for pattern in petitioner_patterns:
                matches = re.findall(pattern, document_text)
                for match in matches:
                    party = match.strip().strip('.,;:')
                    if len(party) > 2 and len(party) < 100:  # Reasonable length
                        found_parties.append(party)
            
            if found_parties:
                response_parts.append("**Found Parties:**")
                for i, party in enumerate(set(found_parties[:5])):  # Unique parties, max 5
                    response_parts.append(f"• {party}")
            else:
                # Fallback: Look for any line containing these keywords
                for line in document_text.split('\n'):
                    line = line.strip()
                    if any(keyword in line.lower() for keyword in ['petitioner', 'plaintiff', 'vs', 'v/s', 'between']):
                        if len(line) < 200:  # Not too long
                            response_parts.append(f"• {line}")
                            break
                
                if len(response_parts) == 1:  # Only header added
                    response_parts.append("Could not identify specific parties from the document text.")
                    response_parts.append("Please check the document for sections mentioning petitioner, plaintiff, or party details.")
        
        elif any(word in question_lower for word in ['respondent', 'respondents', 'defendant', 'defendants']):
            response_parts.append("👥 **Respondent Information:**")
            
            # Look for respondent patterns
            for line in document_text.split('\n'):
                line = line.strip()
                if any(keyword in line.lower() for keyword in ['respondent', 'defendant']):
                    if len(line) < 200:
                        response_parts.append(f"• {line}")
                        break
        
        elif any(word in question_lower for word in ['court', 'judge', 'coram']):
            response_parts.append("🏛️ **Court Information:**")
            
            for line in document_text.split('\n'):
                line = line.strip()
                if any(keyword in line.lower() for keyword in ['court', 'judge', 'hon\'ble', 'coram']):
                    if len(line) < 200:
                        response_parts.append(f"• {line}")
                        break
        
        elif any(word in question_lower for word in ['date', 'dates', 'when']):
            response_parts.append("📅 **Date Information:**")
            
            dates = []
            for line in document_text.split('\n'):
                if any(keyword in line.lower() for keyword in ['dated', 'date', '2023', '2024', '2025']):
                    dates.append(line.strip())
            
            response_parts.append("📅 **Important Dates:**")
            response_parts.extend(dates[:3])
            
        else:
            # General document search
            relevant_lines = []
            question_words = question_lower.split()
            
            for line in document_text.split('\n'):
                line_lower = line.lower()
                if any(word in line_lower for word in question_words if len(word) > 3):
                    relevant_lines.append(line.strip())
                    if len(relevant_lines) >= 3:
                        break
            
            if relevant_lines:
                response_parts.append(f"🔍 **Found relevant information for your question: '{question}'**")
                response_parts.extend(relevant_lines)
            else:
                response_parts.append(f"📝 **Regarding your question: '{question}'**")
                response_parts.append("I've analyzed the document but couldn't find specific information matching your query.")
                response_parts.append("Here are some key details from the document:")
                # Show first few lines of document
                doc_lines = [line.strip() for line in document_text.split('\n') if line.strip()]
                response_parts.extend(doc_lines[:3])
        
        return '\n'.join(response_parts)
        
    except Exception as e:
        return f"I apologize, but I encountered an error while analyzing the document: {str(e)}"

def general_legal_chat_simple(question):
    """
    Simple general legal chat responses with enhanced scenario handling
    """
    question_lower = question.lower()
    
    # Landlord-tenant issues
    if any(word in question_lower for word in ['landlord', 'rent', 'tenant', 'eviction', 'lease', 'housing']):
        return """🏠 **Landlord-Tenant Legal Guidance:**

**Your Scenario**: Landlord demanding extra money and making threats

**Your Legal Options**:
• **Document Everything**: Keep records of all communications, rent receipts, and threats
• **Know Your Rights**: Landlords cannot demand payments beyond agreed rent and legal deposits
• **Threats are Illegal**: Threatening language may constitute harassment or intimidation
• **File Complaints**: Report to local housing authority or consumer court
• **Legal Remedies**: You can seek injunction against harassment and claim damages

**Immediate Steps**:
1. Send written notice asking landlord to stop demands and threats
2. Continue paying only the agreed rent amount
3. Seek legal consultation if threats escalate
4. Consider filing police complaint if threats are serious

**Legal Provisions**: Rent Control Acts, Consumer Protection Act, and local tenancy laws protect tenants from harassment.

*Consult a local lawyer for jurisdiction-specific advice and immediate legal action.*"""

    elif any(word in question_lower for word in ['rights', 'legal rights']):
        return """⚖️ **Legal Rights Overview:**

• **Fundamental Rights**: Right to equality, freedom of speech, right to life and liberty
• **Criminal Cases**: Right to legal representation, right to remain silent, right to bail
• **Civil Cases**: Right to fair hearing, right to appeal, right to legal remedies
• **Consumer Rights**: Right to safety, right to information, right to choose

*Note: Legal rights vary by jurisdiction. Consult a qualified lawyer for specific advice.*"""

    elif any(word in question_lower for word in ['court', 'procedure', 'process']):
        return """🏛️ **Court Procedures:**

• **Filing**: Submit proper documentation with required fees
• **Service**: Ensure all parties are properly notified
• **Discovery**: Exchange of information between parties
• **Trial**: Presentation of evidence and arguments
• **Judgment**: Court's decision on the matter
• **Appeal**: Option to challenge the decision in higher court

*Procedures may vary by court type and jurisdiction.*"""

    elif any(word in question_lower for word in ['bail', 'anticipatory bail']):
        return """🔓 **Bail Information:**

**Regular Bail**: Applied after arrest, allows temporary release pending trial
**Anticipatory Bail**: Applied before potential arrest in anticipation of charges

**Key Factors**: Severity of offense, flight risk, previous criminal history, likelihood to influence witnesses

*Bail decisions are at court's discretion based on case specifics.*"""

    # Enhanced scenario handling
    elif any(word in question_lower for word in ['harassment', 'threat', 'intimidation', 'blackmail']):
        return """⚠️ **Harassment & Threats Legal Response:**

**Legal Options Available**:
• File police complaint under relevant IPC sections
• Seek restraining order from court
• Document all incidents with dates and evidence
• Consider defamation action if reputation is affected

**Immediate Protection**:
• Inform local police about ongoing threats
• Seek support from family/friends as witnesses
• Avoid being alone with the harasser
• Keep communication records as evidence

*Threats and harassment are criminal offenses. Take immediate legal action.*"""

    elif any(word in question_lower for word in ['contract', 'agreement', 'breach', 'violation']):
        return """📄 **Contract Law Guidance:**

**When Contracts Are Breached**:
• Review the specific terms that were violated
• Check for penalty clauses in the agreement
• Calculate actual damages suffered
• Send legal notice demanding compliance
• File suit for specific performance or damages

**Legal Remedies**: Compensation, specific performance, injunction, or contract termination

*Contract disputes require careful legal analysis of the specific terms.*"""

    else:
        return f"""💬 **Legal Guidance Available**

Regarding your question: "{question}"

I can provide guidance on various legal scenarios including:

• **Property & Housing**: Landlord-tenant disputes, rent issues, eviction matters
• **Criminal Law**: Rights during arrest, bail procedures, criminal charges
• **Civil Disputes**: Contracts, torts, property disputes, family matters
• **Consumer Rights**: Product defects, service issues, unfair practices
• **Workplace Issues**: Employment rights, harassment, wrongful termination

**How I Can Help**: Explain legal concepts, suggest possible remedies, outline court procedures, and guide you on next steps.

*For case-specific strategy and representation, consult with a qualified attorney in your jurisdiction.*

Please provide more details about your specific situation for targeted guidance!"""

def process_chat_message(message, mode='general', document_text=None):
    """
    Process a chat message using LLaMA AI model for both document and general questions.
    """
    try:
        if mode == 'document' and document_text and document_text.strip():
            # Use document-specific analysis with LLaMA
            if LLAMA_AVAILABLE:
                answer = document_qa_llama(document_text, message)
            else:
                answer = document_qa_simple(document_text, message)
                
            return {
                'response': answer,
                'mode': 'document',
                'success': True,
                'using_document': True,
                'ai_powered': LLAMA_AVAILABLE
            }
        else:
            # Use general legal chat with LLaMA
            if LLAMA_AVAILABLE:
                answer = general_legal_chat_llama(message)
            else:
                answer = general_legal_chat_simple(message)
                
            return {
                'response': answer,
                'mode': 'general',
                'success': True,
                'using_document': False,
                'ai_powered': LLAMA_AVAILABLE
            }
    
    except Exception as e:
        return {
            'response': f"I apologize, but I encountered an error: {str(e)}",
            'mode': mode,
            'success': False,
            'error': str(e)
        }

def main():
    """
    Main function to handle input/output with the Node.js API.
    """
    try:
        start_time = time.time()
        
        # Read input from stdin
        input_data = sys.stdin.read().strip()
        
        if not input_data:
            raise ValueError("No input data received")
        
        # Parse JSON input
        try:
            data = json.loads(input_data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON input: {e}")
        
        # Extract parameters
        message = data.get('message', '').strip()
        mode = data.get('mode', 'general')
        document_text = data.get('documentText')
        
        # Debug logging
        print(f"DEBUG: Message: {message}", file=sys.stderr)
        print(f"DEBUG: Mode: {mode}", file=sys.stderr)
        print(f"DEBUG: Has document_text: {bool(document_text)}", file=sys.stderr)
        if document_text:
            print(f"DEBUG: Document length: {len(document_text)}", file=sys.stderr)
            print(f"DEBUG: Document preview: {document_text[:200]}...", file=sys.stderr)
        
        if not message:
            raise ValueError("Message is required")
        
        # Process the message
        result = process_chat_message(message, mode, document_text)
        
        # Add timestamp
        result['timestamp'] = time.time()
        result['processing_time'] = time.time() - start_time
        
        # Output JSON response
        print(json.dumps(result, ensure_ascii=False, indent=None))
        
    except Exception as e:
        # Error response
        error_response = {
            'response': "I'm sorry, I encountered an error while processing your request. Please try again.",
            'mode': 'general',
            'success': False,
            'error': str(e)
        }
        print(json.dumps(error_response, ensure_ascii=False, indent=None))
        sys.exit(1)

if __name__ == '__main__':
    main()
