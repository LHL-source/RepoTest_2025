import pytest
from app import app

def test_get_secret(monkeypatch):
    # Mock the Key Vault client to return a test secret
    class MockSecretClient:
        def get_secret(self, secret_name):
            class MockSecret:
                value = "Mocked Secret"
            return MockSecret()
    
    # Replace the real client with the mock
    monkeypatch.setattr("app.client", MockSecretClient())

    # Create a test client for Flask
    client = app.test_client()
    response = client.get('/secret')

    # Assert that the response is correct
    assert response.status_code == 200
    assert response.json == {"message": "Mocked Secret"}
