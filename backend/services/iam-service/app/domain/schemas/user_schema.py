from pydantic import BaseModel, EmailStr, Field
from typing import Optional


MOBILE_REGEX = r"^\+?[1-9]\d{1,14}$"  # E.164

class UserBaseSchema(BaseModel):
    first_name: str
    last_name: str
    mobile_number: str = Field(..., pattern=MOBILE_REGEX)
    email: EmailStr
    # role: str

class UserCreateSchema(UserBaseSchema):
    password: str
    # role: Optional[str] = "user"
    class Config:
        orm_mode = True




class UserLoginSchema(BaseModel):
    username: str = Field(..., description="username")
    password: str

class UserWelcomeSchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    message: str

    class Config:
        orm_mode = True


