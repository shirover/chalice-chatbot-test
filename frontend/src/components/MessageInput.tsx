import React, { useState, FormEvent, memo } from 'react'
import '../styles/MessageInput.css'

interface MessageInputProps {
  onSendMessage: (message: string) => void
  isLoading: boolean
}

const MessageInput: React.FC<MessageInputProps> = ({ onSendMessage, isLoading }) => {
  const [message, setMessage] = useState('')

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault()
    if (message.trim() && !isLoading) {
      onSendMessage(message)
      setMessage('')
    }
  }

  return (
    <form className="message-input-form" onSubmit={handleSubmit}>
      <input
        type="text"
        className="message-input"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="メッセージを入力..."
        disabled={isLoading}
        aria-label="Message input"
        maxLength={1000}
      />
      <button 
        type="submit" 
        className="send-button" 
        disabled={isLoading || !message.trim()}
        aria-label="Send message"
      >
        {isLoading ? '送信中...' : '送信'}
      </button>
    </form>
  )
}

// 不要な再レンダリングを防ぐためにメモ化
export default memo(MessageInput)