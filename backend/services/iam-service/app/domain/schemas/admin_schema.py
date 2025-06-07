from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class AdminBaseSchema(BaseModel):
    name: str
    email: EmailStr
    phone_number: str
    date_of_birth: Optional[str]
    role: Optional[str] = "admin"
  
    class Config:
        orm_mode = True
class AdminCreateSchema(AdminBaseSchema):
    password: str  

    class Config:
        orm_mode = True

        exclude = {"id", "created_at", "updated_at", "is_verified", "role"}
class AdminLoginSchema(BaseModel):
    username: str 
    password: str

    class Config:
        orm_mode = True
class AdminResponseSchema(AdminBaseSchema):
    
    pass


class AdminWelcomeSchema(BaseModel):
    name: str
    email: EmailStr
    phone_number: str
    message: str
    role: Optional[str] = "admin"

    class Config:
        orm_mode = True

class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
