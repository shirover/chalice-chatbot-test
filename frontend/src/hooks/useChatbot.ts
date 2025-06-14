import { useState, useRef, useCallback } from 'react'
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
    } catch (error: any) {
      // Don't show error for aborted requests
      if (error.name === 'AbortError') {
        return
      }
      
      console.error('Error sending message:', error)
      const errorMessage: Message = {
        id: generateId(),
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
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

  return {
    messages,
    sendMessage,
    isLoading,
  }
}