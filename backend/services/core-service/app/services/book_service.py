from app.infrastructure.repositories.book_repository import BookRepository
from app.domain.schemas.book_schema import BookCreate, BookUpdate

class BookService:
    def __init__(self, repository: BookRepository):
        self.repository = repository

    def get_book(self, book_id: int):
        return self.repository.get(book_id)

    def list_books(self, skip: int = 0, limit: int = 10):
        return self.repository.list(skip=skip, limit=limit)

    def create_book(self, book_data: BookCreate):
        return self.repository.create(book_data)

    def update_book(self, book_id: int, book_data: BookUpdate):
        db_book = self.repository.get(book_id)
        if not db_book:
            return None
        return self.repository.update(db_book, book_data)

    def delete_book(self, book_id: int):
        db_book = self.repository.get(book_id)
        if not db_book:
            return None
        self.repository.delete(db_book)
        return True
