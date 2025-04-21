from sqlalchemy.orm import Session
from . import models, schemas

def create_user(db: Session, user: schemas.UserCreate, hashed_password: str):
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db:Session, user_id:int, update_data:schemas.UserUpdate):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return None

    if update_data.username:
        user.username = update_data.username
    if update_data.email:
        user.email = update_data.email
    if update_data.password:
        user.hashed_password = update_data.password

    db.commit()
    db.refresh(user)
    return user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


# Admin functions:
def get_all_pets(db: Session):
    """Fetch all pets (admin only)"""
    return db.query(models.Pet).all()

def get_all_adoptions(db: Session):
    """Fetch all adoptions (admin only)"""
    return db.query(models.Adoption).all()

def create_pet(db: Session, pet: schemas.PetCreate):
    db_pet = models.Pet(**pet.dict())
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    return db_pet

def get_pet_by_id(db: Session, pet_id: int):
    return db.query(models.Pet).filter(models.Pet.id == pet_id).first()

def update_pet(db: Session, pet: models.Pet, pet_update: schemas.PetUpdate):
    for field, value in pet_update.dict(exclude_unset=True).items():
        setattr(pet, field, value)
    db.commit()
    db.refresh(pet)
    return pet

def delete_pet(db:Session,pet_id:int):
    pet=get_pet_by_id(db,pet_id)
    if not pet:
        return None
    
    db.delete(pet)
    db.commit()
    return pet


# User end points
"""Fetch all pets that are available for adoption"""
def get_available_pets(db: Session):
    return db.query(models.Pet).filter(models.Pet.adopted == False).all()

""" to adopt a pet"""
def adopt_pet(db:Session,user:models.User,pet:models.Pet):
    pet.adopted=True
    db.add(pet)

    adoption=models.Adoption(user_id=user.id,pet_id=pet.id)
    db.add(adoption)

    db.commit()
    db.refresh(adoption)

    return adoption

""" get an adoption record """
def get_adoption_record(db: Session, user_id: int, pet_id: int):
    return db.query(models.Adoption).filter(
        models.Adoption.user_id == user_id,
        models.Adoption.pet_id == pet_id
    ).first()


def return_pet(db:Session,adoption:models.Adoption):
    """Remove adoption record and mark pet as available"""
    pet = adoption.pet
    pet.adopted = False
    db.add(pet)

    db.delete(adoption)

    db.commit()
    db.refresh(pet)

    return adoption

def get_user_adoption_history(db:Session,user_id:int):
    return db.query(models.Adoption).filter(
        models.Adoption.user_id == user_id
    ).all()