import crud, schemas
from database import SessionLocal
db = SessionLocal()
try:
    booking = db.query(crud.models.Booking).first()
    if booking:
        inv = crud.create_invoice(db, schemas.InvoiceCreate(bookingId=booking.id))
        schemas.Invoice.model_validate(inv)
        print("OK", inv.id)
    else:
        print("No booking found")
except Exception as e:
    import traceback
    traceback.print_exc()
finally:
    db.close()
