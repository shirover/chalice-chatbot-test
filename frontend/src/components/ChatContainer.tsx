import React from 'react'
import MessageList from './MessageList'
import MessageInput from './MessageInput'
import { useChatbot } from '../hooks/useChatbot'
import '../styles/ChatContainer.css'

const ChatContainer: React.FC = () => {
  const { messages, sendMessage, isLoading } = useChatbot()

  return (
    <div className="chat-container">
      <MessageList messages={messages} />
      <MessageInput onSendMessage={sendMessage} isLoading={isLoading} />
    </div>
  )
}

export default React.memo(ChatContainer)