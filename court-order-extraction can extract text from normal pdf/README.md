# PDF Text Extraction System

A simple system to extract text from scanned PDFs using PaddleOCR.

## Features

- ✅ Upload PDF files
- ✅ Extract text from scanned PDFs using PaddleOCR
- ✅ Download extracted text
- ✅ Clean, simple dashboard
- ✅ Python backend with JavaScript/React frontend

## Setup

### 1. Install Node.js dependencies
\`\`\`bash
npm install
\`\`\`

### 2. Install Python dependencies
\`\`\`bash
npm run setup-python
# or manually:
pip install paddleocr PyMuPDF PyPDF2 Pillow numpy
\`\`\`

### 3. Run the application
\`\`\`bash
npm run dev
\`\`\`

## Usage

1. Open http://localhost:3000
2. Upload a PDF file
3. Click "Extract Text"
4. Download the extracted text

## Requirements

- Node.js 18+
- Python 3.7+
- PaddleOCR for scanned PDF processing

## File Structure

\`\`\`
├── app/
│   ├── layout.js          # App layout
│   ├── page.js            # Main dashboard
│   └── api/
│       └── extract-pdf/   # PDF processing API
├── scripts/
│   ├── extract_text.py    # Python text extraction
│   └── install_requirements.py # Setup script
└── components/ui/         # UI components
