from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from . import schemas, models, crud, database
from .auth import get_current_admin_user

router = APIRouter(prefix="/admin", tags=["Admin"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
security=HTTPBearer()

@router.post("/add_pet", response_model=schemas.PetResponse)
def add_pet(pet: schemas.PetCreate, db: Session = Depends(database.get_db), admin_user: models.User = Depends(get_current_admin_user)
):
    return crud.create_pet(db, pet)
    # if not user.is_admin:
    #     raise HTTPException(status_code=403, detail="Not authorized")


@router.put("/pets/update/{pet_id}", response_model=schemas.PetResponse)
def update_pet(pet_id: int, pet_update: schemas.PetUpdate, db: Session = Depends(database.get_db), admin_user: models.User = Depends(get_current_admin_user)):
    pet = crud.get_pet_by_id(db, pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return crud.update_pet(db, pet, pet_update)


@router.delete("/pets/delete/{pet_id}", response_model=dict)
def remove_pet(pet_id: int, db: Session = Depends(database.get_db), admin_user: models.User = Depends(get_current_admin_user)):
    pet = crud.delete_pet(db, pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return {"detail": f"Pet '{pet.name}' deleted successfully"}


@router.get("/pets", response_model=list[schemas.PetResponse])
def view_all_pets(db: Session = Depends(database.get_db), admin_user: models.User = Depends(get_current_admin_user)):
    return crud.get_all_pets(db)

@router.get("/adoptions", response_model=list[schemas.AdoptionResponse])
def view_all_adoptions(db: Session = Depends(database.get_db), admin_user: models.User = Depends(get_current_admin_user)):
    return crud.get_all_adoptions(db)