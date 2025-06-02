from pydantic import BaseModel, EmailStr, Field

MOBILE_REGEX = r"^\+?[1-9]\d{1,14}$"  # E.164

class UserBaseSchema(BaseModel):
    first_name: str
    last_name: str
    mobile_number: str = Field(..., pattern=MOBILE_REGEX)
    email: EmailStr

class UserCreateSchema(UserBaseSchema):
    password: str
    class Config:
        orm_mode = True

class UserLoginSchema(BaseModel):
    username: str = Field(..., description="username")
    password: str
from pydantic import BaseModel

class UserWelcomeSchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    message: str

    class Config:
        orm_mode = True

class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
