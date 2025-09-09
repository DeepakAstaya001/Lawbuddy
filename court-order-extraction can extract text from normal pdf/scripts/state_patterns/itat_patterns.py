# Regex patterns for INCOME TAX APPELLATE TRIBUNAL (ITAT) courts

PATTERNS = {
    "court_name": [
        r"IN THE (INCOME TAX APPELLATE TRIBUNAL[^\n]*)",
        r"(INCOME TAX APPELLATE TRIBUNAL[^\n]*)",
        r"IN THE ([^\n]*APPELLATE TRIBUNAL[^\n]*)",
        r"([^\n]*APPELLATE TRIBUNAL[^\n]*)",
        r"INCOME TAX APPELLATE TRIBUNAL,\s*(CUTTACK[^\n]*)",  # Cuttack bench format
        r"(INCOME TAX APPELLATE TRI.*CUTTACK[^\n]*)",  # Split line format
        r"IN THE (INCOME TAX APPELLATE TRI[\s\S]*?CUTTACK[^\n]*)",  # Split across multiple lines
        r"(INCOME TAX APPELLATE TRI[\s\S]*?CUTTACK)"  # Split format without full tribunal word
    ],
    
    "case_number": [
        r"ITA\s+no\.?(\d+\/[A-Za-z]+\.?\/\d{4})",  # ITA no.227/Nag./2022
        r"ITA\s+Nos\.(\d+\s+to\s+\d+\/[A-Za-z]+\/\d{4})",  # ITA Nos.271 to 274/CTK/2024
        r"(ITA\s+no\.?\d+\/[A-Za-z]+\.?\/\d{4})",  # Full ITA number
        r"(ITA\s+Nos\.\d+\s+to\s+\d+\/[A-Za-z]+\/\d{4})",  # Full range ITA numbers
        r"(ITA\s+Nos\.\d+\s+to\s+\d+\/[A-Za-z]+\/\d{2})",  # Partial case number
        r"(Appeal\s+No\.?\s*\d+\s+of\s+\d{4})",
        r"([A-Z]+\s+no\.?\d+\/[A-Za-z]+\.?\/\d{4})"  # Generic tribunal case format
    ],
    
    "alternate_case_number": [
        r"Assessment Year\s*:?\s*(\d{4}[–\-]\d{2,4})",  # Assessment Year : 2017–18
        r"A\.Y\.?\s*(\d{4}[–\-]\d{2,4})",  # A.Y. 2017–18
        r"for the assessment year\s+(\d{4}[–\-]\d{2,4})",
        r"ment Years\s*:\s*(\d{4}[–\-]\d{2,4}(?:,\d{4}[–\-]\d{2,4})*(?:,\d{4})?)",  # Allow partial final year
        r"Assessment Years\s*:\s*(\d{4}[–\-]\d{2,4}(?:,\d{4}[–\-]\d{2,4})*)",  # Multiple assessment years
        r"ITA\s+no\.?(\d+\/[A-Za-z]+\.?\/\d{4})\s*\n.*Assessment Year\s*:?\s*(\d{4}[–\-]\d{2,4})"  # Combined pattern
    ],
    
    "order_date": [
        r"Order dictated and pronounced in the open court on\s+(\d{1,2}\/\d{1,2}\/\d{4})",  # Cuttack format
        r"Dated\s+(\d{1,2}\/\d{1,2}\/\d{4})",  # Cuttack; Dated 29/08/2024
        r"Date of Order\s*[–\-:]\s*(\d{1,2}\/\d{1,2}\/\d{4})",  # Date of Order – 02/09/2024
        r"Date of Pronouncement\s*[–\-:]\s*(\d{1,2}\/\d{1,2}\/\d{4})",  # Date of Pronouncement
        r"Date of Order\s*[–\-:]\s*(\d{1,2}\.\d{1,2}\.\d{4})",  # Date format with dots
        r"dated\s+(\d{1,2}\/\d{1,2}\/\d{4})",  # dated 31/05/2022
        r"(\d{1,2}\/\d{1,2}\/\d{4})",  # Generic date format
        r"(\d{1,2}\.\d{1,2}\.\d{4})"   # Generic date format with dots
    ],
    
    "judge_name": [
        r"BEFORE\s+(SHRI\s+[^,]+,\s*JUDICIAL MEMBER\s+AND\s+SHRI\s+[^,]+,\s*ACCOUNTANT[,\s]*MEMBER)",  # Full bench
        r"BEFORE\s+(SHRI\s+[^,]+,\s*JUDICIAL MEMBER)",  # Single member - Cuttack format
        r"\(([A-Z][a-z]+\s+[A-Z][a-z]+)\)\s*\n\s*JUDICIAL MEMBER",  # (George Mathan) JUDICIAL MEMBER
        r"Sd/-\s*\n[^\n]*\(([^)]+)\)\s*\n[^\n]*JUDICIAL MEMBER",  # Signature format
        r"Sd/-\s*\n\s*([A-Z\.\s]+)\s*\n\s*JUDICIAL MEMBER\s*\n[^\n]*\n[^\n]*\n[^\n]*\n[^\n]*\n\s*Sd/-\s*\n\s*([A-Z\.\s]+)\s*\n\s*ACCOUNTANT MEMBER",  # Both signatures
        r"PER\s+([^,\n]+),?\s*A\.M\.", # PER K.M. ROY, A.M.
        r"PER\s+([^,\n]+),?\s*J\.M\.", # PER [NAME], J.M.
        r"SHRI\s+([^,]+),\s*JUDICIAL MEMBER",  # SHRI V. DURGA RAO, JUDICIAL MEMBER
        r"SHRI\s+([^,]+),\s*ACCOUNTANT[,\s]*MEMBER"  # SHRI K.M. ROY, ACCOUNTANT, MEMBER
    ],
    
    "bench": [
        r"BEFORE\s+(SHRI\s+[^,]+,\s*JUDICIAL MEMBER\s+AND\s+SHRI\s+[^,]+,\s*ACCOUNTANT[,\s]*MEMBER)",
        r"(CUTTACK\s+'SMC'\s+BENCH[^\n]*)",  # Cuttack SMC bench
        r"BEFORE\s+([^\n]+MEMBER[^\n]*)",
        r"(NAGPUR BENCH[^\n]*)",
        r"([A-Z]+\s+BENCH[^\n]*)",
        r"'SMC'\s+BENCH",  # Single Member Court
        r"Division Bench",
        r"Single Bench"
    ],
    
    "document_type": [
        r"(O\s*R\s*D\s*E\s*R)",  # O R D E R (spaced format)
        r"(ORDER)",
        r"(JUDGMENT)",
        r"(DECISION)",
        r"Income Tax Appellate Tribunal.*?(Order|Judgment|Decision)",
        r"Appellate.*?(Order|Judgment|Decision)"
    ],
    
    "counsel": [
        {
            "pattern": r"Assessee by\s*:\s*([^\n]+)",
            "for": "Appellant/Assessee"
        },
        {
            "pattern": r"Revenue by\s*:\s*([^\n]+)",
            "for": "Respondent/Revenue"
        },
        {
            "pattern": r"For (?:the )?(?:Assessee|Appellant)(?:s)?[^\n]*[:-]\s*([^\n]+)",
            "for": "Appellant/Assessee"
        },
        {
            "pattern": r"For (?:the )?(?:Revenue|Department|Commissioner)(?:s)?[^\n]*[:-]\s*([^\n]+)",
            "for": "Respondent/Revenue"
        }
    ],
    
    "parties": [
        {
            "pattern": r"([A-Z][A-Za-z\s]*(?:Pvt\.?\s*Ltd\.?|Private Limited|Limited|Company|Corporation)[^\n]*)",
            "type": "company"
        },
        {
            "pattern": r"^([A-Z][a-z]+\s+[A-Z][a-z]+),?\s*Plot No",  # Trilochan Mishra, Plot No.97
            "type": "individual"
        },
        {
            "pattern": r"^([A-Z][a-z]+\s+[A-Z][a-z]+\s+[A-Z][a-z]+)\s*$",  # Exact three-word names on separate lines
            "type": "individual"
        },
        {
            "pattern": r"((?:Dy\.?\s*)?Commissioner of Income Tax[^\n]*)",
            "type": "government"
        },
        {
            "pattern": r"(Assistant Commissioner of Income Tax[^\n]*)",
            "type": "government"
        },
        {
            "pattern": r"(Income Tax Officer[^\n]*)",
            "type": "government"
        }
    ]
}
