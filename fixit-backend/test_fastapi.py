from fastapi.testclient import TestClient
from main import app
client = TestClient(app)
response = client.get("/api/users/")
print(response.status_code)
print(response.json())
