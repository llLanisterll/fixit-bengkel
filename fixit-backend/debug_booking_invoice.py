import crud, schemas
from database import SessionLocal
db = SessionLocal()
try:
    bookings = crud.get_bookings(db)
    for b in bookings:
        schemas.Booking.model_validate(b)
    print("OK")
except Exception as e:
    import traceback
    traceback.print_exc()
finally:
    db.close()
