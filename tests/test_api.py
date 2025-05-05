import requests

def test_api_root():
    response = requests.get("http://localhost:8000/")
    assert response.status_code == 200
    assert "message" in response.json()
