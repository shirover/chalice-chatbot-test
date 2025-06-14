/**
 * UUID v4を生成
 * 利用可能な場合はcrypto.randomUUIDを使用し、手動実装にフォールバック
 */
export function generateUUID(): string {
  // 利用可能な場合はネイティブcrypto APIを使用（より安全）
  if (typeof crypto !== 'undefined' && crypto.randomUUID) {
    return crypto.randomUUID()
  }
  
  // フォールバック実装
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = Math.random() * 16 | 0
    const v = c === 'x' ? r : (r & 0x3 | 0x8)
    return v.toString(16)
  })
}

/**
 * タイムスタンプと乱数に基づいて単純な一意のIDを生成
 * これはUUIDより高速ですが、依然として良好な一意性を提供します
 */
export function generateId(): string {
  return `${Date.now()}-${Math.random().toString(36).substring(2, 11)}`
}