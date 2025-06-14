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
    // プロダクション環境では、これはエラーをログサービスに送信する必要があります
    // 例: errorLoggingService.logError(error, errorInfo)
  }

  private handleReload = () => {
    window.location.reload()
  }

  public render() {
    if (this.state.hasError) {
      return (
        <div className="error-boundary">
          <h2>問題が発生しました</h2>
          <p>ページを更新してもう一度お試しください。</p>
          <button 
            onClick={this.handleReload}
            className="error-boundary-button"
          >
            ページを再読み込み
          </button>
          {/* 開発環境でのみエラー詳細を表示 */}
          {process.env.NODE_ENV === 'development' && this.state.error && (
            <details className="error-details">
              <summary>エラー詳細（開発環境のみ）</summary>
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