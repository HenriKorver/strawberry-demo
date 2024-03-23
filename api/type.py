import strawberry
from typing import List, Optional, Dict, Any
from data import author_data, book_data
from enum import Enum

@strawberry.enum
class Category(Enum):
    FICTION = "fiction"
    NON_FICTION = "non-fiction"

def authors(self, order_by: str = "name", reverse: bool = False) -> List["Author"]:
        # time.sleep(1) # simulate that authors live in a different system
        authors = []
        for book in book_data:
            if self.id == book["id"]:
                for author_id in book["author_ids"]:
                    for author in author_data:
                        if author_id == author["id"]:
                            authors.append(Author(id=author["id"], name=author["name"]))
        authors.sort(key=lambda x: getattr(x, order_by),reverse=reverse)
        return authors 

def get_books_for_author(root: "Author") -> List["Book"]:
    books = []
    for book in book_data:
        if root.id in book["author_ids"]:
            books.append(Book(**book))
    return books

@strawberry.type
class Author:
    id: int
    name: str
    books: List["Book"] = strawberry.field(resolver=get_books_for_author)

@strawberry.type 
class Book:
    id: int
    title: str
    year: int | None
    category: Optional[Category] = None
    author_ids: List[int]

    authors: List["Author"] =  strawberry.field(
        resolver=authors,
        description="Get a list of authors.")
    
    
    @staticmethod
    def from_row(row: Dict[str, Any]):
        return Book(
            id=row["id"], 
            title=row["title"], 
            year=row["year"], 
            author_ids=row["author_ids"]
        )