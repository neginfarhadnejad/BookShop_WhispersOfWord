from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.db.database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256), nullable=False)
    author = Column(String(128), nullable=False)
    price = Column(Float, nullable=False)
    isbn = Column(String(64), unique=True, nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    cover_image_url = Column(String(1024), nullable=True)
    description = Column(String(2048), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # روابط (در ادامه تعریف می‌شن)
    # reviews = relationship("Review", back_populates="book")
    # categories = relationship("Category", secondary="book_categories", back_populates="books")
