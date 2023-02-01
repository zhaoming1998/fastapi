from pydantic import BaseModel, EmailStr,conint
from datetime import datetime
from typing import Optional

# post schema
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class CreatePost(PostBase):
    pass

class Post(PostBase):
    id: int
    owner_id: int
    owner: UserOut
    class Config:
        orm_mode=True

class PostOut(BaseModel):
    Post:Post
    votes:int
    class Config:
        orm_mode=True

class CreateUser(BaseModel):
    email:EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1,ge=0)
