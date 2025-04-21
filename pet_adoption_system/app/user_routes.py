from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from .auth import get_current_user
from . import schemas, models, crud, database

router = APIRouter(prefix="/pets", tags=["Pets"])

@router.get("/", response_model=list[schemas.PetResponse])
def get_adoptable_pets(db: Session = Depends(database.get_db)):

    """View all adoptable pets."""
    return crud.get_available_pets(db)


@router.post("/{pet_id}/adopt")
def adopt_pet(pet_id: int, db: Session = Depends(database.get_db), user: models.User = Depends(get_current_user)):
    """Adopt a pet if available."""
    pet = crud.get_pet_by_id(db, pet_id)
    if not pet or pet.adopted:
        raise HTTPException(status_code=404, detail="Pet not available for adoption")
    adoption=crud.adopt_pet(db, user, pet)
    return JSONResponse(
        status_code=200,
        content={
            "message": "Pet adopted successfully",
            "adoption": {
                "id": adoption.id,
                "pet_id": adoption.pet_id,
                "user_id": adoption.user_id
            }
        }
    )

@router.post("/{pet_id}/return")
def return_pet(pet_id: int, db: Session = Depends(database.get_db), user: models.User = Depends(get_current_user)):
    
    """Return an adopted pet."""
    adoption = crud.get_adoption_record(db, user.id, pet_id)
    if not adoption:
        raise HTTPException(status_code=400, detail="You have not adopted this pet")
    adoption=crud.return_pet(db, adoption)
    return JSONResponse(
        status_code=200,
        content={
            "message": "Pet returned successfully",
            "adoption": {
                "id": adoption.id,
                "pet_id": adoption.pet_id,
                "user_id": adoption.user_id
            }
        }
    )

@router.get("/history", response_model=list[schemas.AdoptionResponse])
def view_adoption_history(db: Session = Depends(database.get_db), user: models.User = Depends(get_current_user)):
    """View adoption history of the logged-in user."""
    return crud.get_user_adoption_history(db, user.id)