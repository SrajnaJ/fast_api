from fastapi import FastAPI
from .database import Base, engine
from .auth import router as auth_router
from .admin_routes import router as admin_router
from .user_routes import router as user_router
from app.admin import create_admin

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(user_router)

create_admin()

@app.get("/")
def home():
    return {"message": "Welcome to Pet Adoption System"}