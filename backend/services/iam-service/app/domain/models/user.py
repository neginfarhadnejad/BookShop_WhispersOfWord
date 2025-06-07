import uuid
from sqlalchemy import Column, String, Boolean, TIMESTAMP, func ,Integer
from sqlalchemy.dialects.postgresql import UUID
from app.core.db.database import Base  

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False) 

    mobile_number = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_verified = Column(Boolean, nullable=False, default=False)
    created_at = Column(
        TIMESTAMP(timezone=True), 
        nullable=False, 
        server_default=func.now()
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), 
        nullable=True, 
        default=None, 
        onupdate=func.now()
    )
    role = Column(String, default="user")   

