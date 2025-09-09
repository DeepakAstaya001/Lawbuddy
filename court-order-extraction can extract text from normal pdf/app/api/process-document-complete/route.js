import { NextResponse } from "next/server"
import { spawn } from "child_process"
import path from "path"
import fs from "fs"
import { writeFile } from "fs/promises"

export async function POST(request) {
  try {
    const formData = await request.formData()
    const file = formData.get("file")
    const options = {
      ocrEnabled: formData.get("ocrEnabled") === "true",
      signatureDetection: formData.get("signatureDetection") === "true",
      summaryLength: formData.get("summaryLength") || "medium",
      language: formData.get("language") || "en",
    }

    if (!file) {
      return NextResponse.json({ error: "No file provided" }, { status: 400 })
    }

    // Validate file type and size
    if (file.type !== "application/pdf" && !file.type.startsWith("image/")) {
      return NextResponse.json({ error: "Only PDF files and images are allowed" }, { status: 400 })
    }

    if (file.size > 100 * 1024 * 1024) {
      return NextResponse.json({ error: "File size exceeds 100MB limit" }, { status: 100 })
    }

    // Save uploaded file temporarily
    const bytes = await file.arrayBuffer()
    const buffer = Buffer.from(bytes)

    const tempDir = path.join(process.cwd(), "temp")
    if (!fs.existsSync(tempDir)) {
      fs.mkdirSync(tempDir, { recursive: true })
    }

    const tempFilePath = path.join(tempDir, `upload_${Date.now()}_${file.name}`)
    await writeFile(tempFilePath, buffer)

    // Call the complete processing pipeline using clean processor
    const pythonScriptPath = path.join(process.cwd(), "scripts", "clean_processor.py")

    return new Promise((resolve, reject) => {
      const pythonProcess = spawn("python", [pythonScriptPath, tempFilePath, JSON.stringify(options)])

      let result = ""
      let error = ""

      pythonProcess.stdout.on("data", (data) => {
        result += data.toString()
      })

      pythonProcess.stderr.on("data", (data) => {
        error += data.toString()
      })

      pythonProcess.on("close", (code) => {
        // Clean up temp file
        try {
          fs.unlinkSync(tempFilePath)
        } catch (e) {
          console.error("Error cleaning up temp file:", e)
        }

        console.log(`Python process exited with code: ${code}`)
        if (error) console.log(`Python stderr: ${error}`)

        if (code !== 0) {
          console.error("Python script error:", error)

          // Return fallback response with actual file info but indicate processing failed
          resolve(
            NextResponse.json({
              error: `Complete processing failed (exit code: ${code}). ${error}`,
              extractedText: `Failed to process ${file.name}. Python Error: ${error}`,
              summary: "Document processing failed. Please check system configuration and install required Python libraries.",
              metadata: {},
              extractionMethod: "Fallback",
              documentType: file.type.startsWith("image/") ? "scanned" : "text_based",
              processingTime: 0,
              wordCount: 0,
              characterCount: 0,
              fileName: file.name,
              fileSize: file.size,
              fileType: file.type,
              documentAnalysis: {
                type: "Unknown",
                confidence: 0.0,
                complexity: "unknown",
                keyEntities: {},
              },
              structureAnalysis: {},
              timestamp: new Date().toISOString(),
              options: options,
              pythonError: error,
              pythonExitCode: code,
            }),
          )
          return
        }

        try {
          // Parse the clean JSON output from the clean processor
          const processedData = JSON.parse(result)

          // Add file metadata to the response
          processedData.fileName = file.name
          processedData.fileSize = file.size
          processedData.fileType = file.type
          processedData.uploadTimestamp = new Date().toISOString()

          console.log("Complete processing successful:", {
            fileName: file.name,
            extractedLength: processedData.extractedText?.length || 0,
            hasMetadata: !!processedData.metadata && Object.keys(processedData.metadata).length > 0,
            hasSummary: !!processedData.summary && processedData.summary.length > 10,
            method: processedData.extractionMethod,
            hasError: !!processedData.error,
            success: processedData.success
          })

          resolve(NextResponse.json(processedData))
        } catch (parseError) {
          console.error("Error parsing clean processor output:", parseError.message)
          console.error("Raw output length:", result.length)
          console.error("First 200 characters:", result.substring(0, 200))

          // The clean processor should always return valid JSON, so this is unexpected
          resolve(
            NextResponse.json({
              error: "Clean processor returned invalid JSON",
              extractedText: result.substring(0, 1000) || "No output from clean processor",
              summary: "Processing completed but clean processor failed to return valid JSON.",
              metadata: {},
              extractionMethod: "Fallback",
              documentType: file.type.startsWith("image/") ? "scanned" : "text_based",
              processingTime: 0,
              wordCount: 0,
              characterCount: 0,
              fileName: file.name,
              fileSize: file.size,
              fileType: file.type,
              parseError: parseError.message,
              timestamp: new Date().toISOString(),
              options: options,
              success: false
            }),
          )
        }
      })

      pythonProcess.on("error", (err) => {
        console.error("Failed to start Python process:", err)

        // Return fallback response when Python process fails to start
        resolve(
          NextResponse.json({
            error: "Failed to start Python processing. Python may not be installed or configured properly.",
            extractedText: `Could not process ${file.name}. Python environment may not be configured properly.`,
            summary: "Document processing unavailable. Please check Python installation and dependencies.",
            metadata: {},
            extractionMethod: "Fallback",
            documentType: file.type.startsWith("image/") ? "scanned" : "text_based",
            processingTime: 0,
            wordCount: 0,
            characterCount: 0,
            fileName: file.name,
            fileSize: file.size,
            fileType: file.type,
            systemError: err.message,
            timestamp: new Date().toISOString(),
            options: options,
          }),
        )
      })
    })
  } catch (error) {
    console.error("Complete document processing error:", error)
    return NextResponse.json(
      {
        error: "Internal server error during complete processing",
        details: error.message,
        timestamp: new Date().toISOString(),
      },
      { status: 500 },
    )
  }
}
