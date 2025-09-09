"use client"

import { useState, useRef, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import {
  Bot,
  User,
  Send,
  MessageSquare,
  FileText,
  Loader2,
  Trash2,
  Download,
  Sparkles,
  Scale,
  BookOpen,
  HelpCircle,
  Settings,
  Volume2,
  Copy
} from "lucide-react"

export default function LegalChatbot({ documentText = null, onClose = null }) {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      content: documentText 
        ? `Hello! I'm your Legal AI Assistant. I can help you with:\n\n📄 **Document Analysis** - Ask questions about your uploaded document\n💬 **General Legal Chat** - Discuss legal concepts and case scenarios\n📝 **Document Summary** - Get a comprehensive summary of your document\n⚖️ **Legal Guidance** - Get explanations about laws and procedures\n\nI have access to your processed document and can answer specific questions about it. How can I assist you today?`
        : `Hello! I'm your Legal AI Assistant. I can help you with:\n\n💬 **General Legal Chat** - Discuss legal concepts and case scenarios\n📚 **Legal Guidance** - Get explanations about laws and procedures\n⚖️ **Case Scenarios** - Analyze hypothetical legal situations\n📋 **Legal Procedures** - Understand court processes and requirements\n\nFeel free to ask me anything about Indian law, legal procedures, or specific case scenarios. How can I assist you today?`,
      timestamp: new Date(),
      mode: documentText ? 'document' : 'general'
    }
  ])
  const [inputMessage, setInputMessage] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [chatMode, setChatMode] = useState(documentText ? "document" : "general")
  const [isTyping, setIsTyping] = useState(false)
  const scrollAreaRef = useRef(null)
  const inputRef = useRef(null)
  const messagesEndRef = useRef(null)

  // Auto-scroll to bottom when new messages are added
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  // Focus input on mount
  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.focus()
    }
  }, [])

  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputMessage,
      timestamp: new Date(),
      mode: chatMode
    }

    setMessages(prev => [...prev, userMessage])
    const currentMessage = inputMessage
    setInputMessage("")
    setIsLoading(true)
    setIsTyping(true)

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: currentMessage,
          mode: chatMode,
          documentText: chatMode === 'document' ? documentText : null
        }),
      })

      const data = await response.json()

      if (data.error && !data.response) {
        throw new Error(data.error)
      }

      // Add typing delay for better UX
      setTimeout(() => {
        const botMessage = {
          id: Date.now() + 1,
          type: 'bot',
          content: data.response || 'I apologize, but I could not generate a proper response.',
          timestamp: new Date(),
          mode: data.mode || chatMode,
          isError: !data.success && data.error,
          warning: data.warning || null
        }

        setMessages(prev => [...prev, botMessage])
        setIsTyping(false)
      }, 1000) // 1 second typing simulation

    } catch (error) {
      console.error('Chat error:', error)
      setTimeout(() => {
        const errorMessage = {
          id: Date.now() + 1,
          type: 'bot',
          content: `I apologize, but I encountered an error while processing your request: ${error.message}\n\nPlease try rephrasing your question or check your connection.`,
          timestamp: new Date(),
          mode: chatMode,
          isError: true
        }
        setMessages(prev => [...prev, errorMessage])
        setIsTyping(false)
      }, 1000)
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  const clearChat = () => {
    const welcomeMessage = {
      id: 1,
      type: 'bot',
      content: documentText 
        ? `Chat cleared! I still have access to your document. How can I help you analyze it?`
        : `Chat cleared! I'm ready to help with legal questions and discussions. What would you like to know?`,
      timestamp: new Date(),
      mode: chatMode
    }
    setMessages([welcomeMessage])
  }

  const exportChat = () => {
    const chatExport = {
      timestamp: new Date().toISOString(),
      mode: chatMode,
      hasDocument: !!documentText,
      totalMessages: messages.length,
      messages: messages.map(msg => ({
        type: msg.type,
        content: msg.content,
        timestamp: msg.timestamp.toISOString(),
        mode: msg.mode
      }))
    }

    const blob = new Blob([JSON.stringify(chatExport, null, 2)], {
      type: 'application/json'
    })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `legal-chat-${new Date().toISOString().split('T')[0]}.json`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  const copyMessage = (content) => {
    navigator.clipboard.writeText(content).then(() => {
      // Could add a toast notification here
    })
  }

  const quickActions = [
    {
      text: documentText ? "Summarize this document" : "What are my legal rights?",
      icon: <FileText className="w-3 h-3" />
    },
    {
      text: documentText ? "What are the key legal provisions?" : "Explain legal procedure",
      icon: <BookOpen className="w-3 h-3" />
    },
    {
      text: documentText ? "Who are the parties involved?" : "Types of legal cases",
      icon: <Users className="w-3 h-3" />
    },
    {
      text: "Help me understand this better",
      icon: <HelpCircle className="w-3 h-3" />
    }
  ]

  return (
    <Card className="h-full flex flex-col bg-gradient-to-br from-white to-gray-50">
      <CardHeader className="pb-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-t-lg">
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center gap-2">
            <div className="relative">
              <Bot className="w-5 h-5" />
              <Sparkles className="w-3 h-3 absolute -top-1 -right-1 animate-pulse" />
            </div>
            Legal AI Assistant
          </CardTitle>
          <div className="flex items-center gap-2">
            <Button
              variant="ghost"
              size="sm"
              onClick={exportChat}
              className="h-8 text-white hover:bg-white/20"
              title="Export Chat"
            >
              <Download className="w-4 h-4" />
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={clearChat}
              className="h-8 text-white hover:bg-white/20"
              title="Clear Chat"
            >
              <Trash2 className="w-4 h-4" />
            </Button>
            {onClose && (
              <Button
                variant="ghost"
                size="sm"
                onClick={onClose}
                className="h-8 text-white hover:bg-white/20"
                title="Close Chat"
              >
                ✕
              </Button>
            )}
          </div>
        </div>
        <CardDescription className="text-blue-100">
          Powered by advanced AI • Ask questions, get legal guidance, analyze documents
        </CardDescription>
        
        {/* Mode Selector */}
        <div className="flex items-center gap-2 pt-2">
          <span className="text-sm font-medium text-blue-100">Mode:</span>
          <Select value={chatMode} onValueChange={setChatMode}>
            <SelectTrigger className="w-40 h-8 bg-white/20 border-white/30 text-white">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="general">
                <div className="flex items-center gap-2">
                  <MessageSquare className="w-4 h-4" />
                  General Chat
                </div>
              </SelectItem>
              {documentText && (
                <SelectItem value="document">
                  <div className="flex items-center gap-2">
                    <FileText className="w-4 h-4" />
                    Document Q&A
                  </div>
                </SelectItem>
              )}
            </SelectContent>
          </Select>
          <Badge variant="secondary" className="text-xs bg-white/20 text-white border-white/30">
            {chatMode === 'document' ? '📄 Analyzing Document' : '💬 General Chat'}
          </Badge>
        </div>
      </CardHeader>

      {/* Chat Messages */}
      <CardContent className="flex-1 flex flex-col gap-3 pb-3 overflow-hidden">
        <div ref={scrollAreaRef} className="flex-1 overflow-y-auto pr-2 space-y-4">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex gap-3 ${
                message.type === 'user' ? 'justify-end' : 'justify-start'
              }`}
            >
              <div className={`flex gap-3 max-w-[85%] ${
                message.type === 'user' ? 'flex-row-reverse' : 'flex-row'
              }`}>
                {/* Avatar */}
                <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                  message.type === 'user' 
                    ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg' 
                    : message.isError 
                      ? 'bg-red-100 text-red-600'
                      : 'bg-gradient-to-r from-gray-100 to-gray-200 text-gray-700 shadow-md'
                }`}>
                  {message.type === 'user' ? (
                    <User className="w-4 h-4" />
                  ) : (
                    <Bot className="w-4 h-4" />
                  )}
                </div>

                {/* Message Content */}
                <div className={`relative rounded-2xl px-4 py-3 shadow-sm ${
                  message.type === 'user'
                    ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white'
                    : message.isError
                      ? 'bg-red-50 text-red-800 border border-red-200'
                      : 'bg-white text-gray-800 border border-gray-200'
                }`}>
                  <div className="whitespace-pre-wrap text-sm leading-relaxed">
                    {message.content}
                  </div>
                  
                  {/* Message footer */}
                  <div className={`text-xs mt-2 flex items-center justify-between ${
                    message.type === 'user' ? 'text-blue-200' : 'text-gray-500'
                  }`}>
                    <div className="flex items-center gap-2">
                      <span>{message.timestamp.toLocaleTimeString()}</span>
                      {message.mode && (
                        <Badge variant="outline" className={`h-4 text-xs ${
                          message.type === 'user' ? 'border-blue-300 text-blue-200' : ''
                        }`}>
                          {message.mode === 'document' ? '📄' : '💬'}
                        </Badge>
                      )}
                      {message.warning && (
                        <Badge variant="outline" className="h-4 text-xs border-yellow-300 text-yellow-600">
                          ⚠️
                        </Badge>
                      )}
                    </div>
                    
                    {message.type === 'bot' && (
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => copyMessage(message.content)}
                        className="h-6 w-6 p-0 opacity-50 hover:opacity-100"
                      >
                        <Copy className="w-3 h-3" />
                      </Button>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))}

          {/* Typing Indicator */}
          {isTyping && (
            <div className="flex gap-3 justify-start">
              <div className="flex gap-3 max-w-[85%]">
                <div className="w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 bg-gradient-to-r from-gray-100 to-gray-200 text-gray-700">
                  <Bot className="w-4 h-4" />
                </div>
                <div className="rounded-2xl px-4 py-3 bg-white border border-gray-200 shadow-sm">
                  <div className="flex items-center gap-2">
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                    </div>
                    <span className="text-sm text-gray-500">AI is thinking...</span>
                  </div>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        <Separator />

        {/* Quick Actions */}
        {messages.length <= 1 && !isLoading && (
          <div className="flex flex-wrap gap-2 mb-3">
            {quickActions.map((action, index) => (
              <Button
                key={index}
                variant="outline"
                size="sm"
                onClick={() => setInputMessage(action.text)}
                className="h-8 text-xs flex items-center gap-1 hover:bg-blue-50 hover:border-blue-300"
              >
                {action.icon}
                {action.text}
              </Button>
            ))}
          </div>
        )}

        {/* Input Area */}
        <div className="flex gap-2">
          <div className="flex-1 relative">
            <Input
              ref={inputRef}
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder={
                chatMode === 'document' 
                  ? "Ask about the document..." 
                  : "Ask about legal concepts, cases, or scenarios..."
              }
              disabled={isLoading}
              className="pr-12 border-gray-300 focus:border-blue-500 focus:ring-blue-500"
            />
            {inputMessage.trim() && (
              <Button
                size="sm"
                onClick={sendMessage}
                disabled={isLoading}
                className="absolute right-1 top-1 h-8 w-8 p-0 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
              >
                {isLoading ? (
                  <Loader2 className="w-4 h-4 animate-spin" />
                ) : (
                  <Send className="w-4 h-4" />
                )}
              </Button>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="text-xs text-gray-500 text-center">
          <span>Powered by LLaMA 3.1 • For informational purposes • Consult a qualified lawyer for legal advice</span>
        </div>
      </CardContent>
    </Card>
  )
}
