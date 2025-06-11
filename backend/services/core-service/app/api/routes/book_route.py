from fastapi import APIRouter, Depends, HTTPException, status
from app.services.book_service import BookService
from app.domain.schemas.book_schema import BookCreate, BookListResponse
from app.infrastructure.repositories.book_repository import BookRepository
from app.core.db.database import get_db
from app.core.auth.security import is_admin  # dependency برای چک کردن ادمین بودن
from sqlalchemy.orm import Session  # وارد کردن Session از sqlalchemy.orm

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)

def get_book_service(db: Session = Depends(get_db)):
    return BookService(BookRepository(db))

# فقط ادمین‌ها اجازه دارند کتاب ایجاد کنند
@router.post("/", response_model=BookListResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, service: BookService = Depends(get_book_service), role: str = Depends(is_admin)):
    db_book = service.create_book(book)
    if not db_book:
        raise HTTPException(status_code=400, detail="Book could not be created")
    return db_book

# این روت قابل دسترسی برای همه است، برای مثال برای لیست کردن کتاب‌ها
@router.get("/", response_model=list[BookListResponse])
def list_books(service: BookService = Depends(get_book_service)):
    books = service.list_books()
    return books
