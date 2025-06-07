from sqlalchemy.orm import Session
from app.core.db.database import get_db
from app.domain.models.admin import Admin
from fastapi import Depends
from app.services.auth_services.hash_service import HashService


class AdminService:
    def __init__(self, db: Session, hash_service: HashService):
        self.db = db
        self.hash_service = hash_service

    def get_by_email_or_phone(self, email: str, phone_number: str):
        return self.db.query(Admin).filter(
            (Admin.email == email) | (Admin.phone_number == phone_number)
        ).first()

    def create_admin(self, name: str, email: str, phone_number: str, hashed_password: str, role="admin"):
        admin = Admin(
            name=name,
            email=email,
            phone_number=phone_number,
            hashed_password=hashed_password,
            is_verified=False,
            role=role
        )
        self.db.add(admin)
        self.db.commit()
        self.db.refresh(admin)
        return admin
