import pytest
from fastapi.testclient import TestClient
from app.main import app, limiter
import time

# 干渉を避けるため各テスト用に新しいクライアントを作成
@pytest.fixture
def test_client():
    # テスト間でレート制限ストレージをクリア
    if hasattr(limiter, '_storage'):
        limiter._storage.clear()
    return TestClient(app)

def test_rate_limit_enforcement(test_client):
    """制限を超えた後にレート制限が適用されることをテスト"""
    # 設定からレート制限を取得（デフォルトは60/分）
    # テストのために、多くのリクエストを素早く送信
    
    # 制限までリクエストを送信
    responses = []
    for i in range(61):  # 60/分の制限を超えようとする
        response = test_client.post(
            "/api/v1/chat/",
            json={"message": f"Test message {i}"}
        )
        responses.append(response)
        
        # レート制限に達したら停止
        if response.status_code == 429:
            break
    
    # 最終的にレート制限に達したことを確認
    rate_limited = any(r.status_code == 429 for r in responses)
    assert rate_limited, "レート制限が適用されていません"
    
    # レート制限されたレスポンスには適切なエラーメッセージが含まれるべき
    rate_limited_response = next(r for r in responses if r.status_code == 429)
    assert "rate limit" in rate_limited_response.json()["detail"].lower()

def test_rate_limit_headers(test_client):
    """レート制限ヘッダーがレスポンスに含まれることをテスト"""
    response = test_client.post(
        "/api/v1/chat/",
        json={"message": "Test message"}
    )
    
    # レート制限ヘッダーを確認
    assert "X-RateLimit-Limit" in response.headers
    assert "X-RateLimit-Remaining" in response.headers
    assert "X-RateLimit-Reset" in response.headers

def test_rate_limit_per_ip():
    """レート制限がIPアドレスごとであることをテスト"""
    # レート制限が適切に設定されていることを確認
    from app.main import limiter
    assert limiter is not None
    assert limiter._key_func.__name__ == 'get_remote_address'