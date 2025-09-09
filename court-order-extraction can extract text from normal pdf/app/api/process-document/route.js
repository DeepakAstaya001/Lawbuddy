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
      return NextResponse.json({ error: "File size exceeds 100MB limit" }, { status: 400 })
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

    // Call Python processing script
    const pythonScriptPath = path.join(process.cwd(), "scripts", "document_processor.py")

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
        console.log(`Python stdout: ${result}`)
        console.log(`Python stderr: ${error}`)

        if (code !== 0) {
          console.error("Python script error:", error)

          // Return fallback response with actual file info but indicate processing failed
          resolve(
            NextResponse.json({
              error: `Python processing failed (exit code: ${code}). ${error}`,
              extractedText: `Failed to process ${file.name}. Python Error: ${error}`,
              summary:
                "Document processing failed. Please check system configuration and install required Python libraries.",
              extractionMethod: "Fallback",
              documentType: file.type.startsWith("image/") ? "scanned" : "text_based",
              processingTime: 2.5,
              wordCount: 0,
              characterCount: 0,
              fileName: file.name,
              fileSize: file.size,
              fileType: file.type,
              documentAnalysis: {
                type: "Unknown",
                confidence: 0.0,
                legalTopics: [],
                complexity: "unknown",
                keyEntities: {},
              },
              structureAnalysis: {},
              timestamp: new Date().toISOString(),
              options: options,
              pythonError: error,
              pythonExitCode: code,
              librariesUsed: {
                advanced_libs_available: false,
                basic_extraction: true,
              },
            }),
          )
          return
        }

        try {
          const processedData = JSON.parse(result)

          // Add file metadata to the response
          processedData.fileName = file.name
          processedData.fileSize = file.size
          processedData.fileType = file.type
          processedData.uploadTimestamp = new Date().toISOString()

          console.log("Processing successful:", {
            fileName: file.name,
            extractedLength: processedData.extractedText?.length || 0,
            method: processedData.extractionMethod,
            hasError: !!processedData.error,
          })

          resolve(NextResponse.json(processedData))
        } catch (parseError) {
          console.error("Error parsing Python output:", parseError)
          console.error("Raw Python output:", result)

          // Return fallback with raw output for debugging
          resolve(
            NextResponse.json({
              error: "Failed to parse processing results",
              extractedText: result || "No output from Python script",
              summary: "Processing completed but results could not be parsed properly.",
              extractionMethod: "Fallback",
              documentType: file.type.startsWith("image/") ? "scanned" : "text_based",
              processingTime: 3.0,
              wordCount: result ? result.split(" ").length : 0,
              characterCount: result ? result.length : 0,
              fileName: file.name,
              fileSize: file.size,
              fileType: file.type,
              rawOutput: result,
              parseError: parseError.message,
              timestamp: new Date().toISOString(),
              options: options,
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
            extractionMethod: "Fallback",
            documentType: file.type.startsWith("image/") ? "scanned" : "text_based",
            processingTime: 1.0,
            wordCount: 0,
            characterCount: 0,
            fileName: file.name,
            fileSize: file.size,
            fileType: file.type,
            systemError: err.message,
            timestamp: new Date().toISOString(),
            options: options,
            librariesUsed: {
              advanced_libs_available: false,
              python_available: false,
            },
          }),
        )
      })
    })
  } catch (error) {
    console.error("Document processing error:", error)
    return NextResponse.json(
      {
        error: "Internal server error during processing",
        details: error.message,
        timestamp: new Date().toISOString(),
      },
      { status: 500 },
    )
  }
}
