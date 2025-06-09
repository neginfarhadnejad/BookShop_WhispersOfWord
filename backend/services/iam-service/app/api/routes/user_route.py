from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.core.db.database import get_db
from app.domain.schemas.user_schema import UserCreateSchema, UserWelcomeSchema
from app.services.auth_services.user_auth_service import UserAuthService
from app.services.auth_services.auth_service import AuthService
from app.services.auth_services.hash_service import HashService
from app.services.user_service import UserService
from app.services.admin_service import AdminService  # اضافه کن
from app.core.security import get_current_user
from app.domain.models.user import User

router = APIRouter(tags=["users"])

def get_user_auth_service(db: Session = Depends(get_db)):
    hash_service = HashService()
    user_service = UserService(db)
    return UserAuthService(hash_service, user_service)


@router.post("/register", status_code=201, response_model=UserWelcomeSchema)
def register_user(
    user: UserCreateSchema,
    user_auth_service: UserAuthService = Depends(get_user_auth_service)
) -> UserWelcomeSchema:
    try:
        created = user_auth_service.register_user(user)
        return UserWelcomeSchema(
            first_name=created["first_name"],
            last_name=created["last_name"],
            email=created["email"],
            message=f"Dear {created['first_name']} welcome to whisperSoftWord!",
            role="user"
        )
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        import traceback
        print("EXCEPTION:", e)
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")


@router.get("/me", response_model=UserWelcomeSchema)
def read_users_me(current_user: User = Depends(get_current_user)):
    try:
        message = f"Dear {current_user.first_name} welcome to whisperSoftWord!"
        return UserWelcomeSchema(
            first_name=current_user.first_name,
            last_name=current_user.last_name,
            email=current_user.email,
            message=message,
            role=current_user.role
        )
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")
