import React, { Component, ErrorInfo, ReactNode } from 'react'
import '../styles/ErrorBoundary.css'

interface Props {
  children: ReactNode
}

interface State {
  hasError: boolean
  error: Error | null
}

class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null
  }

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // In production, this should send errors to a logging service
    // Example: errorLoggingService.logError(error, errorInfo)
  }

  private handleReload = () => {
    window.location.reload()
  }

  public render() {
    if (this.state.hasError) {
      return (
        <div className="error-boundary">
          <h2>Something went wrong</h2>
          <p>Please refresh the page and try again.</p>
          <button 
            onClick={this.handleReload}
            className="error-boundary-button"
          >
            Reload Page
          </button>
          {/* Only show error details in development */}
          {process.env.NODE_ENV === 'development' && this.state.error && (
            <details className="error-details">
              <summary>Error details (development only)</summary>
              <pre>
                {this.state.error.toString()}
              </pre>
            </details>
          )}
        </div>
      )
    }

    return this.props.children
  }
}

export default ErrorBoundary