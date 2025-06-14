import { useState, useRef, useCallback, useEffect } from 'react'
import { Message } from '../types/chat'
import { chatService } from '../services/chatService'
import { generateId } from '../utils/uuid'

const MAX_MESSAGE_LENGTH = 1000
const MAX_MESSAGES = 100

export const useChatbot = () => {
  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const abortControllerRef = useRef<AbortController | null>(null)

  const sendMessage = useCallback(async (content: string) => {
    // Input validation
    const trimmedContent = content.trim()
    if (!trimmedContent) {
      return
    }
    
    if (trimmedContent.length > MAX_MESSAGE_LENGTH) {
      const errorMessage: Message = {
        id: generateId(),
        role: 'assistant',
        content: `Message is too long. Please keep it under ${MAX_MESSAGE_LENGTH} characters.`,
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, errorMessage])
      return
    }

    // Cancel previous request if still pending
    if (abortControllerRef.current) {
      abortControllerRef.current.abort()
    }

    // Create new abort controller for this request
    abortControllerRef.current = new AbortController()
    const userMessage: Message = {
      id: generateId(),
      role: 'user',
      content: trimmedContent,
      timestamp: new Date(),
    }

    setMessages((prev) => {
      // Limit messages to prevent memory issues
      const newMessages = [...prev, userMessage]
      return newMessages.slice(-MAX_MESSAGES)
    })
    setIsLoading(true)

    try {
      const response = await chatService.sendMessage(trimmedContent, abortControllerRef.current.signal)
      
      // Check if request was aborted
      if (abortControllerRef.current.signal.aborted) {
        return
      }
      
      const botMessage: Message = {
        id: generateId(),
        role: 'assistant',
        content: response.response,
        timestamp: new Date(),
      }
      setMessages((prev) => {
        const newMessages = [...prev, botMessage]
        return newMessages.slice(-MAX_MESSAGES)
      })
    } catch (error) {
      // Don't show error for aborted requests
      if (error instanceof Error && error.name === 'AbortError') {
        return
      }
      
      // In production, this should send errors to a logging service
      // Example: errorLoggingService.logError('Error sending message', error)
      
      // Type-safe error handling
      let errorContent = 'Sorry, I encountered an error. Please try again.'
      
      if (error && typeof error === 'object' && 'response' in error) {
        const responseError = error as { response?: { status?: number } }
        if (responseError.response?.status === 429) {
          errorContent = 'Rate limit exceeded. Please wait a moment before sending another message.'
        } else if (responseError.response?.status === 413) {
          errorContent = 'Message is too large. Please shorten your message.'
        }
      }
      
      const errorMessage: Message = {
        id: generateId(),
        role: 'assistant',
        content: errorContent,
        timestamp: new Date(),
      }
      setMessages((prev) => {
        const newMessages = [...prev, errorMessage]
        return newMessages.slice(-MAX_MESSAGES)
      })
    } finally {
      setIsLoading(false)
      abortControllerRef.current = null
    }
  }, [])

  // Cleanup: abort pending requests on unmount
  useEffect(() => {
    return () => {
      if (abortControllerRef.current) {
        abortControllerRef.current.abort()
      }
    }
  }, [])

  return {
    messages,
    sendMessage,
    isLoading,
  }
}