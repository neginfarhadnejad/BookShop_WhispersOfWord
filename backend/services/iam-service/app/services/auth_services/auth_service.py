from datetime import datetime, timedelta
from jose import jwt
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.domain.schemas.user_schema import UserCreateSchema, UserLoginSchema
from app.services.user_service import UserService
from app.services.auth_services.hash_service import HashService
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

class AuthService:
    def __init__(self, hash_service: HashService, user_service: UserService):
        self.hash_service = hash_service
        self.user_service = user_service

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def register_user(self, user_create: UserCreateSchema):
        existing_user = self.user_service.get_by_email_or_mobile(
            user_create.email, user_create.mobile_number
        )
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email or mobile number already registered",
            )
        hashed_password = self.hash_service.hash_password(user_create.password)
        created_user = self.user_service.create_user(
            first_name=user_create.first_name,
            last_name=user_create.last_name,
            email=user_create.email,
            mobile_number=user_create.mobile_number,
            hashed_password=hashed_password,
        )
        return {
            "id": str(created_user.id),
            "first_name": created_user.first_name,
            "last_name": created_user.last_name,
            "email": created_user.email,
            "mobile_number": created_user.mobile_number,
            "is_verified": created_user.is_verified,
        }

    def authenticate_user(self, user_login: UserLoginSchema):
        # جستجو کاربر با ایمیل یا موبایل
        user = self.user_service.get_by_email_or_mobile(
            email=user_login.username,
            mobile_number=user_login.username,
        )

        if not user or not self.hash_service.verify_password(user_login.password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Invalid credentials")

        access_token = self.create_access_token(data={"sub": str(user.id)})

        return {"access_token": access_token, "token_type": "bearer"}

    def authenticate_user_via_oauth(self, form_data: OAuth2PasswordRequestForm):
        user = self.user_service.get_by_email_or_mobile(
            email=form_data.username,
            mobile_number=form_data.username,
        )
        if not user or not self.hash_service.verify_password(form_data.password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Invalid credentials")
        access_token = self.create_access_token(data={"sub": str(user.id)})
        return {"access_token": access_token, "token_type": "bearer"}
