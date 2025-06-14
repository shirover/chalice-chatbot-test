import React from 'react'
import ChatContainer from './components/ChatContainer'
import ErrorBoundary from './components/ErrorBoundary'
import './styles/App.css'

function App(): JSX.Element {
  return (
    <ErrorBoundary>
      <div className="app">
        <header className="app-header">
          <h1>Chatbot</h1>
        </header>
        <main className="app-main">
          <ChatContainer />
        </main>
      </div>
    </ErrorBoundary>
  )
}

export default App