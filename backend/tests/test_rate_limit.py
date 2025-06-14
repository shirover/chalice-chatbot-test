import pytest
from fastapi.testclient import TestClient
from app.main import app
import time

client = TestClient(app)

def test_rate_limit_enforcement():
    """Test that rate limiting is enforced after exceeding the limit"""
    # Get the rate limit from settings (default is 60/minute)
    # For testing, we'll send many requests quickly
    
    # Send requests up to the limit
    responses = []
    for i in range(61):  # Try to exceed the 60/minute limit
        response = client.post(
            "/api/v1/chat/",
            json={"message": f"Test message {i}"}
        )
        responses.append(response)
        
        # Stop if we hit rate limit
        if response.status_code == 429:
            break
    
    # Check that we eventually hit the rate limit
    rate_limited = any(r.status_code == 429 for r in responses)
    assert rate_limited, "Rate limit was not enforced"
    
    # The rate limited response should have appropriate error message
    rate_limited_response = next(r for r in responses if r.status_code == 429)
    assert "rate limit" in rate_limited_response.json()["detail"].lower()

def test_rate_limit_headers():
    """Test that rate limit headers are included in responses"""
    response = client.post(
        "/api/v1/chat/",
        json={"message": "Test message"}
    )
    
    # Check for rate limit headers
    assert "X-RateLimit-Limit" in response.headers
    assert "X-RateLimit-Remaining" in response.headers
    assert "X-RateLimit-Reset" in response.headers

def test_rate_limit_per_ip():
    """Test that rate limiting is per IP address"""
    # This test would require mocking different IP addresses
    # For now, we'll just verify the rate limiter is configured
    from app.api.endpoints.chat import limiter
    assert limiter is not None
    assert limiter._key_func.__name__ == 'get_remote_address'