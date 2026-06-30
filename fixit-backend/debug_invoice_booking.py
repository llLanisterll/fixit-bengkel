import crud, schemas
from database import SessionLocal
db = SessionLocal()
try:
    invoices = crud.get_invoices(db)
    for inv in invoices:
        validated = schemas.Invoice.model_validate(inv)
        print("OK", validated.id)
        if validated.booking:
            print("  Booking:", validated.booking.bookingCode)
            if validated.booking.vehicle:
                print("  Vehicle:", validated.booking.vehicle.brand)
            if validated.booking.user:
                print("  User:", validated.booking.user.name)
except Exception as e:
    import traceback
    traceback.print_exc()
finally:
    db.close()
