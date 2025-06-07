from fastapi import HTTPException, status
from app.domain.schemas.admin_schema import AdminCreateSchema
from app.services.admin_service import AdminService
from app.services.auth_services.hash_service import HashService
from datetime import datetime, timedelta
from jose import jwt
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

class AdminAuthService:
    def __init__(self, hash_service: HashService, admin_service: AdminService):
        self.hash_service = hash_service
        self.admin_service = admin_service

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        # تابعی برای ایجاد توکن دسترسی JWT
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def register_admin(self, admin_create: AdminCreateSchema):
        try:
            # بررسی اینکه آیا ایمیل یا شماره موبایل تکراری است
            existing_admin = self.admin_service.get_by_email_or_phone(
                admin_create.email, admin_create.phone_number
            )
            if existing_admin:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email or phone number already registered",
                )

            # هش کردن رمز عبور
            hashed_password = self.hash_service.hash_password(admin_create.password)

            # ایجاد ادمین جدید
            created_admin = self.admin_service.create_admin(
                name=admin_create.name,
                email=admin_create.email,
                phone_number=admin_create.phone_number,
                hashed_password=hashed_password,
            )

            return {
                "id": str(created_admin.id),
                "name": created_admin.name,
                "email": created_admin.email,
                "phone_number": created_admin.phone_number,
                "is_verified": created_admin.is_verified,
            }

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Registration failed: {str(e)}")

    def authenticate_admin_via_oauth(self, form_data):
        try:
            # جستجو برای ادمین با ایمیل یا شماره موبایل
            admin = self.admin_service.get_by_email_or_phone(
                email=form_data.username,
                phone_number=form_data.username,
            )

            # اگر ادمین پیدا نشد یا رمز عبور اشتباه باشد
            if not admin or not self.hash_service.verify_password(form_data.password, admin.hashed_password):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

            # ایجاد توکن JWT
            access_token = self.create_access_token(data={"sub": str(admin.id)})

            return {"access_token": access_token, "token_type": "bearer"}

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Authentication failed: {str(e)}")
