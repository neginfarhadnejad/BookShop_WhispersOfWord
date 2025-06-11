from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class BookBase(BaseModel):
    title: str
    author: str
    price: float
    isbn: str
    cover_image_url: Optional[str] = None
    description: Optional[str] = None

class BookCreate(BookBase):
    stock: int

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    price: Optional[float] = None
    isbn: Optional[str] = None
    stock: Optional[int] = None
    cover_image_url: Optional[str] = None
    description: Optional[str] = None

class BookListResponse(BaseModel):
    id: int
    title: str
    author: str
    cover_image_url: Optional[str] = None
    is_available: bool

    class Config:
        orm_mode = True

class BookResponse(BookBase):
    id: int
    is_available: bool
    max_selectable: Optional[int] = None  
    created_at: datetime

    class Config:
        orm_mode = True

class AdminBookResponse(BookBase):
    id: int
    stock: int  
    created_at: datetime

    class Config:
        orm_mode = True
