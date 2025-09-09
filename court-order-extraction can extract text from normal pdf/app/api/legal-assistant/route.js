import { NextResponse } from "next/server"

export async function POST(request) {
  try {
    const { message, context, history } = await request.json()

    if (!message) {
      return NextResponse.json({ error: "No message provided" }, { status: 400 })
    }

    // Simple legal assistant responses based on message content
    const lowerMessage = message.toLowerCase()
    let response =
      "I understand you're asking about legal matters. Could you please be more specific about what you'd like to know?"

    // Legal advice patterns
    if (lowerMessage.includes("next steps") || lowerMessage.includes("what should")) {
      response =
        "Based on legal documents like this, typical next steps might include: 1) Reviewing all terms and conditions carefully, 2) Consulting with a qualified lawyer for personalized advice, 3) Ensuring compliance with any deadlines mentioned, 4) Gathering supporting documentation if needed. Please consult with a legal professional for advice specific to your situation."
    } else if (lowerMessage.includes("legal implications") || lowerMessage.includes("implications")) {
      response =
        "Legal implications can vary significantly based on the specific circumstances and jurisdiction. This document appears to contain important legal information that could affect rights, obligations, or legal standing. I strongly recommend consulting with a qualified attorney who can provide personalized legal advice based on your specific situation and local laws."
    } else if (
      lowerMessage.includes("key points") ||
      lowerMessage.includes("summary") ||
      lowerMessage.includes("main")
    ) {
      if (context && context.extractedText) {
        response = `Based on the document analysis, here are some key observations: The document appears to be a ${context.documentAnalysis?.type || "legal document"}. ${context.summary || "Key details have been extracted and processed."} For a complete understanding, please review the full extracted text and consult with a legal professional.`
      } else {
        response =
          "To provide key points, I would need access to the processed document content. Please ensure a document has been successfully analyzed first."
      }
    } else if (
      lowerMessage.includes("deadline") ||
      lowerMessage.includes("time limit") ||
      lowerMessage.includes("due date")
    ) {
      response =
        "Deadlines in legal documents are critical. Please carefully review the document for any specific dates, time limits, or deadlines mentioned. Missing legal deadlines can have serious consequences. If you're unsure about any deadlines, consult with a lawyer immediately."
    } else if (
      lowerMessage.includes("court") ||
      lowerMessage.includes("hearing") ||
      lowerMessage.includes("appearance")
    ) {
      response =
        "Court-related matters require careful attention to procedures and deadlines. If this document relates to court proceedings, ensure you understand any required appearances, filing deadlines, or procedural requirements. Consider consulting with an attorney familiar with court procedures in your jurisdiction."
    } else if (lowerMessage.includes("appeal") || lowerMessage.includes("challenge")) {
      response =
        "Appeals and legal challenges typically have strict time limits and procedural requirements. If you're considering an appeal or challenge, it's crucial to act quickly and consult with a qualified attorney who can advise you on the specific procedures, deadlines, and merits of your case."
    } else if (lowerMessage.includes("rights") || lowerMessage.includes("obligations")) {
      response =
        "Legal documents often establish or modify rights and obligations. Understanding these fully requires careful analysis of the specific language used and how it applies to your situation. A qualified attorney can help you understand your rights and obligations under this document."
    } else if (lowerMessage.includes("hello") || lowerMessage.includes("hi") || lowerMessage.includes("help")) {
      response =
        "Hello! I'm here to help you understand legal documents. I can provide general information about legal concepts, but please remember that I cannot provide specific legal advice. For personalized legal guidance, always consult with a qualified attorney. How can I assist you with understanding this document?"
    }

    return NextResponse.json({
      response: response,
      timestamp: new Date().toISOString(),
      disclaimer:
        "This is general information only and not legal advice. Consult with a qualified attorney for legal advice specific to your situation.",
    })
  } catch (error) {
    console.error("Legal assistant error:", error)
    return NextResponse.json(
      {
        error: "Failed to process message",
        response:
          "I apologize, but I'm having trouble processing your request right now. Please try again, and remember to consult with a qualified attorney for specific legal advice.",
      },
      { status: 500 },
    )
  }
}
