import React from 'react'
import ChatContainer from './components/ChatContainer'
import './styles/App.css'

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1>Chatbot</h1>
      </header>
      <main className="app-main">
        <ChatContainer />
      </main>
    </div>
  )
}

export default App