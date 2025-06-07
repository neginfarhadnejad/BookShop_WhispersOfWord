from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.db.database import get_db
from app.domain.schemas.admin_schema import AdminCreateSchema, AdminResponseSchema, AdminLoginSchema, AdminWelcomeSchema ,TokenSchema
from app.services.auth_services.admin_auth_service import AdminAuthService
from app.services.auth_services.hash_service import HashService
from app.services.admin_service import AdminService
from app.core.security import get_current_admin
from app.domain.models.admin import Admin

router = APIRouter(tags=["admins"])

def get_admin_auth_service(db: Session = Depends(get_db)) -> AdminAuthService:
    hash_service = HashService()  
    admin_service = AdminService(db=db, hash_service=hash_service)
    return AdminAuthService(hash_service=hash_service, admin_service=admin_service)


@router.post("/register", response_model=AdminResponseSchema)
async def register_admin(
    admin_data: AdminCreateSchema, 
    db: Session = Depends(get_db), 
    admin_auth_service: AdminService = Depends(get_admin_auth_service)
):
    name = admin_data.name
    email = admin_data.email
    phone_number = admin_data.phone_number
    password = admin_data.password  

    hashed_password = admin_auth_service.hash_service.hash_password(password)

    return admin_auth_service.create_admin(name, email, phone_number, hashed_password)



@router.post("/login", response_model=TokenSchema)
def login_admin(
    form_data: OAuth2PasswordRequestForm = Depends(),
    admin_auth_service: AdminAuthService = Depends(get_admin_auth_service)  
):

    admin = admin_auth_service.authenticate_admin_via_oauth(form_data)  
    if not admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    return admin



@router.get("/me", response_model=AdminWelcomeSchema)
def read_admins_me(current_admin: Admin = Depends(get_current_admin)):
    # Send a welcome message to the admin
    message = f"Dear {current_admin.name} welcome to Admin Portal!"
    return AdminWelcomeSchema(
        name=current_admin.name,
        email=current_admin.email,
        phone_number=current_admin.phone_number,
        message=message,
        role=current_admin.role
    )
