# 🏛️ Advanced Legal AI Platform

**AI-Powered Legal Document Processing with OCR & Python ML**

A comprehensive legal document analysis platform that combines Next.js frontend with Python ML backend, featuring advanced OCR capabilities, AI-powered document analysis, and LLaMA integration for intelligent legal assistance.

## ✨ Features

### 🔍 **Document Processing**
- **Advanced OCR**: PaddleOCR integration for accurate text extraction
- **Multi-language Support**: Process documents in multiple languages
- **Smart Detection**: Automatic document type detection and classification
- **PDF Processing**: Extract text from complex legal documents

### 🤖 **AI-Powered Analysis**
- **LLaMA 3.1 Integration**: Advanced AI for legal document analysis
- **Intelligent Q&A**: Ask questions about your documents
- **Metadata Extraction**: Extract 27+ metadata fields automatically
- **Legal Provision Detection**: Identify key legal sections and provisions

### 💬 **Interactive Chat Assistant**
- **Dual Mode Operation**: 
  - 📄 **Document Mode**: Analyze uploaded documents
  - 💬 **General Mode**: Ask general legal questions
- **Real-time Processing**: Live typing indicators and loading states
- **Scenario-based Guidance**: Handle complex legal scenarios
- **Enhanced User Experience**: Modern chat interface with animations

### 📊 **Comprehensive Analysis**
- **Party Identification**: Automatically detect involved parties
- **Date & Timeline Extraction**: Important dates and deadlines
- **Court Information**: Extract court names and case details
- **Legal Citations**: Identify referenced laws and precedents

## 🚀 Tech Stack

### Frontend
- **Next.js 14.2.16**: Modern React framework
- **TailwindCSS**: Utility-first CSS framework
- **Shadcn/ui**: Beautiful UI components
- **Lucide Icons**: Modern icon library

### Backend
- **Python 3.x**: Core processing engine
- **PaddleOCR**: Advanced OCR capabilities
- **LangChain**: AI framework integration
- **Ollama**: Local LLaMA model hosting

### AI & ML
- **LLaMA 3.1:8b**: Large language model for legal analysis
- **spaCy/NLTK**: Natural language processing
- **Transformers**: Hugging Face model integration

## 📦 Installation

### Prerequisites
- Node.js 18+ and npm/pnpm
- Python 3.8+
- Ollama (for LLaMA model)

### 1. Clone the Repository
```bash
git clone https://github.com/DeepakAstaya001/Lawbuddy.git
cd Lawbuddy
```

### 2. Frontend Setup
```bash
cd "court-order-extraction can extract text from normal pdf"
npm install
# or
pnpm install
```

### 3. Python Environment Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install PaddlePaddle (CPU build; see requirements.txt for the GPU command)
pip install paddlepaddle

# Install Python dependencies
pip install -r requirements.txt
```

### 4. LLaMA Model Setup
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull LLaMA model
ollama pull llama3.1:8b
```

### 5. Environment Configuration
Create a `.env.local` file in the frontend directory and point the chat API at your virtual environment's Python (defaults to `python` on PATH):
```env
PYTHON_PATH=/path/to/Lawbuddy/venv/bin/python
```

## 🎯 Usage

### 1. Start the Development Server
```bash
cd "court-order-extraction can extract text from normal pdf"
npm run dev
```

### 2. Access the Application
Open [http://localhost:3000](http://localhost:3000) in your browser.

### 3. Upload and Process Documents
1. Navigate to the "Upload & Process" tab
2. Select a legal document (PDF)
3. Configure processing options
4. Click "Process Document"

### 4. Interact with AI Assistant
1. Go to the "Legal Assistant" tab
2. Choose between:
   - **Document Mode**: Ask questions about your uploaded document
   - **General Mode**: Ask general legal questions
3. Use quick action buttons or type custom questions

### 5. Command-Line Processing
Run the full pipeline on a single PDF without the web app:
```bash
python main.py "path/to/court_order.pdf"
```
Results are written to a folder named after the PDF under `output/`.

## 🏗️ Project Structure

```
Lawbuddy/
├── court-order-extraction can extract text from normal pdf/  # Next.js Frontend
│   ├── app/                    # App router pages and API routes
│   ├── components/             # React components
│   ├── lib/                    # Utilities
│   └── scripts/                # Python processing used by the API
│       ├── clean_processor.py      # Document processing pipeline
│       ├── chat_handler_working.py # Chat API handler
│       ├── llama.py                # LLaMA integration
│       └── ocr.py                  # OCR processing
├── main.py                     # Command-line pipeline (OCR + metadata + summary)
├── metadata/                   # Metadata processing modules
├── ocr/                        # OCR utilities
└── utils/                      # LLaMA helpers and output management
```

## 🔧 Configuration

### Python Dependencies
Key packages in `requirements.txt`:
- `paddleocr`: OCR processing
- `langchain-ollama`: LLaMA integration
- `spacy`: NLP processing
- `opencv-python`: Image processing

### Frontend Dependencies
Key packages in `package.json`:
- `next`: React framework
- `tailwindcss`: Styling
- `@radix-ui`: UI components
- `lucide-react`: Icons

## 🤝 API Endpoints

### Document Processing
- `POST /api/process-document-complete`: Complete document processing
- `POST /api/chat`: Chat with AI assistant

### Chat Modes
- **Document Mode**: Analyzes uploaded document content
- **General Mode**: Provides general legal guidance

## 📝 Key Features in Detail

### Document Processing Pipeline
1. **File Upload**: Secure file handling with validation
2. **OCR Processing**: Extract text using PaddleOCR
3. **Metadata Extraction**: Extract 27+ metadata fields
4. **AI Analysis**: LLaMA-powered content analysis
5. **Results Display**: Comprehensive results with download options

### AI Chat Assistant
- **Mode Selection**: Switch between document and general modes
- **Loading States**: Real-time feedback with animations
- **Quick Actions**: Pre-built common questions
- **Timeout Handling**: Graceful handling of long AI responses

### Performance Optimizations
- **Timeout Management**: 30-second timeout for AI responses
- **Loading Animations**: Visual feedback during processing
- **Error Handling**: Comprehensive error management
- **Fallback Responses**: Graceful degradation

## 🛠️ Development

### Running in Development Mode
```bash
# Frontend
npm run dev

# Ensure Python virtual environment is activated
source venv/bin/activate
```

### Building for Production
```bash
npm run build
npm start
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **PaddleOCR**: For excellent OCR capabilities
- **LLaMA**: For advanced language model integration
- **Next.js**: For the robust frontend framework
- **Shadcn/ui**: For beautiful UI components

## 📞 Support

For support, please open an issue in the GitHub repository or contact the development team.

---

**Built with ❤️ for the legal community**
