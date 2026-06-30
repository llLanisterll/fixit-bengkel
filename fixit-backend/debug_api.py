from database import SessionLocal
import crud
import schemas
db = SessionLocal()
try:
    users = crud.get_users(db)
    # try to dump using pydantic
    for u in users:
        schemas.User.model_validate(u)
    print("Serialization OK")
except Exception as e:
    import traceback
    traceback.print_exc()
finally:
    db.close()
