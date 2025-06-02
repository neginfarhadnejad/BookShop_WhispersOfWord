from sqlalchemy.orm import Session
from app.core.db.database import get_db
from app.domain.models.user import User
from fastapi import Depends

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email_or_mobile(self, email: str, mobile_number: str):
        return self.db.query(User).filter(
            (User.email == email) | (User.mobile_number == mobile_number)
        ).first()

    def create_user(self, first_name, last_name, email, mobile_number, hashed_password):
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            mobile_number=mobile_number,
            hashed_password=hashed_password,
            is_verified=False,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

