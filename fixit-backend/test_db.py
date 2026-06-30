from database import SessionLocal
import crud
import schemas
db = SessionLocal()
try:
    v = crud.create_vehicle(db, schemas.VehicleCreate(userId=1, brand="Honda", model="Beat", year=2021, licensePlate="A123BC", color="Black"))
    print(v.id)
except Exception as e:
    print(e)
finally:
    db.close()
