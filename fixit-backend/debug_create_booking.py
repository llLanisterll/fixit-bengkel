import crud, schemas
from database import SessionLocal
from datetime import datetime

db = SessionLocal()
try:
    user = db.query(crud.models.User).filter(crud.models.User.email != "admin@fixit.com").first()
    vehicle = db.query(crud.models.Vehicle).filter(crud.models.Vehicle.userId == user.id).first()
    service = db.query(crud.models.Service).first()
    
    print("User:", user.id, "Vehicle:", vehicle.id, "Service:", service.id)
    
    booking_in = schemas.BookingCreate(
        userId=user.id,
        vehicleId=vehicle.id,
        bookingDate=datetime.now(),
        timeSlot="09:00",
        serviceIds=[service.id]
    )
    
    db_booking = crud.create_booking(db, booking_in)
    validated = schemas.Booking.model_validate(db_booking)
    print("OK Booking ID:", validated.id)
    
    crud.delete_booking(db, validated.id)
except Exception as e:
    import traceback
    traceback.print_exc()
finally:
    db.close()
