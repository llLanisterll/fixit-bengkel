import crud, schemas
from database import SessionLocal
db = SessionLocal()
try:
    user = db.query(crud.models.User).first()
    vehicle_in = schemas.VehicleCreate(
        userId=user.id,
        brand="Test",
        model="Test",
        year=2024,
        licensePlate="TEST-DUP"
    )
    crud.create_vehicle(db, vehicle_in)
    crud.create_vehicle(db, vehicle_in) # Duplicate!
except Exception as e:
    import traceback
    traceback.print_exc()
finally:
    db.close()
