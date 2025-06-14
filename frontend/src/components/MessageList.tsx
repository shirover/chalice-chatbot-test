import React, { useEffect, useRef, memo } from 'react'
import { Message } from '../types/chat'
import '../styles/MessageList.css'

interface MessageListProps {
  messages: Message[]
}

const MessageList: React.FC<MessageListProps> = memo(({ messages }) => {
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  return (
    <div className="message-list" role="log" aria-live="polite" aria-label="Chat messages">
      {messages.map((message) => (
        <div
          key={message.id}
          className={`message ${message.role === 'user' ? 'user-message' : 'bot-message'}`}
          role="article"
          aria-label={`${message.role === 'user' ? 'User' : 'Assistant'} message`}
        >
          <div className="message-content">{message.content}</div>
          <div className="message-timestamp">
            {new Date(message.timestamp).toLocaleTimeString()}
          </div>
        </div>
      ))}
      <div ref={messagesEndRef} />
    </div>
  )
})

export default MessageList