from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .auth import get_current_user
from . import schemas, models, crud, database

router = APIRouter(prefix="/pets", tags=["Pets"])

@router.get("/", response_model=list[schemas.PetResponse])
def get_adoptable_pets(db: Session = Depends(database.get_db)):
    """View all adoptable pets."""
    return crud.get_available_pets(db)

@router.post("/{pet_id}/adopt", response_model=schemas.AdoptionResponse)
def adopt_pet(pet_id: int, db: Session = Depends(database.get_db), user: models.User = Depends(get_current_user)):
    """Adopt a pet if available."""
    pet = crud.get_pet_by_id(db, pet_id)
    if not pet or not pet.is_available:
        raise HTTPException(status_code=404, detail="Pet not available for adoption")
    return crud.adopt_pet(db, user, pet)

@router.post("/{pet_id}/return", response_model=schemas.AdoptionResponse)
def return_pet(pet_id: int, db: Session = Depends(database.get_db), user: models.User = Depends(get_current_user)):
    """Return an adopted pet."""
    adoption = crud.get_adoption_record(db, user.id, pet_id)
    if not adoption:
        raise HTTPException(status_code=400, detail="You have not adopted this pet")
    return crud.return_pet(db, adoption)

@router.get("/history", response_model=list[schemas.AdoptionResponse])
def view_adoption_history(db: Session = Depends(database.get_db), user: models.User = Depends(get_current_user)):
    """View adoption history of the logged-in user."""
    return crud.get_user_adoption_history(db, user.id)