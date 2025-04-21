import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.database import SessionLocal
from app.models import User

load_dotenv()

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")  # Default fallback

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_admin():
    db: Session = SessionLocal()
    admin = db.query(User).filter(User.username == ADMIN_USERNAME).first()
    
    if not admin:
        hashed_password = pwd_context.hash(ADMIN_PASSWORD)  # Change to a secure password
        admin_user = User(username=ADMIN_USERNAME, email="admin@example.com",hashed_password=hashed_password, is_admin=True)
        db.add(admin_user)
        db.commit()
        # print("Admin user created successfully!")
    # else:
        # print("Admin user already exists.")
    db.close()

# Call this function at application startup
# create_admin()