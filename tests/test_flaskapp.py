import app  # Import the Flask app from app.py
import json
import pytest

def test_power():
    # Create a test client using the Flask app's test client
    client = app.app.test_client()
    
    # Simulate a request to the power function
    response = client.get('/power/2/2')
    
    # Assert that the response JSON is correct
    assert response.status_code == 200
    assert json.loads(response.data) == {'result': 4}
