"use client"

import type React from "react"

import { useState, useRef, useEffect } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Loader2, ArrowUp, MessageCircle, X, Clock } from "lucide-react"
import { apiService } from "@/lib/api"
import { parseAiResponse } from "@/lib/parseAiResponse"
import { AiChatBubble } from "@/components/ai-chat-bubble"

export function SearchPrompt() {
  const [prompt, setPrompt] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [loadingTime, setLoadingTime] = useState(0)
  const [followUpMessage, setFollowUpMessage] = useState<string | null>(null)
  const [conversationMessages, setConversationMessages] = useState<string[]>([])
  const [sessionId, setSessionId] = useState<string | undefined>(undefined)
  const [isFocused, setIsFocused] = useState(false)
  const [isHovered, setIsHovered] = useState(false)
  const textareaRef = useRef<HTMLTextAreaElement>(null)
  const router = useRouter()

  // Timer for loading progress
  useEffect(() => {
    let interval: NodeJS.Timeout
    if (isLoading) {
      interval = setInterval(() => {
        setLoadingTime(prev => prev + 1)
      }, 1000)
    } else {
      setLoadingTime(0)
    }
    return () => clearInterval(interval)
  }, [isLoading])

  const getLoadingMessage = () => {
    if (loadingTime < 30) {
      return "Analyzing your request..."
    } else if (loadingTime < 60) {
      return "Searching for concerts..."
    } else if (loadingTime < 120) {
      return "Processing results..."
    } else {
      return "Almost done..."
    }
  }

  const handleSubmit = async () => {
    if (!prompt.trim() || isLoading) return

    setIsLoading(true)
    setFollowUpMessage(null)

    try {
      let messageToSend = prompt;
      if (conversationMessages.length > 0) {
        // This is a follow-up response, concatenate with all previous messages
        messageToSend = `${conversationMessages.join(' ')} ${prompt}`;
        console.log('Concatenating messages:', { 
          previous: conversationMessages, 
          followUp: prompt, 
          combined: messageToSend 
        });
      }

      const response = await apiService.chat({
        message: messageToSend,
        user_id: "default_user",
        session_id: sessionId
      })

      setSessionId(response.session_id)

      const parsedData = parseAiResponse(response.response)

      if (parsedData.isFollowUpQuestion && parsedData.followUpMessage) {
        // Add the current prompt to conversation history
        setConversationMessages(prev => [...prev, prompt]);
        setFollowUpMessage(parsedData.followUpMessage)
        setPrompt("")
      } else {
        const responseData = {
          query: messageToSend,
          response: response.response,
          session_id: response.session_id,
          timestamp: Date.now()
        }
        
        sessionStorage.setItem('concert_search_results', JSON.stringify(responseData))
        
        const queryParams = new URLSearchParams({
          q: messageToSend,
          session_id: response.session_id
        })
        
        router.push(`/results?${queryParams.toString()}`)
        
        setConversationMessages([])
        setFollowUpMessage(null)
      }
    } catch (error: any) {
      console.error("Error sending message:", error)
      
      let errorMessage = "Sorry, there was an error processing your request. Please try again.";
      let errorType = "general";
      
      if (error.apiError?.isQuotaExceeded) {
        errorMessage = "API quota limit reached. Please try again later (quota resets daily).";
        errorType = "quota_exceeded";
      } else if (error.apiError?.isServerError) {
        errorMessage = "Server error occurred. Please try again in a few moments.";
        errorType = "server_error";
      } else if (error.message?.includes('timeout')) {
        errorMessage = "The request took too long to process. Please try with a simpler query or try again later.";
        errorType = "timeout";
      }
      
      const errorData = {
        query: prompt,
        response: errorMessage,
        session_id: "",
        timestamp: Date.now(),
        error: true,
        errorType: errorType
      }
      
      sessionStorage.setItem('concert_search_results', JSON.stringify(errorData))
      
      const queryParams = new URLSearchParams({
        q: prompt
      })
      router.push(`/results?${queryParams.toString()}`)
    } finally {
      setIsLoading(false)
    }
  }

  const handleDismissFollowUp = () => {
    setFollowUpMessage(null)
    setConversationMessages([])
    setSessionId(undefined)
    setPrompt("")
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto"
      const minHeight = 48
      const scrollHeight = textareaRef.current.scrollHeight
      textareaRef.current.style.height = `${Math.max(minHeight, scrollHeight)}px`
    }
  }, [prompt])

  return (
    <div className="w-full max-w-4xl space-y-4">
      <div className="relative">
        <div 
          className={`relative rounded-lg transition-all duration-300 ${
            isFocused 
              ? 'shadow-[0_0_20px_rgba(168,85,247,0.4),0_0_40px_rgba(236,72,153,0.2),0_0_60px_rgba(59,130,246,0.1)]' 
              : isHovered
              ? 'shadow-[0_0_15px_rgba(168,85,247,0.3),0_0_30px_rgba(236,72,153,0.15)]'
              : 'shadow-none'
          }`}
          onMouseEnter={() => setIsHovered(true)}
          onMouseLeave={() => setIsHovered(false)}
        >
          <textarea
            ref={textareaRef}
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            onKeyDown={handleKeyDown}
            onFocus={() => setIsFocused(true)}
            onBlur={() => setIsFocused(false)}
            placeholder={
              followUpMessage 
                ? "Please provide the additional information requested above..."
                : "Tell me about your music taste and where you want to find concerts..."
            }
            className={`w-full min-h-[48px] max-h-[300px] p-3 pr-12 text-white bg-gray-800/50 border rounded-lg resize-none focus:outline-none placeholder-gray-400 transition-all duration-300 ${
              isFocused 
                ? 'border-purple-400/50 bg-gray-800/70' 
                : isHovered
                ? 'border-purple-500/30 bg-gray-800/60'
                : 'border-gray-700 bg-gray-800/50'
            }`}
            disabled={isLoading}
          />
          <Button
            onClick={handleSubmit}
            disabled={!prompt.trim() || isLoading}
            className="absolute top-3 right-3 bg-purple-600 hover:bg-purple-700 text-white rounded-md p-2 h-auto z-20"
          >
            {isLoading ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <ArrowUp className="h-4 w-4" />
            )}
          </Button>
        </div>
      </div>

      {/* Loading progress indicator - moved below search box */}
      {isLoading && (
        <div className="bg-gray-800/30 border border-gray-700 rounded-lg p-4 space-y-3 animate-in slide-in-from-top-2 duration-300 mt-2">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Clock className="h-4 w-4 text-purple-400" />
              <span className="text-sm font-medium text-purple-400">{getLoadingMessage()}</span>
            </div>
          </div>
          
          {/* Progress bar */}
          <div className="w-full bg-gray-700 rounded-full h-2">
            <div 
              className="bg-gradient-to-r from-purple-500 to-pink-500 h-2 rounded-full transition-all duration-300"
              style={{ 
                width: `${Math.min((loadingTime / 75) * 100, 100)}%` 
              }}
            ></div>
          </div>
          
          <p className="text-xs text-gray-500">
            {loadingTime > 60 ? 
              "This is taking longer than usual. The AI is processing a complex request..." : 
              "Please wait while the AI analyzes your request and searches for concerts..."
            }
          </p>
        </div>
      )}

      {followUpMessage && (
        <div className="bg-gray-800/30 border border-gray-700 rounded-lg p-4 space-y-4 animate-in slide-in-from-top-2 duration-300">
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-2">
              <div className="p-1.5 bg-purple-500/20 rounded-lg">
                <MessageCircle className="h-4 w-4 text-purple-400" />
              </div>
              <span className="text-sm font-medium text-purple-400">Concert Scout AI needs more info:</span>
            </div>
            <Button
              variant="ghost"
              size="sm"
              onClick={handleDismissFollowUp}
              className="text-gray-400 hover:text-white h-6 w-6 p-0"
            >
              <X className="h-4 w-4" />
            </Button>
          </div>
          
          <AiChatBubble
            title="Concert Scout AI"
            message={followUpMessage}
          />
          
          <p className="text-xs text-gray-500">
            Please provide the requested information in the search box above and press Enter to continue.
          </p>
        </div>
      )}
    </div>
  )
}
