from sqlalchemy.orm import Session
from app.domain.models.book import Book
from app.domain.schemas.book_schema import BookCreate, BookUpdate

class BookRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, book_id: int):
        return self.db.query(Book).filter(Book.id == book_id).first()

    def get_by_isbn(self, isbn: str):
        return self.db.query(Book).filter(Book.isbn == isbn).first()

    def list(self, skip: int = 0, limit: int = 10):
        return self.db.query(Book).offset(skip).limit(limit).all()

    def create(self, book: BookCreate):
        db_book = Book(**book.dict())
        self.db.add(db_book)
        self.db.commit()
        self.db.refresh(db_book)
        return db_book

    def update(self, db_book: Book, book_update: BookUpdate):
        for key, value in book_update.dict(exclude_unset=True).items():
            setattr(db_book, key, value)
        self.db.commit()
        self.db.refresh(db_book)
        return db_book

    def delete(self, db_book: Book):
        self.db.delete(db_book)
        self.db.commit()
