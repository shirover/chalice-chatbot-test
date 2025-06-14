import axios from 'axios'
import { ChatResponse } from '../types/chat'

const API_BASE_URL = '/api/v1'

class ChatService {
  async sendMessage(message: string, signal?: AbortSignal): Promise<ChatResponse> {
    const response = await axios.post<ChatResponse>(
      `${API_BASE_URL}/chat/`,
      {
        message,
      },
      {
        signal,
        timeout: 30000, // 30 second timeout
      }
    )
    return response.data
  }
}

export const chatService = new ChatService()