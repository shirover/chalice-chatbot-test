import { renderHook, act, waitFor } from '@testing-library/react'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { useChatbot } from './useChatbot'
import { chatService } from '../services/chatService'

// チャットサービスをモック
vi.mock('../services/chatService', () => ({
  chatService: {
    sendMessage: vi.fn()
  }
}))

describe('useChatbot', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('should initialize with empty messages', () => {
    const { result } = renderHook(() => useChatbot())
    expect(result.current.messages).toEqual([])
    expect(result.current.isLoading).toBe(false)
  })

  it('should send a message successfully', async () => {
    const mockResponse = { response: 'Hello from chatbot!' }
    vi.mocked(chatService.sendMessage).mockResolvedValueOnce(mockResponse)

    const { result } = renderHook(() => useChatbot())

    await act(async () => {
      await result.current.sendMessage('Hello!')
    })

    await waitFor(() => {
      expect(result.current.messages).toHaveLength(2)
      expect(result.current.messages[0].role).toBe('user')
      expect(result.current.messages[0].content).toBe('Hello!')
      expect(result.current.messages[1].role).toBe('assistant')
      expect(result.current.messages[1].content).toBe('Hello from chatbot!')
    })
  })

  it('should handle empty message', async () => {
    const { result } = renderHook(() => useChatbot())

    await act(async () => {
      await result.current.sendMessage('   ')
    })

    expect(result.current.messages).toHaveLength(0)
    expect(chatService.sendMessage).not.toHaveBeenCalled()
  })

  it('should handle long messages', async () => {
    const { result } = renderHook(() => useChatbot())
    const longMessage = 'a'.repeat(1001)

    await act(async () => {
      await result.current.sendMessage(longMessage)
    })

    expect(result.current.messages).toHaveLength(1)
    expect(result.current.messages[0].role).toBe('assistant')
    expect(result.current.messages[0].content).toContain('too long')
    expect(chatService.sendMessage).not.toHaveBeenCalled()
  })

  it('should handle errors', async () => {
    vi.mocked(chatService.sendMessage).mockRejectedValueOnce(new Error('Network error'))

    const { result } = renderHook(() => useChatbot())

    await act(async () => {
      await result.current.sendMessage('Hello!')
    })

    await waitFor(() => {
      expect(result.current.messages).toHaveLength(2)
      expect(result.current.messages[1].role).toBe('assistant')
      expect(result.current.messages[1].content).toContain('error')
    })
  })
})