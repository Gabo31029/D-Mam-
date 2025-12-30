
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from database import SessionLocal, engine, Base
    from models import User
    from crud import get_user_by_username
    import sqlalchemy
    
    print("Imports successful.")
    
    # Try connecting
    with engine.connect() as connection:
        print("Database connection successful.")
        
    db = SessionLocal()
    print("Session created.")
    
    # Try querying
    user = get_user_by_username(db, "test_user_debug")
    print(f"Query successful. User found: {user}")
    
    db.close()
    print("Test finished successfully.")

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
