import crud, schemas
from database import SessionLocal
db = SessionLocal()
try:
    user = db.query(crud.models.User).filter(crud.models.User.email != "admin@fixit.com").first()
    if user:
        print("Found user:", user.id)
        db_user = crud.delete_user(db, user.id)
        schemas.User.model_validate(db_user)
        print("OK", db_user.id)
    else:
        print("No user found")
except Exception as e:
    import traceback
    traceback.print_exc()
finally:
    db.close()
