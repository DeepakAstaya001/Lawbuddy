import { NextResponse } from "next/server"
import { spawn } from "child_process"
import path from "path"
import fs from "fs"
import { writeFile } from "fs/promises"

export async function POST(request) {
  try {
    const formData = await request.formData()
    const file = formData.get("file")

    if (!file) {
      return NextResponse.json({ error: "No file provided" }, { status: 400 })
    }

    if (file.type !== "application/pdf") {
      return NextResponse.json({ error: "Only PDF files are allowed" }, { status: 400 })
    }

    if (file.size > 50 * 1024 * 1024) {
      return NextResponse.json({ error: "File size exceeds 50MB limit" }, { status: 400 })
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

    // Call Python extraction script
    const pythonScriptPath = path.join(process.cwd(), "scripts", "extract_text.py")

    return new Promise((resolve) => {
      const pythonProcess = spawn("python", [pythonScriptPath, tempFilePath])

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

        if (code !== 0) {
          console.error("Python script error:", error)
          resolve(
            NextResponse.json({
              error: "Text extraction failed. Please ensure Python and PaddleOCR are installed.",
              extractedText: "",
              fileName: file.name,
              fileSize: file.size,
              processingTime: 0,
              wordCount: 0,
              characterCount: 0,
              extractionMethod: "Failed",
            }),
          )
          return
        }

        try {
          const processedData = JSON.parse(result)
          processedData.fileName = file.name
          processedData.fileSize = file.size
          resolve(NextResponse.json(processedData))
        } catch (parseError) {
          console.error("Error parsing Python output:", parseError)
          resolve(
            NextResponse.json({
              error: "Failed to parse extraction results",
              extractedText: result || "",
              fileName: file.name,
              fileSize: file.size,
              processingTime: 0,
              wordCount: result ? result.split(" ").length : 0,
              characterCount: result ? result.length : 0,
              extractionMethod: "Basic",
            }),
          )
        }
      })

      pythonProcess.on("error", (err) => {
        console.error("Failed to start Python process:", err)
        resolve(
          NextResponse.json({
            error: "Python not available. Please install Python and PaddleOCR.",
            extractedText: "",
            fileName: file.name,
            fileSize: file.size,
            processingTime: 0,
            wordCount: 0,
            characterCount: 0,
            extractionMethod: "Unavailable",
          }),
        )
      })
    })
  } catch (error) {
    console.error("API error:", error)
    return NextResponse.json(
      {
        error: "Internal server error",
        details: error.message,
      },
      { status: 500 },
    )
  }
}
