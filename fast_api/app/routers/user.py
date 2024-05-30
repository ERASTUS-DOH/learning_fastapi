from fastapi import status, HTTPException, Depends, APIRouter
from ..schema import UserCreate, UserResponse
from sqlalchemy.orm import Session

from ..utils import hash_pwd

from ..database import get_db

from .. models import User

router = APIRouter()

@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    
    # hashing user password.
    user.password = hash_pwd(user.password)

    new_user = User(**dict(user)) #unpacking the user details into the pydantic model.
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/users/{id}", response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    queried_user = db.query(User).filter(User.id == id).first()

    if not queried_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")

    return queried_user