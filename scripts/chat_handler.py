#!/usr/bin/env python3
"""
Chat Handler for Legal AI Assistant
Processes chat requests from the frontend and returns responses using LLaMA model.
"""

import sys
import json
import os
from pathlib import Path

# Add the scripts directory to Python path
scripts_dir = Path(__file__).parent
sys.path.insert(0, str(scripts_dir))

# Import the llama functions
try:
    from llama import interactive_qa_session, general_legal_chat
except ImportError as e:
    print(f"Error importing llama functions: {e}", file=sys.stderr)
    sys.exit(1)

def process_chat_message(message, mode='general', document_text=None):
    """
    Process a chat message using the appropriate LLaMA function.
    
    Args:
        message (str): The user's message/question
        mode (str): 'document' or 'general' mode
        document_text (str): Document text for document mode
    
    Returns:
        dict: Response with answer and metadata
    """
    try:
        if mode == 'document' and document_text:
            # Use document-specific Q&A
            answer = interactive_qa_session(document_text, message, single_question=True)
        else:
            # Use general legal chat
            answer = general_legal_chat(message)
        
        return {
            'response': answer,
            'mode': mode,
            'success': True
        }
    
    except Exception as e:
        error_msg = f"Error processing message: {str(e)}"
        print(error_msg, file=sys.stderr)
        
        # Return a fallback response
        return {
            'response': "I apologize, but I'm experiencing technical difficulties. Please try again later or rephrase your question.",
            'mode': mode,
            'success': False,
            'error': str(e)
        }

def main():
    """
    Main function to handle input/output with the Node.js API.
    """
    try:
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
        
        if not message:
            raise ValueError("Message is required")
        
        # Process the message
        result = process_chat_message(message, mode, document_text)
        
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
