import { NextResponse } from 'next/server'
import { spawn } from 'child_process'
import path from 'path'

export async function POST(request) {
  try {
    const { message, mode = 'general', documentText = null } = await request.json()

    if (!message) {
      return NextResponse.json(
        { error: 'Message is required' },
        { status: 400 }
      )
    }

    // Path to the working chat handler - FIXED PATH
    const scriptPath = path.join(process.cwd(), 'scripts', 'chat_handler_working.py')
    
    // Interpreter is configurable so the route works outside the original dev machine
    const pythonPath = process.env.PYTHON_PATH || 'python'

    return new Promise((resolve) => {
      const pythonProcess = spawn(pythonPath, [scriptPath], {
        stdio: ['pipe', 'pipe', 'pipe']
      })

      let output = ''
      let error = ''
      let timeoutId
      const finish = (response) => {
        clearTimeout(timeoutId)
        resolve(response)
      }

      pythonProcess.on('error', (err) => {
        console.error('Failed to start Python chat process:', err)
        finish(NextResponse.json(
          {
            error: 'Python not available',
            response: 'The chat service is not configured correctly. Please check the Python installation or PYTHON_PATH.',
            details: err.message
          },
          { status: 500 }
        ))
      })

      // Send input data to Python script
      const inputData = JSON.stringify({
        message,
        mode,
        documentText
      })
      
      pythonProcess.stdin.write(inputData)
      pythonProcess.stdin.end()

      pythonProcess.stdout.on('data', (data) => {
        output += data.toString()
      })

      pythonProcess.stderr.on('data', (data) => {
        error += data.toString()
      })

      pythonProcess.on('close', (code) => {
        if (code !== 0) {
          console.error('Python chat error:', error)
          finish(NextResponse.json(
            { 
              error: 'Chat processing failed', 
              response: 'Sorry, I encountered an error while processing your request. Please try again.',
              details: error 
            },
            { status: 500 }
          ))
          return
        }

        try {
          // Parse the JSON response from Python
          const result = JSON.parse(output.trim())
          
          finish(NextResponse.json({
            response: result.response || 'I apologize, but I could not generate a proper response.',
            mode: result.mode || mode,
            timestamp: new Date().toISOString(),
            success: result.success || false,
            using_document: result.using_document || false,
            ai_powered: result.ai_powered || false,
            processing_time: result.processing_time || 0
          }))
        } catch (parseError) {
          console.error('Failed to parse Python output:', parseError)
          console.error('Raw output:', output)
          
          // Fallback response
          finish(NextResponse.json({
            response: output.trim() || 'Sorry, I could not process your request properly.',
            mode: mode,
            timestamp: new Date().toISOString(),
            success: false,
            warning: 'Response formatting issue'
          }))
        }
      })

      // Set a timeout to prevent hanging
      timeoutId = setTimeout(() => {
        pythonProcess.kill('SIGTERM')
        finish(NextResponse.json({
          response: 'The request took too long to process. Please try again with a shorter question.',
          mode: mode,
          timestamp: new Date().toISOString(),
          success: false,
          timeout: true
        }))
      }, 30000) // 30 second timeout
    })

  } catch (error) {
    console.error('Chat API error:', error)
    return NextResponse.json(
      { 
        error: 'Internal server error', 
        response: 'Sorry, there was a technical issue. Please try again.',
        details: error.message 
      },
      { status: 500 }
    )
  }
}
