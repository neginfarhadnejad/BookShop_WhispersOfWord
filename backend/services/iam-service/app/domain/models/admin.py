from sqlalchemy import Column, Integer, String, TIMESTAMP, func, Sequence, Boolean
from app.core.db.database import Base  

class Admin(Base):
    __tablename__ = "admin"

    id = Column(Integer, Sequence("admin_id_seq"), primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone_number = Column(String(20), unique=True, nullable=False)
    date_of_birth = Column(String(15))
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default="admin")
    is_verified = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())
