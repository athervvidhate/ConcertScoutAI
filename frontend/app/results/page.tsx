"use client"

import { Suspense, useEffect, useState } from "react"
import Link from "next/link"
import { useSearchParams } from "next/navigation"
import { Button } from "@/components/ui/button"
import { ConcertResults } from "@/components/concert-results"
import { ResultsSkeleton } from "@/components/results-skeleton"
import { ArrowLeft, Sparkles } from "lucide-react"

export default function ResultsPage() {
  const searchParams = useSearchParams()
  const [responseData, setResponseData] = useState<{
    query: string
    response: string
    session_id: string
    timestamp: number
    error?: boolean
    errorType?: string
  } | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Get query from URL as a fallback
    const queryFromUrl = searchParams.get("q") || ""
    const sessionIdFromUrl = searchParams.get("session_id") || ""

    // Try to get data from sessionStorage
    const storedData = sessionStorage.getItem('concert_search_results')
    
    if (storedData) {
      try {
        const parsedData = JSON.parse(storedData)
        setResponseData(parsedData)
      } catch (error) {
        console.error("Error parsing stored data:", error)
        // Fallback to URL params if available
        setResponseData({
          query: queryFromUrl,
          response: "Error loading results. Please try searching again.",
          session_id: sessionIdFromUrl,
          timestamp: Date.now(),
          error: true
        })
      }
    } else {
      // No stored data, create error state
      setResponseData({
        query: queryFromUrl,
        response: "No results found. Please try searching again.",
        session_id: sessionIdFromUrl,
        timestamp: Date.now(),
        error: true
      })
    }
    
    setIsLoading(false)
  }, [searchParams])

  if (isLoading) {
    return (
      <main className="flex min-h-screen flex-col p-4 md:p-24">
        <div className="w-full max-w-6xl mx-auto">
          <ResultsSkeleton />
        </div>
      </main>
    )
  }

  if (!responseData) {
    return (
      <main className="flex min-h-screen flex-col p-4 md:p-24">
        <div className="w-full max-w-6xl mx-auto space-y-8">
          <div className="text-center py-12">
            <h2 className="text-2xl font-bold text-white mb-4">No results found</h2>
            <p className="text-gray-400 mb-8">
              There was an issue loading your search results. Please try again.
            </p>
            <Link href="/">
              <Button className="bg-purple-600 hover:bg-purple-700">
                New Search
              </Button>
            </Link>
          </div>
        </div>
      </main>
    )
  }

  return (
    <main className="flex min-h-screen flex-col p-4 md:p-24">
      <div className="w-full max-w-6xl mx-auto space-y-8">
        <div className="flex items-center justify-between">
          <Link href="/">
            <Button variant="outline" className="border-gray-700 text-gray-300 hover:bg-gray-800">
              <ArrowLeft className="h-4 w-4 mr-2" />
              New Search
            </Button>
          </Link>
        </div>

        <div className="text-center space-y-4">
          <div className="flex items-center justify-center gap-2 mb-4">
            <Sparkles className="h-8 w-8 text-purple-500" />
            <h1 className="text-4xl font-bold text-white">Concert Results</h1>
          </div>
          <p className="text-xl text-gray-400">
            Based on your search: <span className="text-purple-400 font-medium">"{responseData.query}"</span>
          </p>
        </div>

        {responseData.error ? (
          <div className="text-center py-12">
            {responseData.errorType === 'quota_exceeded' ? (
              <>
                <div className="mb-6">
                  <div className="w-16 h-16 mx-auto mb-4 bg-yellow-500/20 rounded-full flex items-center justify-center">
                    <svg className="w-8 h-8 text-yellow-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                    </svg>
                  </div>
                </div>
                <h2 className="text-2xl font-bold text-yellow-500 mb-4">API Quota Limit Reached</h2>
                <p className="text-gray-400 mb-4 max-w-md mx-auto leading-relaxed">
                  We've reached our daily API request limit.
                </p>
                <p className="text-gray-500 text-sm mb-8">
                  Please try again later or contact support if you need immediate access.
                </p>
                <div className="space-y-4">
                  <Link href="/">
                    <Button className="bg-purple-600 hover:bg-purple-700">
                      Try Again Later
                    </Button>
                  </Link>
                  <div className="text-xs text-gray-600">
                    Tip: Try searching during off-peak hours for better availability
                  </div>
                </div>
              </>
            ) : responseData.errorType === 'server_error' ? (
              <>
                <div className="mb-6">
                  <div className="w-16 h-16 mx-auto mb-4 bg-red-500/20 rounded-full flex items-center justify-center">
                    <svg className="w-8 h-8 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                </div>
                <h2 className="text-2xl font-bold text-red-500 mb-4">Server Error</h2>
                <p className="text-gray-400 mb-8 max-w-md mx-auto">
                  There was a temporary server issue. Please try again in a few moments.
                </p>
                <Link href="/">
                  <Button className="bg-purple-600 hover:bg-purple-700">
                    Try Again
                  </Button>
                </Link>
              </>
            ) : (
              <>
                <h2 className="text-2xl font-bold text-white mb-4">Something went wrong</h2>
                <p className="text-gray-400 mb-8">
                  {responseData.response}
                </p>
                <Link href="/">
                  <Button className="bg-purple-600 hover:bg-purple-700">
                    Try Again
                  </Button>
                </Link>
              </>
            )}
          </div>
        ) : (
          <ConcertResults 
            query={responseData.query} 
            aiResponse={responseData.response} 
            sessionId={responseData.session_id} 
          />
        )}
      </div>
    </main>
  )
}
