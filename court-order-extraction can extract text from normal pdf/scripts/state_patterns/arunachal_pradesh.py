"""
Arunachal Pradesh specific patterns for court order extraction
Based on Arunachal Pradesh court document formats
"""

import re

ARUNACHAL_PRADESH_PATTERNS = {
    # Case number patterns for Arunachal Pradesh courts
    'case_number': [
        r'BSR/ABA\s+No\.?\s*(\d+/\d+)',                    # BSR/ABA No.01/23
        r'DMJ\s+PS\s+Case\s+No\.?\s*(\d+/\d+)',           # DMJ PS Case No.02/23
        r'Case\s+No\.?\s*(\d+/\d+)',                       # General case number
        r'No\.?\s*(\d+/\d+)',                              # Simple number pattern
    ],

    # Judge name patterns
    'judge_name': [
        r'Present:\s+Mr\.?\s+([A-Z][a-z]+\s+[A-Z][a-z]+),?\s+APJS',  # Mr. Tage Halley, APJS
        r'Present:\s+([A-Z][a-z]+\s+[A-Z][a-z]+),?\s+APJS',         # Without Mr.
        r'([A-Z][a-z]+\s+[A-Z][a-z]+),?\s+APJS',                    # Direct name with APJS
        r'([A-Z][a-z]+\s+[A-Z][a-z]+),?\s+Addl\.?\s+Sessions\s+Judge', # With title
    ],

    # Court name patterns
    'court_name': [
        r'IN\s+THE\s+COURT\s+OF\s+(ADDITIONAL\s+DISTRICT\s+&\s+SESSIONS\s+JUDGE[^,]+(?:,[^,]+){0,3})',
        r'THE\s+COURT\s+OF\s+(ADDITIONAL\s+DISTRICT\s+&\s+SESSIONS\s+JUDGE[^,]+)',
        r'COURT\s+OF\s+(ADDITIONAL\s+DISTRICT\s+&\s+SESSIONS\s+JUDGE[^,]+)',
        r'(ADDITIONAL\s+DISTRICT\s+&\s+SESSIONS\s+JUDGE[^,]+,\s+[^,]+,\s+[^,]+,\s+ARUNACHAL\s+PRADESH)',
    ],

    # Order date patterns
    'order_date': [
        r'Date:\s*(\d{1,2}\.?\d{1,2}\.?\d{4})',            # Date: 13.01.2023
        r'dated?\s*(\d{1,2}\.?\d{1,2}\.?\d{4})',           # dated 13.01.2023
        r'(\d{1,2}th\s+day\s+of\s+\w+\s+\d{4})',          # 13th day of January 2023
        r'on\s+this\s+(\d{1,2}th\s+day\s+of\s+\w+\s+\d{4})', # on this 13th day of January 2023
    ],

    # Petitioner/Applicant patterns
    'petitioner_name': [
        r'applicant\s+accused\s+Sh\.?\s+([A-Z][a-zA-Z\s@]+?)(?:\s+U/S|—vs—|\s+through)',  # applicant accused Sh. Name
        r'Sh\.?\s+([A-Z][a-zA-Z\s@]+?)(?:\s*—vs—|\s*vs\.?\s*)',                          # Sh. Name—vs—
        r'applicant\s+([A-Z][a-zA-Z\s@]+?)(?:\s+U/S|—vs—)',                             # applicant Name
        r'filed\s+by\s+(?:the\s+)?(?:applicant\s+)?([A-Z][a-zA-Z\s@]+?)(?:\s+U/S|—vs—)', # filed by applicant Name
    ],

    # Respondent patterns
    'respondent_name': [
        r'—vs—\s*(State\s+of\s+AP?)',                      # —vs—State of AP
        r'vs\.?\s*(State\s+of\s+AP?)',                     # vs State of AP
        r'against\s+(State\s+of\s+AP?)',                   # against State of AP
        r'—vs—\s*(State\s+of\s+Arunachal\s+Pradesh)',      # Full state name
    ],

    # Legal sections patterns
    'statutes_offences': [
        r'U/S(?:\(s\))?:?\s*((?:\d+/?)+(?:/\d+)*(?:-\w+)*)',  # U/S(s): 341/324/427/34-IPC
        r'under\s+Section\s+((?:\d+/?)+(?:/\d+)*)',           # under Section numbers
        r'U/S-?(\d+(?:/\d+)*(?:-\w+)*)',                     # U/S-438, U/S-341/324/427/34-IPC
        r'Section\s+(\d+(?:-\w+)*)',                          # Section 438
    ],

    # FIR/Police case patterns  
    'fir_crime_no': [
        r'DMJ\s+PS\s+Case\s+No\.?\s*(\d+/\d+)',           # DMJ PS Case No.02/23
        r'PS\s+Case\s+No\.?\s*(\d+/\d+)',                 # PS Case No.
        r'Crime\s+No\.?\s*(\d+/\d+)',                     # Crime No.
        r'FIR\s+No\.?\s*(\d+/\d+)',                       # FIR No.
    ],

    # Police station patterns
    'police_station': [
        r'(DMJ)\s+PS\s+Case',                             # DMJ PS Case
        r'connection\s+with\s+([A-Z]+)\s+PS',             # in connection with DMJ PS
        r'([A-Z]{2,4})\s+Police\s+Station',              # DMJ Police Station
        r'PS\s+([A-Z]+)',                                 # PS DMJ
    ],

    # Advocates/Counsel patterns
    'advocates': [
        r'through\s+his\s+Ld\.?\s+counsel\s+Mr\.?\s+([A-Z][a-zA-Z\s]+)', # through his Ld. counsel Mr. Name
        r'Ld\.?\s+counsel\s+Mr\.?\s+([A-Z][a-zA-Z\s]+)',                # Ld. counsel Mr. Name  
        r'counsel\s+Mr\.?\s+([A-Z][a-zA-Z\s]+)',                        # counsel Mr. Name
        r'represented\s+by\s+([A-Z][a-zA-Z\s]+)',                       # represented by Name
    ],

    # Document type patterns
    'document_type': [
        r'(pre-arrest\s+bail\s+application)',             # pre-arrest bail application
        r'(anticipatory\s+bail)',                         # anticipatory bail
        r'(bail\s+application)',                          # bail application
        r'U/S-?438\s+of\s+Cr\.?\s+PC',                    # U/S-438 of Cr. PC (indicates bail)
    ],

    # Decision/Order patterns
    'decision': [
        r'this\s+(anticipatory\s+bail[^.]+is\s+not\s+maintainable)', # anticipatory bail is not maintainable
        r'(this\s+matter\s+stands\s+disposed\s+of)',                # this matter stands disposed of
        r'court\s+is\s+of\s+the\s+(belief\s+that[^.]+)',           # court is of the belief that
        r'(offence[^.]+remains\s+to\s+be\s+a\s+bailable\s+section)', # offence remains to be a bailable section
    ],

    # Court location patterns
    'court_location': [
        r'BASAR,\s+WESTERN\s+ZONE,\s+LEPARADA\s+DISTRICT', # Court location
        r'here\s+at\s+([A-Z][a-z]+)',                      # here at Basar
    ]
}

# Party-specific patterns for Arunachal Pradesh
ARUNACHAL_PRADESH_PARTY_PATTERNS = {
    'petitioner': {
        'name': [
            r'applicant\s+accused\s+Sh\.?\s+([A-Z][a-zA-Z\s@]+?)(?:\s+U/S|—vs—)',
            r'Sh\.?\s+([A-Z][a-zA-Z\s@]+?)(?:\s*—vs—|\s*vs\.?\s*)',
        ],
        'alias': [
            r'([A-Z][a-zA-Z\s]+)\s+@\s+([A-Z][a-zA-Z\s]+)',  # Ripe Maro @ Yigam
        ]
    },
    'respondent': {
        'name': [
            r'—vs—\s*(State\s+of\s+AP?)',
            r'vs\.?\s*(State\s+of\s+AP?)',
            r'—vs—\s*(State\s+of\s+Arunachal\s+Pradesh)',
        ]
    }
}

# Export the patterns
__all__ = ['ARUNACHAL_PRADESH_PATTERNS', 'ARUNACHAL_PRADESH_PARTY_PATTERNS']
