import requests
res = requests.post("http://localhost:8000/api/service-logs", json={
    "bookingId": 1,
    "mechanicId": 1,
    "description": "Test",
    "sparepartQty": 1,
    "status": "DONE"
})
print(res.status_code)
print(res.text)
