from langchain_ollama.llms import OllamaLLM # type: ignore

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

def interactive_qa_session():
    """
    Interactive Q&A session with the legal document
    """
    # Load the legal document
    try:
        with open("raw_full_text.txt", 'r') as file:
            document_text = file.read()
        print("📄 Legal document loaded successfully!")
        print("=" * 60)
        print("📋 Document Preview:")
        print(document_text[:300] + "..." if len(document_text) > 300 else document_text)
        print("=" * 60)
    except FileNotFoundError:
        print("❌ Error: raw_full_text.txt not found!")
        return
    
    print("\n🤖 Legal Document Q&A System")
    print("=" * 60)
    print("You can now ask questions about the legal document.")
    print("💡 TIP: Type 'summary' to get a formatted court order summary")
    print("Type 'exit' or 'quit' to end the session.")
    print("=" * 60)
    
    while True:
        question = input("\n❓ Your Question: ").strip()
        
        if question.lower() in ['exit', 'quit', '']:
            print("👋 Session ended. Goodbye!")
            break
        
        # Check if user wants a summary
        if question.lower() in ['summary', 'summarize', 'give me summary', 'court order summary','give me a summary of this document','give me the summary of this document','summarize this document','summarize this court order']:
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
        else:
            print("\n🤔 Thinking...")
            try:
                answer = answer_from_data(document_text, question)
                print(f"\n💡 Answer:\n{answer}")
                print("-" * 40)
            except Exception as e:
                print(f"❌ Error: {e}")


if __name__ == "__main__":
    print("🚀 LEGAL DOCUMENT Q&A SYSTEM")
    print("=" * 60)
    print("Choose an option:")
    print("1. Interactive Q&A Session")
    print("2. Test with predefined questions")
    print("3. Single question mode")
    print("4. Generate Court Order Summary")
    
    choice = input("\nEnter your choice (1/2/3/4): ").strip()
    
    if choice == "1":
        interactive_qa_session()
    elif choice == "2":
        with open("raw_full_text.txt", 'r') as file:
            document_text = file.read()
        
        question = input("Enter your question: ")
        answer = answer_from_data(document_text, question)
        print(f"\nAnswer: {answer}")
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
        except Exception as e:
            print(f"❌ Error generating summary: {e}")
    else:
        print("Invalid choice. Running interactive session by default.")
        interactive_qa_session()