import axios from 'axios'
import { ChatResponse } from '../types/chat'

const API_BASE_URL = '/api/v1'
const REQUEST_TIMEOUT_MS = 30000 // 30秒

class ChatService {
  async sendMessage(message: string, signal?: AbortSignal): Promise<ChatResponse> {
    const response = await axios.post<ChatResponse>(
      `${API_BASE_URL}/chat/`,
      {
        message,
      },
      {
        signal,
        timeout: REQUEST_TIMEOUT_MS,
      }
    )
    return response.data
  }
}

export const chatService = new ChatService()