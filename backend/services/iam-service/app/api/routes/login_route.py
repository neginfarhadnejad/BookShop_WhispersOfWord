from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.db.database import get_db
from app.services.user_service import UserService
from app.services.admin_service import AdminService
from app.services.auth_services.auth_service import AuthService
from app.services.auth_services.hash_service import HashService
from app.domain.schemas.token_schema import TokenSchema

# فقط همین یک خط
router = APIRouter(tags=["login"])

def get_auth_service(db: Session = Depends(get_db)):
    hash_service = HashService()
    user_service = UserService(db)
    admin_service = AdminService(db)
    return AuthService(hash_service, user_service, admin_service)

@router.post("/login", response_model=TokenSchema)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service)
):
    token = auth_service.authenticate_via_oauth(form_data)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    return token
