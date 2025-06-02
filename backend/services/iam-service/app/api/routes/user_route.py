from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


from app.core.db.database import get_db
from app.domain.schemas.user_schema import UserCreateSchema ,UserWelcomeSchema ,TokenSchema
from app.services.auth_services.auth_service import AuthService
from app.services.auth_services.hash_service import HashService
from app.services.user_service import UserService
from app.core.security import get_current_user
from app.domain.models.user import User

router = APIRouter(tags=["users"])

def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    hash_service = HashService()
    user_service = UserService(db)
    return AuthService(hash_service=hash_service, user_service=user_service)

@router.post("/register", status_code=201)
def register_user(
    user: UserCreateSchema,
    auth_service: AuthService = Depends(get_auth_service)
):
    created = auth_service.register_user(user)
    return {"message": "User created successfully", "user": created}

# @router.post("/login", response_model=TokenSchema)
# async def login_user(
#     form_data: OAuth2PasswordRequestForm = Depends(),
#     auth_service: AuthService = Depends(get_auth_service),
# ):
#     return auth_service.authenticate_user_via_oauth(form_data)

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service)
):
    user = auth_service.authenticate_user_via_oauth(form_data)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    return user

@router.get("/me", response_model=UserWelcomeSchema)
def read_users_me(current_user: User = Depends(get_current_user)):
    message = f"Dear {current_user.first_name} welcome to whisperSoftWord!"
    return UserWelcomeSchema(
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        email=current_user.email,
        message=message
    )