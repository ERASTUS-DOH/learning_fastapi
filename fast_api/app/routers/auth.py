from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..models import User
from ..database import get_db
from ..schema import UserLogin, Token
from ..utils import verify
from ..oauth2 import create_access_token

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=Token)
def login(login_details: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # The injected login details is a dictionary containing the fields username and password.
    queried_user = db.query(User).filter(User.email == login_details.username).first()

    if not queried_user: # User does not exist.
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    # verify user passwords.
    if not verify(plain_password=login_details.password, hashed_password=queried_user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    

    # create token
    access_token = create_access_token(data= {"user_id" : queried_user.id})


    return {
        "access_token" : access_token, "token_type" : "bearer"
    }
