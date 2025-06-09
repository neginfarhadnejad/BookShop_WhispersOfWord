from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.db.database import get_db
from app.domain.schemas.admin_schema import AdminCreateSchema, AdminResponseSchema, AdminWelcomeSchema
from app.services.auth_services.admin_auth_service import AdminAuthService
from app.services.auth_services.hash_service import HashService
from app.services.admin_service import AdminService
from app.core.security import get_current_admin
from app.domain.models.admin import Admin

router = APIRouter(tags=["admins"])

def get_admin_auth_service(db: Session = Depends(get_db)) -> AdminAuthService:
    hash_service = HashService()
    admin_service = AdminService(db)   # فقط db
    return AdminAuthService(hash_service=hash_service, admin_service=admin_service)


@router.post("/register", response_model=AdminResponseSchema)
async def register_admin(
    admin_data: AdminCreateSchema, 
    admin_auth_service: AdminAuthService = Depends(get_admin_auth_service)
):
    return admin_auth_service.register_admin(admin_data)

@router.get("/me", response_model=AdminWelcomeSchema)
def read_admins_me(current_admin: Admin = Depends(get_current_admin)):
    message = f"Dear {current_admin.name} welcome to Admin Portal!"
    return AdminWelcomeSchema(
        name=current_admin.name,
        email=current_admin.email,
        phone_number=current_admin.phone_number,
        message=message,
        role=current_admin.role
    )
