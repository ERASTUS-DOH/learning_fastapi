import datetime as _dt
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass
 
class PostResponse(PostBase):
    id: int
    created_at: _dt.datetime
    owner_id: int
    owner_details: UserResponse

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int]




# class CreatePost(BaseModel):
#     title: str
#     content: str
#     published: bool = True

# class UpdatePost(BaseModel):
#     title: str
#     content: str
#     published: bool