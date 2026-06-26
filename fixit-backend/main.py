from fastapi import FastAPI
from database import engine
import models
from routers import services, mechanics, spareparts, vehicles, bookings, service_logs, invoices, auth

# Create tables if they don't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FixIt API",
    description="REST API backend for FixIt Auto Service Workshop",
    version="1.0.0"
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(services.router, prefix="/api/services", tags=["Services"])
app.include_router(mechanics.router, prefix="/api/mechanics", tags=["Mechanics"])
app.include_router(spareparts.router, prefix="/api/spareparts", tags=["Spareparts"])
app.include_router(vehicles.router, prefix="/api/vehicles", tags=["Vehicles"])
app.include_router(bookings.router, prefix="/api/bookings", tags=["Bookings"])
app.include_router(service_logs.router, prefix="/api/service-logs", tags=["Service Logs"])
app.include_router(invoices.router, prefix="/api/invoices", tags=["Invoices"])

@app.get("/")
def root():
    return {"message": "Welcome to FixIt API. Go to /docs for Swagger UI documentation."}
