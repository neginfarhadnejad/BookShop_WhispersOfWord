from pydantic import BaseModel, EmailStr ,validator
import re

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

    @validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[0-9]", value):
            raise ValueError("Password must contain at least one number")
        if not re.search(r"[!@#$%^&*()_+{}\[\]:;\"'<>,.?/~`\\|-]", value):
            raise ValueError("Password must contain at least one special character (!@#$%^&...)")
        return value