import strawberry
from typing import List, Optional, Dict, Any, TYPE_CHECKING, Annotated
from data import author_data, book_data
from enum import Enum

if TYPE_CHECKING:
    from books import Book


@strawberry.type
class Author:
    id: int
    name: str

    @strawberry.field
    def books(self) -> List[Annotated["Book", strawberry.lazy("books")]]:
        from books import Book # to avoid circulair definition
        books = []
        for book in book_data:
            if self.id in book["author_ids"]:
                books.append(Book(**book))
        return books




