from database import SessionLocal
import crud
db = SessionLocal()
try:
    users = crud.get_users(db)
    print("Users count:", len(users))
except Exception as e:
    import traceback
    traceback.print_exc()
finally:
    db.close()
