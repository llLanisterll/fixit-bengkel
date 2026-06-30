import urllib.request
import urllib.error

BASE_URL = "http://localhost:8000/api"
endpoints = [
    "/users/",
    "/services/",
    "/mechanics/",
    "/spareparts/",
    "/vehicles/",
    "/bookings/",
    "/invoices/",
    "/service-logs/"
]

errors = []
for ep in endpoints:
    url = BASE_URL + ep
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            if response.status != 200:
                errors.append(f"{ep} -> {response.status}")
            else:
                print(f"{ep} OK")
    except urllib.error.HTTPError as e:
        errors.append(f"{ep} -> HTTP {e.code}: {e.read().decode('utf-8')}")
    except Exception as e:
        errors.append(f"{ep} -> Exception: {e}")

if errors:
    print("\nERRORS FOUND:")
    for e in errors:
        print(e)
else:
    print("\nALL ENDPOINTS OK")
