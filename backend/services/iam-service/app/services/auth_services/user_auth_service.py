from fastapi import HTTPException, status
from app.domain.schemas.user_schema import UserCreateSchema
from app.services.user_service import UserService
from app.services.auth_services.hash_service import HashService
from datetime import datetime, timedelta
from jose import jwt
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
        try:
            # بررسی اینکه آیا ایمیل یا شماره موبایل تکراری است
            existing_user = self.user_service.get_by_email_or_mobile(
                user_create.email, user_create.mobile_number
            )
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email or mobile number already registered",
                )

            # هش کردن رمز عبور
            hashed_password = self.hash_service.hash_password(user_create.password)

            # ایجاد کاربر جدید
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

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Registration failed: {str(e)}")

    def authenticate_user_via_oauth(self, form_data):
        try:
            # جستجو برای کاربر با ایمیل یا شماره موبایل
            user = self.user_service.get_by_email_or_mobile(
                email=form_data.username,
                mobile_number=form_data.username,
            )

            # اگر کاربر پیدا نشد یا رمز عبور اشتباه باشد
            if not user or not self.hash_service.verify_password(form_data.password, user.hashed_password):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

            # ایجاد توکن JWT
            access_token = self.create_access_token(data={"sub": str(user.id)})

            return {"access_token": access_token, "token_type": "bearer"}

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Authentication failed: {str(e)}")
