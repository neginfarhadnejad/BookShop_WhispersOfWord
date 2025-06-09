from fastapi import HTTPException, status
from app.domain.schemas.admin_schema import AdminCreateSchema
from app.services.admin_service import AdminService
from app.services.auth_services.hash_service import HashService

class AdminAuthService:
    def __init__(self, hash_service: HashService, admin_service: AdminService):
        self.hash_service = hash_service
        self.admin_service = admin_service

    def register_admin(self, admin_create: AdminCreateSchema):
        try:
            # چک تکراری بودن ایمیل یا موبایل
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
