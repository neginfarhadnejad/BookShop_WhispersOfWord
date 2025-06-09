from fastapi import HTTPException, status
from app.domain.schemas.user_schema import UserCreateSchema
from app.services.user_service import UserService
from app.services.auth_services.hash_service import HashService

class UserAuthService:
    def __init__(self, hash_service: HashService, user_service: UserService):
        self.hash_service = hash_service
        self.user_service = user_service

    def register_user(self, user_create: UserCreateSchema):
        try:
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
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            print("EXCEPTION:", e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Registration failed: {str(e)}"
            )
