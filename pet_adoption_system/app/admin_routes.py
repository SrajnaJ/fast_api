from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import schemas, models, crud, database
from .auth import get_current_user

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post("/pets", response_model=schemas.PetResponse)
def add_pet(pet: schemas.PetCreate, db: Session = Depends(database.get_db), user: models.User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    return crud.create_pet(db, pet)

@router.put("/pets/{pet_id}", response_model=schemas.PetResponse)
def update_pet(pet_id: int, pet_update: schemas.PetUpdate, db: Session = Depends(database.get_db), user: models.User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    pet = crud.get_pet_by_id(db, pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return crud.update_pet(db, pet, pet_update)

@router.delete("/pets/{pet_id}", response_model=dict)
def remove_pet(pet_id: int, db: Session = Depends(database.get_db), user: models.User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    pet = crud.get_pet_by_id(db, pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    crud.delete_pet(db, pet)
    return {"detail": "Pet deleted successfully"}

@router.get("/pets", response_model=list[schemas.PetResponse])
def view_all_pets(db: Session = Depends(database.get_db), user: models.User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    return crud.get_all_pets(db)

@router.get("/adoptions", response_model=list[schemas.AdoptionResponse])
def view_all_adoptions(db: Session = Depends(database.get_db), user: models.User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    return crud.get_all_adoptions(db)