import { NextResponse } from "next/server"

export async function POST(request) {
  try {
    const { query, documentData } = await request.json()

    if (!query || !documentData) {
      return NextResponse.json({ error: "Missing query or document data" }, { status: 400 })
    }

    // Simple Q&A processing based on extracted text
    const extractedText = documentData.extractedText || ""
    let answer = "I couldn't find relevant information in the document to answer your question."

    // Basic keyword matching for common legal questions
    const lowerQuery = query.toLowerCase()
    const lowerText = extractedText.toLowerCase()

    if (lowerQuery.includes("parties") || lowerQuery.includes("involved")) {
      // Look for party information
      const partyMatches = extractedText.match(
        /(?:plaintiff|defendant|petitioner|respondent|appellant|appellee)[\s:]+([^\n.]+)/gi,
      )
      if (partyMatches) {
        answer = `Based on the document, the parties involved appear to be: ${partyMatches.slice(0, 3).join(", ")}`
      }
    } else if (lowerQuery.includes("date") || lowerQuery.includes("when")) {
      // Look for dates
      const dateMatches = extractedText.match(
        /\d{1,2}[/\-.]\d{1,2}[/\-.]\d{2,4}|\d{1,2}\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{2,4}/gi,
      )
      if (dateMatches) {
        answer = `Key dates mentioned in the document: ${dateMatches.slice(0, 3).join(", ")}`
      }
    } else if (lowerQuery.includes("decision") || lowerQuery.includes("judgment") || lowerQuery.includes("ruling")) {
      // Look for decision/judgment information
      const decisionKeywords = [
        "ordered",
        "decreed",
        "decided",
        "ruled",
        "judgment",
        "dismissed",
        "allowed",
        "granted",
        "denied",
      ]
      const sentences = extractedText.split(/[.!?]+/)
      const relevantSentences = sentences.filter((sentence) =>
        decisionKeywords.some((keyword) => sentence.toLowerCase().includes(keyword)),
      )
      if (relevantSentences.length > 0) {
        answer = `The key decision appears to be: ${relevantSentences[0].trim()}`
      }
    } else if (lowerQuery.includes("amount") || lowerQuery.includes("fine") || lowerQuery.includes("penalty")) {
      // Look for monetary amounts
      const amountMatches = extractedText.match(/(?:Rs\.?|₹|INR)\s*[\d,]+(?:\.\d{2})?/gi)
      if (amountMatches) {
        answer = `Monetary amounts mentioned: ${amountMatches.slice(0, 3).join(", ")}`
      }
    } else {
      // General search in the text
      const words = lowerQuery.split(" ").filter((word) => word.length > 3)
      const relevantSentences = extractedText
        .split(/[.!?]+/)
        .filter((sentence) => words.some((word) => sentence.toLowerCase().includes(word)))
      if (relevantSentences.length > 0) {
        answer = `Relevant information: ${relevantSentences[0].trim()}`
      }
    }

    return NextResponse.json({
      answer: answer,
      query: query,
      timestamp: new Date().toISOString(),
    })
  } catch (error) {
    console.error("Q&A processing error:", error)
    return NextResponse.json(
      {
        error: "Failed to process query",
        answer: "Sorry, I encountered an error while processing your question. Please try again.",
      },
      { status: 500 },
    )
  }
}
