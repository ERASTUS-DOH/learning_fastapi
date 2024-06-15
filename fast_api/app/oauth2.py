import datetime as dt
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from .config import settings
from .database import get_db
from .models import User
from .schema import TokenData, UserResponse
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# SECRET_KEY
# ALGORITHM
# EXPIRATION TIME

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict)-> str:
    to_encode = data.copy()

    expire = dt.datetime.now(dt.UTC) + dt.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verifiy_access_token(token: str, credentials_exception: Exception) -> str:
    try: 
        payload = jwt.decode(token=token, key= SECRET_KEY, algorithms=[ALGORITHM])
        id: int = int(payload.get("user_id"))
        if id is None:
            raise credentials_exception
        
        token_data = TokenData(id = id)

    except JWTError as e:
        raise credentials_exception

    return token_data
    

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> UserResponse:
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail=f"Could not validate credentails", 
        headers={"WWW-Authenticate" : "Bearer"}
    )

    token_id = verifiy_access_token(token=token, credentials_exception= credentials_exception)

    current_user = db.query(User).filter(User.id == token_id.id).first()
    
    return current_user