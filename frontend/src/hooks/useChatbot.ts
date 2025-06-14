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
    // 入力検証
    const trimmedContent = content.trim()
    if (!trimmedContent) {
      return
    }
    
    if (trimmedContent.length > MAX_MESSAGE_LENGTH) {
      const errorMessage: Message = {
        id: generateId(),
        role: 'assistant',
        content: `メッセージが長すぎます。${MAX_MESSAGE_LENGTH}文字以内にしてください。`,
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, errorMessage])
      return
    }

    // まだ保留中の場合は前のリクエストをキャンセル
    if (abortControllerRef.current) {
      abortControllerRef.current.abort()
    }

    // このリクエスト用の新しいアボートコントローラーを作成
    abortControllerRef.current = new AbortController()
    const userMessage: Message = {
      id: generateId(),
      role: 'user',
      content: trimmedContent,
      timestamp: new Date(),
    }

    setMessages((prev) => {
      // メモリの問題を防ぐためにメッセージを制限
      const newMessages = [...prev, userMessage]
      return newMessages.slice(-MAX_MESSAGES)
    })
    setIsLoading(true)

    try {
      const response = await chatService.sendMessage(trimmedContent, abortControllerRef.current.signal)
      
      // リクエストが中止されたかチェック
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
      // 中止されたリクエストのエラーは表示しない
      if (error instanceof Error && error.name === 'AbortError') {
        return
      }
      
      // プロダクション環境では、これはエラーをログサービスに送信する必要があります
      // 例: errorLoggingService.logError('Error sending message', error)
      
      // 型安全なエラーハンドリング
      let errorContent = '申し訳ありません、エラーが発生しました。もう一度お試しください。'
      
      if (error && typeof error === 'object' && 'response' in error) {
        const responseError = error as { response?: { status?: number } }
        if (responseError.response?.status === 429) {
          errorContent = 'レート制限を超えました。しばらく待ってから次のメッセージを送信してください。'
        } else if (responseError.response?.status === 413) {
          errorContent = 'メッセージが大きすぎます。メッセージを短くしてください。'
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

  // クリーンアップ：アンマウント時に保留中のリクエストを中止
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