import datetime as dt
from jose import JWTError, jwt

from .schema import TokenData
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# SECRET_KEY
# ALGORITHM
# EXPIRATION TIME

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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
    

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail=f"Could not validate credentails", 
        headers={"WWW-Authenticate" : "Bearer"}
    )

    return verifiy_access_token(token=token, credentials_exception= credentials_exception)