"use client"

import { useState, useRef } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Switch } from "@/components/ui/switch"
import {
  Upload,
  FileText,
  CheckCircle,
  AlertCircle,
  Download,
  Scale,
  Users,
  Volume2,
  VolumeX,
  Brain,
  BookOpen,
  Languages,
  Zap,
  Eye,
  FileCheck,
  Gavel,
  Search,
  Bot,
  Clock,
  Scan,
  FileImage,
  MapPin,
  Send,
  User,
  MessageCircle,
  HelpCircle,
  Sparkles,
  Loader2,
  X
} from "lucide-react"
import { useToast } from "@/hooks/use-toast"
import LegalChatbot from "@/components/LegalChatbot"

export default function AdvancedLegalAIPlatform() {
  const [file, setFile] = useState(null)
  const [processing, setProcessing] = useState(false)
  const [progress, setProgress] = useState(0)
  const [currentStep, setCurrentStep] = useState("")
  const [extractedData, setExtractedData] = useState(null)
  const [activeTab, setActiveTab] = useState("upload")
  const [summaryLength, setSummaryLength] = useState("medium")
  const [selectedLanguage, setSelectedLanguage] = useState("en")
  const [isRecording, setIsRecording] = useState(false)
  const [voiceRecording, setVoiceRecording] = useState(null)
  const [isSpeaking, setIsSpeaking] = useState(false)
  const [showChatbot, setShowChatbot] = useState(false)
  const [chatMessages, setChatMessages] = useState([])
  const [chatInput, setChatInput] = useState("")
  const [isChatLoading, setIsChatLoading] = useState(false)
  const [chatMode, setChatMode] = useState("general") // "document" or "general"
  const [qaQuery, setQaQuery] = useState("")
  const [qaResponse, setQaResponse] = useState("")
  const [mobileScanning, setMobileScanning] = useState(false)
  const [ocrEnabled, setOcrEnabled] = useState(true)
  const [signatureDetection, setSignatureDetection] = useState(true)
  const [autoTranslate, setAutoTranslate] = useState(false)
  const [documentType, setDocumentType] = useState("unknown")
  const [isScanned, setIsScanned] = useState(false)

  const mediaRecorderRef = useRef(null)
  const videoRef = useRef(null)
  const canvasRef = useRef(null)
  const { toast } = useToast()

  const languages = [
    { code: "en", name: "English" },
    { code: "hi", name: "हिंदी (Hindi)" },
    { code: "bn", name: "বাংলা (Bengali)" },
    { code: "te", name: "తెలుగు (Telugu)" },
    { code: "mr", name: "मराठी (Marathi)" },
    { code: "ta", name: "தமிழ் (Tamil)" },
    { code: "gu", name: "ગુજરાતી (Gujarati)" },
    { code: "kn", name: "ಕನ್ನಡ (Kannada)" },
    { code: "ml", name: "മലയാളം (Malayalam)" },
    { code: "pa", name: "ਪੰਜਾਬੀ (Punjabi)" },
    { code: "or", name: "ଓଡ଼ିଆ (Odia)" },
    { code: "as", name: "অসমীয়া (Assamese)" },
    { code: "ur", name: "اردو (Urdu)" },
  ]

  const documentTypes = [
    { type: "Court Order", icon: Gavel, color: "bg-blue-500" },
    { type: "FIR", icon: AlertCircle, color: "bg-red-500" },
    { type: "Judgment", icon: Scale, color: "bg-green-500" },
    { type: "Affidavit", icon: FileCheck, color: "bg-purple-500" },
  ]

  const handleFileUpload = (event) => {
    const selectedFile = event.target.files?.[0]
    if (selectedFile) {
      if (selectedFile.type !== "application/pdf" && !selectedFile.type.startsWith("image/")) {
        toast({
          title: "Invalid file type",
          description: "Please upload a PDF file or image.",
          variant: "destructive",
        })
        return
      }

      if (selectedFile.size > 100 * 1024 * 1024) {
        toast({
          title: "File too large",
          description: "File size must be under 100MB.",
          variant: "destructive",
        })
        return
      }

      setFile(selectedFile)
      // Detect if it's likely a scanned document based on file type
      setIsScanned(selectedFile.type.startsWith("image/"))

      toast({
        title: "File uploaded",
        description: `${selectedFile.name} is ready for processing.`,
      })
    }
  }

  const processDocument = async () => {
    if (!file) return

    setProcessing(true)
    setProgress(0)
    setActiveTab("processing")

    try {
      // Create FormData for file upload
      const formData = new FormData()
      formData.append("file", file)
      formData.append("ocrEnabled", ocrEnabled.toString())
      formData.append("signatureDetection", signatureDetection.toString())
      formData.append("summaryLength", summaryLength)
      formData.append("language", selectedLanguage)

      // Simulate progress updates
      const steps = [
        "Uploading document...",
        "Detecting document type...",
        isScanned || file.type.startsWith("image/") ? "Running OCR analysis..." : "Extracting text from PDF...",
        "Analyzing document structure...",
        "Extracting legal entities...",
        "Classifying document type...",
        "Generating summary...",
        "Analyzing complexity...",
        "Finalizing results...",
      ]

      // Start progress simulation
      let currentStepIndex = 0
      const progressInterval = setInterval(() => {
        if (currentStepIndex < steps.length) {
          setCurrentStep(steps[currentStepIndex])
          setProgress(((currentStepIndex + 1) / steps.length) * 90) // Leave 10% for final processing
          currentStepIndex++
        }
      }, 800)

      // Call the complete Python processing API
      /* ------------------------------------------------------------------
         Call the Complete Python processing API with integrated pipeline
         This uses the full processing pipeline from scripts/integrated_processor.py
         which combines OCR, metadata extraction, and AI summarization
      ------------------------------------------------------------------ */
      const response = await fetch("/api/process-document-complete", {
        method: "POST",
        body: formData,
      })

      clearInterval(progressInterval)

      const raw = await response.text()
      let result
      try {
        result = JSON.parse(raw)
      } catch {
        // Server returned non-JSON payload; wrap it so UI can still display it
        result = { error: raw || "Unknown server response" }
      }

      if (!response.ok || result.error) {
        toast({
          title: "Processing failed",
          description: result.error || `HTTP ${response.status} error`,
          variant: "destructive",
        })
        // continue so user can inspect details
      }

      // Complete progress
      setCurrentStep("Processing complete!")
      setProgress(100)

      // Add some additional UI-friendly data
      const enhancedResult = {
        ...result,
        // Add fullText for chat functionality
        fullText: result.extractedText || "",
        // Ensure we have display-friendly data
        displayData: {
          fileName: result.fileName || file.name,
          fileSize: result.fileSize || file.size,
          fileType: result.fileType || file.type,
          processingMethod: result.extractionMethod || "Unknown",
          documentCategory: result.documentAnalysis?.type || "Legal Document",
          extractedEntities: result.documentAnalysis?.keyEntities || {},
          hasError: !!result.error,
          errorMessage: result.error || null,
          textPreview: result.extractedText ? result.extractedText.substring(0, 500) + "..." : "No text extracted",
          summaryGenerated: !!result.summary && result.summary.length > 10,
          entitiesFound: result.structureAnalysis?.entities_found || 0,
          processingSuccess: result.success !== false && !result.error && result.extractedText && result.extractedText.length > 50,
          metadataExtracted: result.metadata && Object.keys(result.metadata).length > 0
        },
      }

      setExtractedData(enhancedResult)
      setActiveTab("results")
      
      // Auto-switch to document mode when document is processed
      if (enhancedResult.fullText && enhancedResult.fullText.length > 0) {
        setChatMode("document")
      }

      // Show appropriate toast message
      if (enhancedResult.displayData.processingSuccess) {
        toast({
          title: "Complete Processing Finished",
          description: `Successfully extracted ${enhancedResult.wordCount || 0} words and ${enhancedResult.displayData.metadataExtracted ? 'comprehensive metadata' : 'basic information'} from ${enhancedResult.displayData.fileName}`,
        })
      } else if (enhancedResult.error) {
        toast({
          title: "Processing completed with issues",
          description: enhancedResult.error,
          variant: "destructive",
        })
      } else {
        toast({
          title: "Processing complete",
          description: "Document processed but limited text was extracted.",
        })
      }
    } catch (error) {
      console.error("Processing error:", error)

      // Create fallback data with file information
      const fallbackData = {
        error: "Network or processing error occurred",
        extractedText: `Failed to process ${file.name}. Please check your connection and try again.`,
        fullText: `Failed to process ${file.name}. Please check your connection and try again.`,
        summary: "Processing failed due to technical issues.",
        extractionMethod: "Failed",
        documentType: file.type.startsWith("image/") ? "scanned" : "text_based",
        processingTime: 0,
        wordCount: 0,
        characterCount: 0,
        fileName: file.name,
        fileSize: file.size,
        fileType: file.type,
        displayData: {
          fileName: file.name,
          fileSize: file.size,
          fileType: file.type,
          hasError: true,
          errorMessage: error.message,
          processingSuccess: false,
        },
        timestamp: new Date().toISOString(),
      }

      setExtractedData(fallbackData)
      setActiveTab("results")
      
      // Auto-switch to document mode if there's any extracted text
      if (fallbackData.fullText && fallbackData.fullText.length > 0) {
        setChatMode("document")
      }

      toast({
        title: "Processing failed",
        description: "An error occurred while processing the document.",
        variant: "destructive",
      })
    } finally {
      setProcessing(false)
    }
  }

  const handleQAQuery = async () => {
    if (!qaQuery.trim() || !extractedData) return

    setQaResponse("Processing your query...")

    try {
      const response = await fetch("/api/qa-query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query: qaQuery,
          documentData: extractedData,
        }),
      })

      const result = await response.json()
      setQaResponse(result.answer)
    } catch (error) {
      setQaResponse("Sorry, I couldn't process your query. Please try again.")
    }
  }

  const handleChatMessage = async () => {
    if (!chatInput.trim()) return

    const userMessage = chatInput
    const newMessage = { role: "user", content: userMessage }
    setChatMessages((prev) => [...prev, newMessage])
    setChatInput("")
    setIsChatLoading(true)

    // Add typing indicator message
    const typingMessage = {
      role: "assistant",
      content: "thinking",
      isTyping: true,
      timestamp: new Date().toLocaleTimeString()
    }
    setChatMessages((prev) => [...prev, typingMessage])

    try {
      // Use the user-selected chat mode
      const mode = chatMode === "document" && extractedData?.fullText ? "document" : "general"
      const documentText = chatMode === "document" ? extractedData?.fullText || null : null

      console.log('Chat request:', { 
        message: userMessage, 
        mode, 
        selectedChatMode: chatMode,
        hasDocumentText: !!documentText,
        docLength: documentText?.length 
      })

      const response = await fetch("/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: userMessage,
          mode: mode,
          documentText: documentText,
        }),
      })

      const result = await response.json()
      
      // Remove typing indicator
      setChatMessages((prev) => prev.filter(msg => !msg.isTyping))
      
      let assistantContent = result.response || "I apologize, but I couldn't generate a proper response."
      
      // Add indicators for document usage and AI status
      if (result.using_document && result.ai_powered) {
        assistantContent = `🤖 *LLaMA AI analyzing your document* \n\n${assistantContent}`
      } else if (result.using_document) {
        assistantContent = `📄 *Using your document* \n\n${assistantContent}`
      } else if (result.ai_powered) {
        assistantContent = `🧠 *LLaMA AI Legal Assistant* \n\n${assistantContent}`
      }
      
      const assistantResponse = {
        role: "assistant",
        content: assistantContent,
        usingDocument: result.using_document,
        mode: result.mode,
        aiPowered: result.ai_powered,
        processingTime: result.processing_time
      }
      setChatMessages((prev) => [...prev, assistantResponse])
      
    } catch (error) {
      console.error('Chat error:', error)
      
      // Remove typing indicator
      setChatMessages((prev) => prev.filter(msg => !msg.isTyping))
      
      const errorResponse = {
        role: "assistant",
        content: "I apologize, but I'm having trouble connecting to the AI system. Please try again in a moment.",
      }
      setChatMessages((prev) => [...prev, errorResponse])
    } finally {
      setIsChatLoading(false)
    }
  }

  const speakText = (text) => {
    if (typeof window !== "undefined" && "speechSynthesis" in window) {
      const utterance = new SpeechSynthesisUtterance(text)
      utterance.lang = selectedLanguage === "hi" ? "hi-IN" : "en-US"
      utterance.onstart = () => setIsSpeaking(true)
      utterance.onend = () => setIsSpeaking(false)
      speechSynthesis.speak(utterance)
    }
  }

  const stopSpeaking = () => {
    if (typeof window !== "undefined" && "speechSynthesis" in window) {
      speechSynthesis.cancel()
      setIsSpeaking(false)
    }
  }

  const downloadResults = (format) => {
    if (!extractedData) return

    const filename = `court_order_${extractedData.metadata?.case_number?.replace(/[^a-zA-Z0-9]/g, "_") || "document"}`
    const timestamp = new Date().toISOString().split('T')[0]

    switch (format) {
      case "json":
        const dataStr = JSON.stringify(extractedData, null, 2)
        const dataBlob = new Blob([dataStr], { type: "application/json" })
        const url = URL.createObjectURL(dataBlob)
        const link = document.createElement("a")
        link.href = url
        link.download = `${filename}_${timestamp}.json`
        link.click()
        URL.revokeObjectURL(url)
        break
      case "pdf":
        // Create a comprehensive report
        const reportContent = generatePDFReport(extractedData)
        const pdfBlob = new Blob([reportContent], { type: "text/plain" })
        const pdfUrl = URL.createObjectURL(pdfBlob)
        const pdfLink = document.createElement("a")
        pdfLink.href = pdfUrl
        pdfLink.download = `${filename}_report_${timestamp}.txt`
        pdfLink.click()
        URL.revokeObjectURL(pdfUrl)
        toast({
          title: "Report Generated",
          description: "Comprehensive legal report downloaded successfully.",
        })
        break
      case "excel":
        // Create CSV format for Excel compatibility
        const csvContent = generateCSVReport(extractedData)
        const csvBlob = new Blob([csvContent], { type: "text/csv" })
        const csvUrl = URL.createObjectURL(csvBlob)
        const csvLink = document.createElement("a")
        csvLink.href = csvUrl
        csvLink.download = `${filename}_data_${timestamp}.csv`
        csvLink.click()
        URL.revokeObjectURL(csvUrl)
        toast({
          title: "Excel Data Generated",
          description: "Structured data exported to CSV format.",
        })
        break
      case "summary":
        // Download just the summary
        const summaryContent = generateSummaryReport(extractedData)
        const summaryBlob = new Blob([summaryContent], { type: "text/plain" })
        const summaryUrl = URL.createObjectURL(summaryBlob)
        const summaryLink = document.createElement("a")
        summaryLink.href = summaryUrl
        summaryLink.download = `${filename}_summary_${timestamp}.txt`
        summaryLink.click()
        URL.revokeObjectURL(summaryUrl)
        toast({
          title: "Summary Downloaded",
          description: "Document summary downloaded successfully.",
        })
        break
    }
  }

  const generatePDFReport = (data) => {
    return `
🏛️ LEGAL DOCUMENT ANALYSIS REPORT
=====================================
Generated: ${new Date().toLocaleString()}
Document: ${data.fileName || "Unknown"}
Processing Method: ${data.extractionMethod || "Unknown"}
Processing Time: ${data.processingTime || 0}s

📋 DOCUMENT INFORMATION
-----------------------
Case Number: ${data.metadata?.case_number || "Not found"}
Court Name: ${data.metadata?.court_name || "Not found"}
Document Type: ${data.metadata?.document_type || "Unknown"}
Order Date: ${data.metadata?.order_date || "Not found"}
Judge Name: ${data.metadata?.judge_name || "Not found"}

👥 PARTIES INVOLVED
-------------------
Petitioner: ${data.metadata?.petitioner_name || "Not found"}
Respondent: ${data.metadata?.respondent_name || "Not found"}

${data.metadata?.parties && data.metadata.parties.length > 0 ? 
  "Additional Parties:\n" + data.metadata.parties.map(party => 
    `- ${party.role || "Party"}: ${party.name || party}`
  ).join('\n') : ""
}

⚖️ LEGAL PROVISIONS
-------------------
${data.metadata?.statutes_sections && data.metadata.statutes_sections.length > 0 ? 
  data.metadata.statutes_sections.join(', ') : "No specific statutes identified"
}

📝 DOCUMENT SUMMARY
-------------------
${data.summary || "No summary available"}

📊 PROCESSING STATISTICS
-------------------------
Total Words: ${data.wordCount || 0}
Total Characters: ${data.characterCount || 0}
Pages Processed: ${data.pageCount || 0}
Extraction Confidence: ${data.documentAnalysis?.confidence ? (data.documentAnalysis.confidence * 100).toFixed(1) + '%' : 'N/A'}

🔧 TECHNICAL DETAILS
--------------------
Processing Pipeline:
${data.processingStages ? Object.entries(data.processingStages).map(([stage, completed]) => 
  `- ${stage.replace('_', ' ')}: ${completed ? '✅ Completed' : '❌ Failed'}`
).join('\n') : "No stage information available"}

Extracted Text Length: ${data.extractedText ? data.extractedText.length : 0} characters
Entities Found: ${data.structureAnalysis?.entities_found || 0}

=====================================
Report generated by Legal AI Platform
=====================================
    `
  }

  const generateCSVReport = (data) => {
    const headers = "Field,Value\n"
    const rows = [
      ["File Name", data.fileName || "Unknown"],
      ["Processing Method", data.extractionMethod || "Unknown"],
      ["Processing Time (seconds)", data.processingTime || 0],
      ["Case Number", data.metadata?.case_number || "Not found"],
      ["Court Name", data.metadata?.court_name || "Not found"],
      ["Document Type", data.metadata?.document_type || "Unknown"],
      ["Order Date", data.metadata?.order_date || "Not found"],
      ["Judge Name", data.metadata?.judge_name || "Not found"],
      ["Petitioner", data.metadata?.petitioner_name || "Not found"],
      ["Respondent", data.metadata?.respondent_name || "Not found"],
      ["Total Words", data.wordCount || 0],
      ["Total Characters", data.characterCount || 0],
      ["Pages Processed", data.pageCount || 0],
      ["Extraction Confidence", data.documentAnalysis?.confidence ? (data.documentAnalysis.confidence * 100).toFixed(1) + '%' : 'N/A'],
      ["Entities Found", data.structureAnalysis?.entities_found || 0],
    ].map(row => `"${row[0]}","${row[1]}"`).join('\n')
    
    return headers + rows
  }

  const generateSummaryReport = (data) => {
    return `
📄 DOCUMENT SUMMARY REPORT
===========================
Document: ${data.fileName || "Unknown"}
Generated: ${new Date().toLocaleString()}
Case: ${data.metadata?.case_number || "Unknown"}
Court: ${data.metadata?.court_name || "Unknown"}

📝 SUMMARY
-----------
${data.summary || "No summary available"}

📊 KEY INFORMATION
------------------
• Document Type: ${data.metadata?.document_type || "Unknown"}
• Order Date: ${data.metadata?.order_date || "Not found"}
• Judge: ${data.metadata?.judge_name || "Not found"}
• Total Words: ${data.wordCount || 0}
• Processing Time: ${data.processingTime || 0}s
• Extraction Method: ${data.extractionMethod || "Unknown"}

===========================
Summary generated by Legal AI Platform
===========================
    `
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 p-4">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-4">
            Advanced Legal AI Platform
          </h1>
          <p className="text-xl text-gray-600 mb-6">AI-Powered Legal Document Processing with OCR & Python ML</p>
          <div className="flex flex-wrap justify-center gap-3 mb-6">
            <Badge variant="secondary" className="flex items-center gap-1 px-3 py-1">
              <Brain className="w-4 h-4" />
              Python ML/AI
            </Badge>
            <Badge variant="secondary" className="flex items-center gap-1 px-3 py-1">
              <Scan className="w-4 h-4" />
              PaddleOCR
            </Badge>
            <Badge variant="secondary" className="flex items-center gap-1 px-3 py-1">
              <FileText className="w-4 h-4" />
              PDF Text Extraction
            </Badge>
            <Badge variant="secondary" className="flex items-center gap-1 px-3 py-1">
              <Languages className="w-4 h-4" />
              Multi-language
            </Badge>
            <Badge variant="secondary" className="flex items-center gap-1 px-3 py-1">
              <Eye className="w-4 h-4" />
              Smart Detection
            </Badge>
          </div>
        </div>

        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="upload">Upload & Process</TabsTrigger>
            <TabsTrigger value="processing" disabled={!processing && !extractedData}>
              AI Processing
            </TabsTrigger>
            <TabsTrigger value="results" disabled={!extractedData}>
              Results & Analysis
            </TabsTrigger>
            <TabsTrigger value="assistant">Legal Assistant</TabsTrigger>
          </TabsList>

          <TabsContent value="upload" className="space-y-6">
            <div className="grid lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Upload className="w-5 h-5" />
                    Document Upload & Processing
                  </CardTitle>
                  <CardDescription>
                    Upload PDF documents or images. Automatic detection of scanned vs regular PDFs.
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid w-full items-center gap-1.5">
                    <Label htmlFor="document">Legal Document (PDF/Image)</Label>
                    <Input
                      id="document"
                      type="file"
                      accept=".pdf,image/*"
                      onChange={handleFileUpload}
                      className="cursor-pointer"
                    />
                  </div>

                  {file && (
                    <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
                      <div className="flex items-center gap-2 text-green-800 mb-2">
                        <CheckCircle className="w-5 h-5" />
                        <span className="font-medium">File Ready for Processing</span>
                      </div>
                      <div className="space-y-1 text-sm">
                        <p>
                          <strong>File:</strong> {file.name}
                        </p>
                        <p>
                          <strong>Size:</strong> {(file.size / (1024 * 1024)).toFixed(2)} MB
                        </p>
                        <p>
                          <strong>Type:</strong> {file.type}
                        </p>
                        <div className="flex items-center gap-2 mt-2">
                          {file.type.startsWith("image/") || isScanned ? (
                            <Badge variant="outline" className="flex items-center gap-1">
                              <FileImage className="w-3 h-3" />
                              Scanned Document (OCR Required)
                            </Badge>
                          ) : (
                            <Badge variant="outline" className="flex items-center gap-1">
                              <FileText className="w-3 h-3" />
                              Text-based PDF
                            </Badge>
                          )}
                        </div>
                      </div>
                    </div>
                  )}

                  <div className="grid grid-cols-2 gap-4">
                    <div className="flex items-center space-x-2">
                      <Switch id="ocr" checked={ocrEnabled} onCheckedChange={setOcrEnabled} />
                      <Label htmlFor="ocr" className="text-sm">
                        OCR Processing
                      </Label>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Switch id="signature" checked={signatureDetection} onCheckedChange={setSignatureDetection} />
                      <Label htmlFor="signature" className="text-sm">
                        Signature Detection
                      </Label>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label>Summary Length</Label>
                    <Select value={summaryLength} onValueChange={setSummaryLength}>
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="brief">Brief (50-70 words)</SelectItem>
                        <SelectItem value="medium">Medium (100-120 words)</SelectItem>
                        <SelectItem value="detailed">Detailed (200-250 words)</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label>Language</Label>
                    <Select value={selectedLanguage} onValueChange={setSelectedLanguage}>
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {languages.map((lang) => (
                          <SelectItem key={lang.code} value={lang.code}>
                            {lang.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <Button onClick={processDocument} disabled={!file || processing} className="w-full" size="lg">
                    {processing ? "Processing with Python AI..." : "Analyze Document"}
                  </Button>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Brain className="w-5 h-5" />
                    Processing Pipeline
                  </CardTitle>
                  <CardDescription>Advanced Python-based document analysis</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-3">
                    <div className="flex items-center gap-3 p-3 bg-blue-50 rounded-lg">
                      <FileText className="w-5 h-5 text-blue-600" />
                      <div>
                        <h4 className="font-semibold text-sm">Regular PDF Processing</h4>
                        <p className="text-xs text-gray-600">Direct text extraction using PyPDF2/pdfplumber</p>
                      </div>
                    </div>

                    <div className="flex items-center gap-3 p-3 bg-purple-50 rounded-lg">
                      <Scan className="w-5 h-5 text-purple-600" />
                      <div>
                        <h4 className="font-semibold text-sm">Scanned Document OCR</h4>
                        <p className="text-xs text-gray-600">PaddleOCR for accurate text recognition</p>
                      </div>
                    </div>

                    <div className="flex items-center gap-3 p-3 bg-green-50 rounded-lg">
                      <Brain className="w-5 h-5 text-green-600" />
                      <div>
                        <h4 className="font-semibold text-sm">AI Summarization</h4>
                        <p className="text-xs text-gray-600">Transformers/BERT models for legal text analysis</p>
                      </div>
                    </div>
                  </div>

                  <Separator />

                  <div>
                    <Label className="font-semibold">Python Libraries Used</Label>
                    <div className="grid grid-cols-2 gap-2 mt-2">
                      <Badge variant="outline" className="justify-center">
                        PyPDF2
                      </Badge>
                      <Badge variant="outline" className="justify-center">
                        PaddleOCR
                      </Badge>
                      <Badge variant="outline" className="justify-center">
                        Transformers
                      </Badge>
                      <Badge variant="outline" className="justify-center">
                        spaCy
                      </Badge>
                      <Badge variant="outline" className="justify-center">
                        NLTK
                      </Badge>
                      <Badge variant="outline" className="justify-center">
                        OpenCV
                      </Badge>
                    </div>
                  </div>

                  <div>
                    <Label className="font-semibold">Supported Document Types</Label>
                    <div className="grid grid-cols-2 gap-2 mt-2">
                      {documentTypes.map((docType) => {
                        const IconComponent = docType.icon
                        return (
                          <div key={docType.type} className="flex items-center gap-2 p-2 border rounded-lg">
                            <div className={`w-3 h-3 rounded-full ${docType.color}`}></div>
                            <IconComponent className="w-4 h-4" />
                            <span className="text-sm">{docType.type}</span>
                          </div>
                        )
                      })}
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="processing" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Zap className="w-5 h-5 animate-pulse" />
                  Python AI Processing Pipeline
                </CardTitle>
                <CardDescription>Advanced document analysis using Python ML/AI libraries</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <Progress value={progress} className="w-full h-3" />
                <p className="text-sm text-gray-600 text-center font-medium">{progress.toFixed(0)}% Complete</p>

                {currentStep && (
                  <div className="flex items-center justify-center gap-2 p-3 bg-blue-50 rounded-lg">
                    <AlertCircle className="w-4 h-4 text-blue-600 animate-spin" />
                    <span className="text-sm font-medium text-blue-800">{currentStep}</span>
                  </div>
                )}

                <div className="grid md:grid-cols-2 gap-4 mt-6">
                  <div className="space-y-2">
                    <h4 className="font-semibold text-sm">Processing Steps:</h4>
                    <div className="space-y-1 text-xs">
                      <div className="flex items-center gap-2">
                        <CheckCircle className="w-3 h-3 text-green-500" />
                        <span>Document type detection</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <CheckCircle className="w-3 h-3 text-green-500" />
                        <span>{isScanned ? "OCR text extraction" : "PDF text extraction"}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <AlertCircle className="w-3 h-3 text-yellow-500 animate-spin" />
                        <span>AI analysis & summarization</span>
                      </div>
                    </div>
                  </div>
                  <div className="space-y-2">
                    <h4 className="font-semibold text-sm">Python Libraries Active:</h4>
                    <div className="space-y-1 text-xs">
                      <Badge variant="outline" className="text-xs">
                        {isScanned ? "PaddleOCR" : "PyPDF2"}
                      </Badge>
                      <Badge variant="outline" className="text-xs">
                        Transformers
                      </Badge>
                      <Badge variant="outline" className="text-xs">
                        spaCy NLP
                      </Badge>
                    </div>
                  </div>
                </div>

                {file && (
                  <div className="text-sm text-gray-500 mt-4 p-3 bg-gray-50 rounded-lg">
                    <p>
                      <strong>Processing:</strong> {file.name}
                    </p>
                    <p>
                      <strong>Size:</strong> {(file.size / (1024 * 1024)).toFixed(2)} MB
                    </p>
                    <p>
                      <strong>Method:</strong>{" "}
                      {isScanned || file.type.startsWith("image/") ? "OCR + AI Analysis" : "Direct Text + AI Analysis"}
                    </p>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="results" className="space-y-6">
            {extractedData && (
              <div>
                <div className="flex justify-between items-center">
                  <h2 className="text-3xl font-bold">AI Analysis Results</h2>
                  <div className="flex gap-2 flex-wrap">
                    <Button onClick={() => downloadResults("json")} variant="outline" size="sm">
                      <Download className="w-4 h-4 mr-2" />
                      Complete Data (JSON)
                    </Button>
                    <Button onClick={() => downloadResults("pdf")} variant="outline" size="sm">
                      <Download className="w-4 h-4 mr-2" />
                      Full Report (TXT)
                    </Button>
                    <Button onClick={() => downloadResults("excel")} variant="outline" size="sm">
                      <Download className="w-4 h-4 mr-2" />
                      Data (CSV)
                    </Button>
                    <Button onClick={() => downloadResults("summary")} variant="outline" size="sm">
                      <Download className="w-4 h-4 mr-2" />
                      Summary Only
                    </Button>
                  </div>
                </div>

                {/* Performance Metrics */}
                <div className="grid md:grid-cols-6 gap-4">
                  <Card>
                    <CardContent className="p-4 text-center">
                      <Clock className="w-6 h-6 mx-auto mb-2 text-green-600" />
                      <div className="text-2xl font-bold text-green-600">
                        {extractedData.processingTime ? extractedData.processingTime.toFixed(1) : "0"}s
                      </div>
                      <p className="text-sm text-gray-600">Processing Time</p>
                    </CardContent>
                  </Card>
                  <Card>
                    <CardContent className="p-4 text-center">
                      <Brain className="w-6 h-6 mx-auto mb-2 text-blue-600" />
                      <div className="text-2xl font-bold text-blue-600">
                        {extractedData.documentAnalysis?.confidence
                          ? (extractedData.documentAnalysis.confidence * 100).toFixed(0)
                          : "85"}
                        %
                      </div>
                      <p className="text-sm text-gray-600">Extraction Confidence</p>
                    </CardContent>
                  </Card>
                  <Card>
                    <CardContent className="p-4 text-center">
                      <FileText className="w-6 h-6 mx-auto mb-2 text-purple-600" />
                      <div className="text-2xl font-bold text-purple-600">{extractedData.pageCount || "N/A"}</div>
                      <p className="text-sm text-gray-600">Pages Processed</p>
                    </CardContent>
                  </Card>
                  <Card>
                    <CardContent className="p-4 text-center">
                      <Scan className="w-6 h-6 mx-auto mb-2 text-orange-600" />
                      <div className="text-xs font-bold text-orange-600 text-center leading-tight">
                        {extractedData.extractionMethod || "Unknown"}
                      </div>
                      <p className="text-sm text-gray-600">Extraction Method</p>
                    </CardContent>
                  </Card>
                  <Card>
                    <CardContent className="p-4 text-center">
                      <Scale className="w-6 h-6 mx-auto mb-2 text-red-600" />
                      <div className="text-2xl font-bold text-red-600">{extractedData.wordCount || "0"}</div>
                      <p className="text-sm text-gray-600">Words Extracted</p>
                    </CardContent>
                  </Card>
                  <Card>
                    <CardContent className="p-4 text-center">
                      <Zap className="w-6 h-6 mx-auto mb-2 text-indigo-600" />
                      <div className="text-2xl font-bold text-indigo-600">
                        {extractedData.structureAnalysis?.processing_stages_completed || 0}/
                        {extractedData.structureAnalysis?.total_processing_stages || 4}
                      </div>
                      <p className="text-sm text-gray-600">Pipeline Stages</p>
                    </CardContent>
                  </Card>
                </div>

                {/* Show error message if processing failed */}
                {extractedData.displayData?.hasError && (
                  <Card className="border-red-200 bg-red-50">
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2 text-red-800">
                        <AlertCircle className="w-5 h-5" />
                        Processing Issues Detected
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="text-red-700 text-sm mb-2">
                        {extractedData.displayData.errorMessage || extractedData.error}
                      </p>
                      <div className="text-xs text-red-600">
                        <p>
                          <strong>File:</strong> {extractedData.displayData?.fileName}
                        </p>
                        <p>
                          <strong>Size:</strong> {(extractedData.displayData.fileSize / (1024 * 1024)).toFixed(2)} MB
                        </p>
                        <p>
                          <strong>Type:</strong> {extractedData.displayData.fileType}
                        </p>
                      </div>
                    </CardContent>
                  </Card>
                )}

                {/* File Information */}
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <FileText className="w-5 h-5" />
                      Document Information
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <div className="grid md:grid-cols-2 gap-4">
                      <div>
                        <Label className="font-semibold">File Name</Label>
                        <p className="text-sm mt-1">{extractedData.displayData?.fileName || "Unknown"}</p>
                      </div>
                      <div>
                        <Label className="font-semibold">File Size</Label>
                        <p className="text-sm mt-1">
                          {extractedData.displayData?.fileSize
                            ? (extractedData.displayData.fileSize / (1024 * 1024)).toFixed(2) + " MB"
                            : "Unknown"}
                        </p>
                      </div>
                      <div>
                        <Label className="font-semibold">Document Type</Label>
                        <p className="text-sm mt-1">{extractedData.documentAnalysis?.type || "Unknown"}</p>
                      </div>
                      <div>
                        <Label className="font-semibold">Processing Method</Label>
                        <p className="text-sm mt-1">{extractedData.extractionMethod || "Unknown"}</p>
                      </div>
                    </div>

                    {extractedData.documentAnalysis?.complexity && (
                      <div>
                        <Label className="font-semibold">Document Complexity</Label>
                        <Badge
                          variant={
                            extractedData.documentAnalysis.complexity === "high"
                              ? "destructive"
                              : extractedData.documentAnalysis.complexity === "medium"
                                ? "default"
                                : "secondary"
                          }
                          className="ml-2"
                        >
                          {extractedData.documentAnalysis.complexity.toUpperCase()}
                        </Badge>
                      </div>
                    )}
                  </CardContent>
                </Card>

                {/* Extracted Text Preview */}
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <FileText className="w-5 h-5" />
                      Extracted Text Preview
                    </CardTitle>
                    <CardDescription>
                      Text extracted using {extractedData.extractionMethod || "Unknown method"}
                      {extractedData.librariesUsed?.advanced_libs_available === false && (
                        <span className="text-orange-600 ml-2">
                          (Basic extraction - install Python libraries for enhanced processing)
                        </span>
                      )}
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="p-4 bg-gray-50 border rounded-lg max-h-60 overflow-y-auto">
                      <pre className="text-sm whitespace-pre-wrap">
                        {extractedData.extractedText || "No text extracted"}
                      </pre>
                    </div>
                    {extractedData.extractedText && (
                      <div className="mt-2 text-sm text-gray-500 flex justify-between">
                        <span>Characters: {extractedData.characterCount || extractedData.extractedText.length}</span>
                        <span>Words: {extractedData.wordCount || extractedData.extractedText.split(/\s+/).length}</span>
                      </div>
                    )}
                  </CardContent>
                </Card>

                {/* AI Generated Summary */}
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center justify-between">
                      <span className="flex items-center gap-2">
                        <BookOpen className="w-5 h-5" />
                        Generated Summary
                      </span>
                      <div className="flex items-center gap-2">
                        <Button
                          onClick={() => speakText(extractedData.summary || "")}
                          disabled={isSpeaking || !extractedData.summary}
                          variant="outline"
                          size="sm"
                        >
                          {isSpeaking ? <VolumeX className="w-4 h-4" /> : <Volume2 className="w-4 h-4" />}
                        </Button>
                        {isSpeaking && (
                          <Button onClick={stopSpeaking} variant="outline" size="sm">
                            Stop
                          </Button>
                        )}
                      </div>
                    </CardTitle>
                    <CardDescription>
                      {extractedData.displayData?.summaryGenerated
                        ? "AI-generated summary based on extracted content"
                        : "Summary generation may be limited due to text extraction issues"}
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                      <p className="text-sm leading-relaxed">{extractedData.summary || "No summary available"}</p>
                    </div>

                    <div className="flex justify-between text-sm text-gray-500">
                      <span>
                        Word count: {extractedData.summary ? extractedData.summary.split(" ").length : 0} words
                      </span>
                      <span>
                        Method:{" "}
                        {extractedData.librariesUsed?.advanced_libs_available ? "AI-Enhanced" : "Basic Extraction"}
                      </span>
                    </div>
                  </CardContent>
                </Card>

                {/* Comprehensive Metadata Display */}
                {extractedData.metadata && Object.keys(extractedData.metadata).length > 0 && (
                  <Card>
                    <CardHeader>
                      <CardTitle className="flex items-center justify-between">
                        <span className="flex items-center gap-2">
                          <Gavel className="w-5 h-5" />
                          Legal Document Metadata
                        </span>
                        <Badge 
                          variant={
                            extractedData.metadata.extraction_confidence > 80 ? "default" :
                            extractedData.metadata.extraction_confidence > 60 ? "secondary" : "destructive"
                          }
                        >
                          {extractedData.metadata.extraction_confidence ? 
                            `${extractedData.metadata.extraction_confidence.toFixed(0)}% Confidence` : 
                            "Metadata Extracted"
                          }
                        </Badge>
                      </CardTitle>
                      <CardDescription>
                        Comprehensive legal information extracted using advanced AI and pattern recognition
                      </CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-6">
                      {/* Case Information Grid */}
                      <div>
                        <h4 className="font-semibold mb-3 text-lg flex items-center gap-2">
                          <Scale className="w-4 h-4" />
                          Case Information
                        </h4>
                        <div className="grid md:grid-cols-2 gap-4">
                          <div className="space-y-1">
                            <Label className="font-medium text-sm text-gray-600">Case Number</Label>
                            <p className="text-sm font-mono bg-gray-50 p-2 rounded border">
                              {extractedData.metadata.case_number || "Not found"}
                            </p>
                          </div>
                          <div className="space-y-1">
                            <Label className="font-medium text-sm text-gray-600">Court Name</Label>
                            <p className="text-sm bg-gray-50 p-2 rounded border">
                              {extractedData.metadata.court_name || "Not found"}
                            </p>
                          </div>
                          <div className="space-y-1">
                            <Label className="font-medium text-sm text-gray-600">Document Type</Label>
                            <p className="text-sm bg-gray-50 p-2 rounded border">
                              {extractedData.metadata.document_type || "Legal Document"}
                            </p>
                          </div>
                          <div className="space-y-1">
                            <Label className="font-medium text-sm text-gray-600">Order Date</Label>
                            <p className="text-sm bg-gray-50 p-2 rounded border">
                              {extractedData.metadata.order_date || "Not found"}
                            </p>
                          </div>
                          <div className="space-y-1">
                            <Label className="font-medium text-sm text-gray-600">Judge Name</Label>
                            <p className="text-sm bg-gray-50 p-2 rounded border">
                              {extractedData.metadata.judge_name || "Not found"}
                            </p>
                          </div>
                          <div className="space-y-1">
                            <Label className="font-medium text-sm text-gray-600">Processing Method</Label>
                            <p className="text-sm bg-gray-50 p-2 rounded border">
                              {extractedData.processingStages?.metadata_extraction ? "Advanced AI Extraction" : "Basic Pattern Matching"}
                            </p>
                          </div>
                        </div>
                      </div>

                      {/* Parties Information - Comprehensive Display */}
                      {((extractedData.metadata.petitioner_name && extractedData.metadata.petitioner_name !== "Not found") ||
                        (extractedData.metadata.respondent_name && extractedData.metadata.respondent_name !== "Not found") ||
                        (extractedData.metadata.parties && extractedData.metadata.parties.length > 0)) && (
                        <div>
                          <h4 className="font-semibold mb-3 text-lg flex items-center gap-2">
                            <Users className="w-4 h-4" />
                            Parties Involved
                          </h4>
                          <div className="space-y-4">
                            {/* Legacy fields display */}
                            {extractedData.metadata.petitioner_name && extractedData.metadata.petitioner_name !== "Not found" && (
                              <div className="flex items-center gap-2 p-2 bg-blue-50 rounded-lg border">
                                <Badge variant="outline" className="bg-blue-100 text-blue-800">Petitioner</Badge>
                                <span className="text-sm font-medium">{extractedData.metadata.petitioner_name}</span>
                              </div>
                            )}
                            {extractedData.metadata.respondent_name && extractedData.metadata.respondent_name !== "Not found" && (
                              <div className="flex items-center gap-2 p-2 bg-red-50 rounded-lg border">
                                <Badge variant="outline" className="bg-red-100 text-red-800">Respondent</Badge>
                                <span className="text-sm font-medium">{extractedData.metadata.respondent_name}</span>
                              </div>
                            )}
                            
                            {/* Comprehensive parties display */}
                            {extractedData.metadata.parties && extractedData.metadata.parties.length > 0 && (
                              <div>
                                <Label className="font-medium text-sm text-gray-600 mb-3 block">Detailed Parties Information</Label>
                                <div className="space-y-3">
                                  {extractedData.metadata.parties.map((party, index) => (
                                    <Card key={index} className="border-l-4 border-l-blue-400">
                                      <CardContent className="pt-4">
                                        <div className="space-y-2">
                                          {/* Party Name and Role */}
                                          <div className="flex items-center justify-between">
                                            <div className="flex items-center gap-2">
                                              <Badge variant="outline" className="capitalize font-medium">
                                                {party.role || party.type || "Party"}
                                              </Badge>
                                              <span className="font-semibold text-sm">
                                                {party.name || (typeof party === 'string' ? party : "Unknown")}
                                              </span>
                                            </div>
                                            {party.age && (
                                              <Badge variant="secondary" className="text-xs">
                                                Age: {party.age}
                                              </Badge>
                                            )}
                                          </div>
                                          
                                          {/* Address Information */}
                                          {party.address && (
                                            <div className="ml-4 text-xs text-gray-600 bg-gray-50 p-2 rounded">
                                              <strong>Address:</strong> {party.address}
                                            </div>
                                          )}
                                          
                                          {/* Father's/Guardian's Name */}
                                          {party.father_name && (
                                            <div className="ml-4 text-xs text-gray-600">
                                              <strong>Father/Guardian:</strong> {party.father_name}
                                            </div>
                                          )}
                                          
                                          {/* Counsel Information */}
                                          {party.counsel && party.counsel.length > 0 && (
                                            <div className="ml-4">
                                              <Label className="text-xs text-gray-500 block mb-1">Legal Counsel:</Label>
                                              <div className="flex flex-wrap gap-1">
                                                {party.counsel.map((counsel, cIndex) => (
                                                  <Badge key={cIndex} variant="outline" className="text-xs bg-green-50 text-green-700">
                                                    {typeof counsel === 'string' ? counsel : counsel.name}
                                                  </Badge>
                                                ))}
                                              </div>
                                            </div>
                                          )}
                                          
                                          {/* Additional party details if available */}
                                          {party.description && (
                                            <div className="ml-4 text-xs text-gray-600 italic">
                                              {party.description}
                                            </div>
                                          )}
                                        </div>
                                      </CardContent>
                                    </Card>
                                  ))}
                                </div>
                              </div>
                            )}
                          </div>
                        </div>
                      )}

                      {/* Legal Provisions - Enhanced Display */}
                      {extractedData.metadata.statutes_sections && extractedData.metadata.statutes_sections.length > 0 && (
                        <div>
                          <h4 className="font-semibold mb-3 text-lg flex items-center gap-2">
                            <BookOpen className="w-4 h-4" />
                            Legal Provisions & Statutes
                          </h4>
                          <div className="space-y-3">
                            <div className="flex flex-wrap gap-2">
                              {extractedData.metadata.statutes_sections.map((statute, index) => (
                                <Badge key={index} variant="outline" className="text-xs">
                                  {statute}
                                </Badge>
                              ))}
                            </div>
                            {extractedData.metadata.acts_referenced && extractedData.metadata.acts_referenced.length > 0 && (
                              <div>
                                <Label className="text-xs text-gray-500 block mb-2">Referenced Acts:</Label>
                                <div className="flex flex-wrap gap-1">
                                  {extractedData.metadata.acts_referenced.map((act, index) => (
                                    <Badge key={index} variant="secondary" className="text-xs">
                                      {act}
                                    </Badge>
                                  ))}
                                </div>
                              </div>
                            )}
                          </div>
                        </div>
                      )}

                      {/* Additional Metadata Fields */}
                      <div className="space-y-4">
                        {/* Filing Details */}
                        {(extractedData.metadata.filing_date || extractedData.metadata.filing_number || extractedData.metadata.filing_year) && (
                          <div>
                            <h4 className="font-semibold mb-3 text-lg flex items-center gap-2">
                              <FileText className="w-4 h-4" />
                              Filing Information
                            </h4>
                            <div className="grid md:grid-cols-3 gap-3">
                              {extractedData.metadata.filing_date && (
                                <div className="space-y-1">
                                  <Label className="font-medium text-sm text-gray-600">Filing Date</Label>
                                  <p className="text-sm bg-gray-50 p-2 rounded border">
                                    {extractedData.metadata.filing_date}
                                  </p>
                                </div>
                              )}
                              {extractedData.metadata.filing_number && (
                                <div className="space-y-1">
                                  <Label className="font-medium text-sm text-gray-600">Filing Number</Label>
                                  <p className="text-sm font-mono bg-gray-50 p-2 rounded border">
                                    {extractedData.metadata.filing_number}
                                  </p>
                                </div>
                              )}
                              {extractedData.metadata.filing_year && (
                                <div className="space-y-1">
                                  <Label className="font-medium text-sm text-gray-600">Filing Year</Label>
                                  <p className="text-sm bg-gray-50 p-2 rounded border">
                                    {extractedData.metadata.filing_year}
                                  </p>
                                </div>
                              )}
                            </div>
                          </div>
                        )}

                        {/* Bench and Jurisdiction */}
                        {(extractedData.metadata.bench || extractedData.metadata.jurisdiction || extractedData.metadata.location) && (
                          <div>
                            <h4 className="font-semibold mb-3 text-lg flex items-center gap-2">
                              <MapPin className="w-4 h-4" />
                              Jurisdiction & Bench
                            </h4>
                            <div className="grid md:grid-cols-3 gap-3">
                              {extractedData.metadata.bench && (
                                <div className="space-y-1">
                                  <Label className="font-medium text-sm text-gray-600">Bench</Label>
                                  <p className="text-sm bg-gray-50 p-2 rounded border">
                                    {extractedData.metadata.bench}
                                  </p>
                                </div>
                              )}
                              {extractedData.metadata.jurisdiction && (
                                <div className="space-y-1">
                                  <Label className="font-medium text-sm text-gray-600">Jurisdiction</Label>
                                  <p className="text-sm bg-gray-50 p-2 rounded border">
                                    {extractedData.metadata.jurisdiction}
                                  </p>
                                </div>
                              )}
                              {extractedData.metadata.location && (
                                <div className="space-y-1">
                                  <Label className="font-medium text-sm text-gray-600">Location</Label>
                                  <p className="text-sm bg-gray-50 p-2 rounded border">
                                    {extractedData.metadata.location}
                                  </p>
                                </div>
                              )}
                            </div>
                          </div>
                        )}

                        {/* Subject Matter and Case Type */}
                        {(extractedData.metadata.subject_matter || extractedData.metadata.case_type || extractedData.metadata.nature_of_case) && (
                          <div>
                            <h4 className="font-semibold mb-3 text-lg flex items-center gap-2">
                              <Scale className="w-4 h-4" />
                              Case Classification
                            </h4>
                            <div className="grid md:grid-cols-2 gap-3">
                              {extractedData.metadata.subject_matter && (
                                <div className="space-y-1">
                                  <Label className="font-medium text-sm text-gray-600">Subject Matter</Label>
                                  <p className="text-sm bg-gray-50 p-2 rounded border">
                                    {extractedData.metadata.subject_matter}
                                  </p>
                                </div>
                              )}
                              {extractedData.metadata.case_type && (
                                <div className="space-y-1">
                                  <Label className="font-medium text-sm text-gray-600">Case Type</Label>
                                  <p className="text-sm bg-gray-50 p-2 rounded border">
                                    {extractedData.metadata.case_type}
                                  </p>
                                </div>
                              )}
                              {extractedData.metadata.nature_of_case && (
                                <div className="space-y-1 md:col-span-2">
                                  <Label className="font-medium text-sm text-gray-600">Nature of Case</Label>
                                  <p className="text-sm bg-gray-50 p-2 rounded border">
                                    {extractedData.metadata.nature_of_case}
                                  </p>
                                </div>
                              )}
                            </div>
                          </div>
                        )}

                        {/* Counsel Information - Consolidated View */}
                        {(extractedData.metadata.petitioner_counsel || extractedData.metadata.respondent_counsel || 
                          (extractedData.metadata.counsels && extractedData.metadata.counsels.length > 0)) && (
                          <div>
                            <h4 className="font-semibold mb-3 text-lg flex items-center gap-2">
                              <Users className="w-4 h-4" />
                              Legal Representation
                            </h4>
                            <div className="space-y-3">
                              {extractedData.metadata.petitioner_counsel && (
                                <div className="p-3 bg-blue-50 rounded-lg border border-blue-200">
                                  <Label className="font-medium text-sm text-blue-800">Petitioner's Counsel</Label>
                                  <p className="text-sm text-blue-700 mt-1">
                                    {Array.isArray(extractedData.metadata.petitioner_counsel) 
                                      ? extractedData.metadata.petitioner_counsel.join(", ")
                                      : extractedData.metadata.petitioner_counsel}
                                  </p>
                                </div>
                              )}
                              {extractedData.metadata.respondent_counsel && (
                                <div className="p-3 bg-red-50 rounded-lg border border-red-200">
                                  <Label className="font-medium text-sm text-red-800">Respondent's Counsel</Label>
                                  <p className="text-sm text-red-700 mt-1">
                                    {Array.isArray(extractedData.metadata.respondent_counsel) 
                                      ? extractedData.metadata.respondent_counsel.join(", ")
                                      : extractedData.metadata.respondent_counsel}
                                  </p>
                                </div>
                              )}
                              {extractedData.metadata.counsels && extractedData.metadata.counsels.length > 0 && (
                                <div>
                                  <Label className="font-medium text-sm text-gray-600 mb-2 block">All Counsels Identified</Label>
                                  <div className="flex flex-wrap gap-2">
                                    {extractedData.metadata.counsels.map((counsel, index) => (
                                      <Badge key={index} variant="outline" className="text-xs bg-green-50 text-green-700">
                                        {typeof counsel === 'string' ? counsel : counsel.name || counsel}
                                      </Badge>
                                    ))}
                                  </div>
                                </div>
                              )}
                            </div>
                          </div>
                        )}

                        {/* Orders and Directions */}
                        {(extractedData.metadata.final_order || extractedData.metadata.directions || extractedData.metadata.interim_orders) && (
                          <div>
                            <h4 className="font-semibold mb-3 text-lg flex items-center gap-2">
                              <Gavel className="w-4 h-4" />
                              Orders & Directions
                            </h4>
                            <div className="space-y-3">
                              {extractedData.metadata.final_order && (
                                <div className="p-3 bg-yellow-50 rounded-lg border border-yellow-200">
                                  <Label className="font-medium text-sm text-yellow-800">Final Order</Label>
                                  <p className="text-sm text-yellow-700 mt-1">
                                    {extractedData.metadata.final_order}
                                  </p>
                                </div>
                              )}
                              {extractedData.metadata.directions && (
                                <div className="p-3 bg-purple-50 rounded-lg border border-purple-200">
                                  <Label className="font-medium text-sm text-purple-800">Court Directions</Label>
                                  <p className="text-sm text-purple-700 mt-1">
                                    {extractedData.metadata.directions}
                                  </p>
                                </div>
                              )}
                              {extractedData.metadata.interim_orders && (
                                <div className="p-3 bg-indigo-50 rounded-lg border border-indigo-200">
                                  <Label className="font-medium text-sm text-indigo-800">Interim Orders</Label>
                                  <p className="text-sm text-indigo-700 mt-1">
                                    {Array.isArray(extractedData.metadata.interim_orders) 
                                      ? extractedData.metadata.interim_orders.join("; ")
                                      : extractedData.metadata.interim_orders}
                                  </p>
                                </div>
                              )}
                            </div>
                          </div>
                        )}
                      </div>

                      {/* Processing Statistics */}
                      {extractedData.metadata.total_fields_extracted && (
                        <div className="p-3 bg-blue-50 border border-blue-200 rounded-lg">
                          <div className="flex items-center justify-between">
                            <span className="text-sm font-medium text-blue-800">Metadata Extraction Summary</span>
                            <Badge className="bg-blue-100 text-blue-800">
                              {extractedData.metadata.total_fields_extracted} fields extracted
                            </Badge>
                          </div>
                          <div className="mt-2 text-xs text-blue-700">
                            Extraction confidence: {extractedData.metadata.extraction_confidence ? 
                              `${extractedData.metadata.extraction_confidence.toFixed(1)}%` : "N/A"}
                          </div>
                        </div>
                      )}

                      {/* Processing Stages Status */}
                      {extractedData.processingStages && (
                        <div>
                          <h4 className="font-semibold mb-3 text-lg flex items-center gap-2">
                            <Zap className="w-4 h-4" />
                            Processing Pipeline Status
                          </h4>
                          <div className="grid grid-cols-2 gap-2">
                            {Object.entries(extractedData.processingStages).map(([stage, completed]) => (
                              <div key={stage} className="flex items-center gap-2 p-2 rounded border">
                                {completed ? (
                                  <CheckCircle className="w-4 h-4 text-green-600" />
                                ) : (
                                  <AlertCircle className="w-4 h-4 text-gray-400" />
                                )}
                                <span className="text-sm capitalize">
                                  {stage.replace('_', ' ')}
                                </span>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </CardContent>
                  </Card>
                )}

                {/* Legal Entities Extracted */}
                {extractedData.documentAnalysis?.keyEntities && (
                  <Card>
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2">
                        <Users className="w-5 h-5" />
                        Extracted Legal Entities
                      </CardTitle>
                      <CardDescription>Key information automatically extracted from the document</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      {Object.entries(extractedData.documentAnalysis.keyEntities).map(
                        ([entityType, entities]) =>
                          entities &&
                          entities.length > 0 && (
                            <div key={entityType}>
                              <Label className="font-semibold capitalize">{entityType.replace("_", " ")}</Label>
                              <div className="flex flex-wrap gap-2 mt-2">
                                {entities.slice(0, 5).map((entity, index) => (
                                  <Badge key={index} variant="outline">
                                    {entity}
                                  </Badge>
                                ))}
                                {entities.length > 5 && <Badge variant="secondary">+{entities.length - 5} more</Badge>}
                              </div>
                            </div>
                          ),
                      )}

                      {Object.values(extractedData.documentAnalysis.keyEntities).every(
                        (arr) => !arr || arr.length === 0,
                      ) && (
                        <p className="text-gray-500 text-sm">
                          No specific legal entities could be extracted from this document.
                        </p>
                      )}
                    </CardContent>
                  </Card>
                )}
              </div>
            )}
          </TabsContent>

          <TabsContent value="assistant" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Bot className="w-5 h-5" />
                  Legal AI Assistant
                  <Badge variant="secondary" className="ml-2">
                    {extractedData?.fullText ? "📄 Document Mode" : "💬 General Mode"}
                  </Badge>
                  {isChatLoading && (
                    <div className="flex items-center gap-2 ml-auto">
                      <div className="w-3 h-3 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
                      <span className="text-sm text-blue-600 font-medium">AI Processing...</span>
                    </div>
                  )}
                </CardTitle>
                <CardDescription>
                  Enhanced interactive AI assistant powered by LLaMA 3.1 • Ask questions, get legal guidance, analyze documents
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Chat Mode Selection */}
                <div className="flex gap-2 p-2 bg-gray-100 rounded-lg">
                  <button
                    onClick={() => setChatMode("general")}
                    className={`flex items-center gap-2 px-4 py-2 rounded-md text-sm font-medium transition-all ${
                      chatMode === "general"
                        ? "bg-blue-600 text-white shadow-md"
                        : "bg-white text-gray-700 hover:bg-gray-50"
                    }`}
                  >
                    <MessageCircle className="w-4 h-4" />
                    General Questions
                  </button>
                  <button
                    onClick={() => setChatMode("document")}
                    disabled={!extractedData?.fullText}
                    className={`flex items-center gap-2 px-4 py-2 rounded-md text-sm font-medium transition-all ${
                      chatMode === "document" && extractedData?.fullText
                        ? "bg-purple-600 text-white shadow-md"
                        : extractedData?.fullText
                        ? "bg-white text-gray-700 hover:bg-gray-50"
                        : "bg-gray-200 text-gray-400 cursor-not-allowed"
                    }`}
                  >
                    <FileText className="w-4 h-4" />
                    Document Analysis
                  </button>
                </div>
                <div className="h-96 border rounded-lg p-4 overflow-y-auto bg-gradient-to-br from-gray-50 to-white">
                  {chatMessages.length === 0 ? (
                    <div className="text-center text-gray-500 mt-16">
                      <div className="relative">
                        <Bot className="w-16 h-16 mx-auto mb-4 text-blue-400" />
                        <Sparkles className="w-4 h-4 absolute top-0 right-1/2 transform translate-x-8 text-purple-400 animate-pulse" />
                      </div>
                      <h3 className="text-lg font-semibold mb-2 text-gray-700">Legal AI Assistant Ready</h3>
                      {chatMode === "document" && extractedData?.fullText ? (
                        <div>
                          <p className="mb-2">🔍 <strong>Document Analysis Mode:</strong> I'll analyze your processed document and can help with:</p>
                          <div className="text-sm space-y-1 text-gray-600">
                            <p>📄 Document-specific questions and analysis</p>
                            <p>📝 Generate comprehensive summaries</p>
                            <p>⚖️ Identify legal provisions and parties</p>
                            <p>� Extract key information and dates</p>
                          </div>
                        </div>
                      ) : (
                        <div>
                          <p className="mb-2">💬 <strong>General Legal Mode:</strong> I can help you with:</p>
                          <div className="text-sm space-y-1 text-gray-600">
                            <p>💬 General legal questions and guidance</p>
                            <p>📚 Explain legal procedures and concepts</p>
                            <p>⚖️ Discuss case scenarios and implications</p>
                            <p>📋 Legal rights and responsibilities</p>
                          </div>
                        </div>
                      )}
                      <p className="text-sm mt-3 text-blue-600">Powered by Enhanced Interactive Q&A System</p>
                    </div>
                  ) : (
                    <div className="space-y-4">
                      {chatMessages.map((message, index) => (
                        <div
                          key={index}
                          className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}
                        >
                          <div className={`flex gap-3 max-w-[85%] ${
                            message.role === "user" ? "flex-row-reverse" : "flex-row"
                          }`}>
                            {/* Avatar */}
                            <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                              message.role === "user" 
                                ? "bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg" 
                                : "bg-gradient-to-r from-gray-100 to-gray-200 text-gray-700 shadow-md"
                            }`}>
                              {message.role === "user" ? (
                                <User className="w-4 h-4" />
                              ) : (
                                <Bot className="w-4 h-4" />
                              )}
                            </div>
                            
                            {/* Message Content */}
                            <div
                              className={`rounded-2xl px-4 py-3 shadow-sm ${
                                message.role === "user" 
                                  ? "bg-gradient-to-r from-blue-600 to-purple-600 text-white" 
                                  : "bg-white border border-gray-200"
                              }`}
                            >
                              <div className="whitespace-pre-wrap text-sm leading-relaxed">
                                {message.isTyping ? (
                                  <div className="flex items-center gap-2">
                                    <div className="flex gap-1">
                                      <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{animationDelay: '0ms'}}></div>
                                      <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{animationDelay: '150ms'}}></div>
                                      <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{animationDelay: '300ms'}}></div>
                                    </div>
                                    <span className="text-gray-500 text-xs">LLaMA AI is analyzing your question...</span>
                                  </div>
                                ) : (
                                  message.content
                                )}
                              </div>
                              <div className={`text-xs mt-2 flex items-center justify-between ${
                                message.role === "user" ? "text-blue-200" : "text-gray-500"
                              }`}>
                                <div className="flex items-center gap-2">
                                  {new Date().toLocaleTimeString()}
                                  {message.role === "assistant" && message.aiPowered && (
                                    <span className="bg-purple-100 text-purple-700 px-2 py-1 rounded-full text-xs font-medium">
                                      🤖 LLaMA AI
                                    </span>
                                  )}
                                  {message.role === "assistant" && message.usingDocument && (
                                    <span className="bg-blue-100 text-blue-700 px-2 py-1 rounded-full text-xs font-medium">
                                      📄 Document
                                    </span>
                                  )}
                                </div>
                                {message.role === "assistant" && message.processingTime && (
                                  <span className="text-xs opacity-60">
                                    {message.processingTime.toFixed(1)}s
                                  </span>
                                )}
                              </div>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>

                {/* Input Area */}
                <div className="flex gap-2">
                  <div className="flex-1 relative">
                    <Input
                      placeholder={
                        chatMode === "document"
                          ? "Ask questions about your uploaded document..."
                          : "Ask general legal questions, scenarios, or procedures..."
                      }
                      value={chatInput}
                      onChange={(e) => setChatInput(e.target.value)}
                      onKeyPress={(e) => e.key === "Enter" && !isChatLoading && handleChatMessage()}
                      disabled={isChatLoading}
                      className="pr-12 border-gray-300 focus:border-blue-500"
                    />
                    {chatInput.trim() && (
                      <Button
                        size="sm"
                        onClick={handleChatMessage}
                        disabled={!chatInput.trim() || isChatLoading}
                        className="absolute right-1 top-1 h-8 w-8 p-0 bg-gradient-to-r from-blue-600 to-purple-600"
                      >
                        {isChatLoading ? (
                          <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                        ) : (
                          <Send className="w-4 h-4" />
                        )}
                      </Button>
                    )}
                  </div>
                  {!chatInput.trim() && (
                    <Button onClick={handleChatMessage} disabled={!chatInput.trim() || isChatLoading}>
                      {isChatLoading ? (
                        <>
                          <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin mr-2"></div>
                          Processing...
                        </>
                      ) : (
                        <>
                          <Send className="w-4 h-4 mr-2" />
                          Send
                        </>
                      )}
                    </Button>
                  )}
                </div>

                {/* Enhanced Quick Actions */}
                <div className="space-y-3">
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-medium text-gray-600">Quick Actions:</span>
                    <Badge variant="outline" className="text-xs">
                      {chatMode === "document" ? "Document Analysis" : "General Legal"}
                    </Badge>
                  </div>
                  
                  <div className="grid grid-cols-2 gap-2">
                    {chatMode === "document" && extractedData?.fullText ? (
                      // Document-specific quick actions
                      <>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => {
                            setChatInput("Give me a comprehensive summary of this document")
                            handleChatMessage()
                          }}
                          className="flex items-center gap-2 hover:bg-blue-50"
                        >
                          <FileText className="w-4 h-4" />
                          Document Summary
                        </Button>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => {
                            setChatInput("Who are the parties involved in this case?")
                            handleChatMessage()
                          }}
                          className="flex items-center gap-2 hover:bg-green-50"
                        >
                          <Users className="w-4 h-4" />
                          Parties Involved
                        </Button>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => {
                            setChatInput("What are the key legal provisions mentioned?")
                            handleChatMessage()
                          }}
                          className="flex items-center gap-2 hover:bg-purple-50"
                        >
                          <BookOpen className="w-4 h-4" />
                          Legal Provisions
                        </Button>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => {
                            setChatInput("What is the court's decision or order?")
                            handleChatMessage()
                          }}
                          className="flex items-center gap-2 hover:bg-yellow-50"
                        >
                          <Gavel className="w-4 h-4" />
                          Court Decision
                        </Button>
                      </>
                    ) : (
                      // General legal quick actions (when in general mode OR no document)
                      <>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => {
                            setChatInput("What are my legal rights in criminal cases?")
                            handleChatMessage()
                          }}
                          className="flex items-center gap-2 hover:bg-blue-50"
                        >
                          <Scale className="w-4 h-4" />
                          Legal Rights
                        </Button>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => {
                            setChatInput("Explain the court procedure for filing a case")
                            handleChatMessage()
                          }}
                          className="flex items-center gap-2 hover:bg-green-50"
                        >
                          <FileCheck className="w-4 h-4" />
                          Court Procedures
                        </Button>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => {
                            setChatInput("What is the difference between bail and anticipatory bail?")
                            handleChatMessage()
                          }}
                          className="flex items-center gap-2 hover:bg-purple-50"
                        >
                          <HelpCircle className="w-4 h-4" />
                          Legal Concepts
                        </Button>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => {
                            setChatInput("Types of criminal cases in Indian law")
                            handleChatMessage()
                          }}
                          className="flex items-center gap-2 hover:bg-yellow-50"
                        >
                          <BookOpen className="w-4 h-4" />
                          Case Types
                        </Button>
                      </>
                    )}
                  </div>
                </div>

                {/* Mode Switcher */}
                {extractedData?.fullText && (
                  <div className="border-t pt-3">
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-gray-600">AI Assistant Mode:</span>
                      <div className="flex items-center gap-2">
                        <Badge variant="default" className="bg-blue-600">
                          📄 Document Analysis Available
                        </Badge>
                        <Badge variant="outline">
                          💬 General Chat Available
                        </Badge>
                      </div>
                    </div>
                  </div>
                )}

                {/* Footer */}
                <div className="text-xs text-gray-500 text-center border-t pt-2">
                  <span>Enhanced with Interactive Q&A System • Powered by LLaMA 3.1 • For informational purposes</span>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>

      {/* Floating Chatbot Button */}
      <div className="fixed bottom-6 right-6 z-50">
        <Button
          onClick={() => setShowChatbot(true)}
          className="w-14 h-14 rounded-full shadow-lg bg-blue-600 hover:bg-blue-700 text-white"
          size="lg"
        >
          <Bot className="w-6 h-6" />
        </Button>
      </div>

      {/* Chatbot Modal */}
      {showChatbot && (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
          <div className="w-full max-w-2xl h-[600px] bg-white rounded-lg shadow-xl">
            <LegalChatbot 
              documentText={extractedData?.fullText || null}
              onClose={() => setShowChatbot(false)}
            />
          </div>
        </div>
      )}
    </div>
  )
}
