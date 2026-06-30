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
        licensePlate="TEST-999"
    )
    db_vehicle = crud.create_vehicle(db, vehicle_in)
    validated = schemas.Vehicle.model_validate(db_vehicle)
    print("OK", validated.id)
    crud.delete_vehicle(db, validated.id)
except Exception as e:
    import traceback
    traceback.print_exc()
finally:
    db.close()
