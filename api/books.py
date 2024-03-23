import strawberry
from typing import List, Optional, Dict, Any, Annotated, TYPE_CHECKING
from data import author_data, book_data
from enum import Enum
from authors import Author

if TYPE_CHECKING:
    from authors import Author

@strawberry.enum
class Category(Enum):
    FICTION = "fiction"
    NON_FICTION = "non-fiction"



@strawberry.type 
class Book:
    id: int
    title: str
    year: int | None
    category: Optional[Category] = None
    author_ids: List[int]


    @strawberry.field
    def authors(self, order_by: str = "name", reverse: bool = False) \
                -> List[Annotated["Author", strawberry.lazy("authors")]]:
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
    
    
    @staticmethod
    def from_row(row: Dict[str, Any]):
        return Book(
            id=row["id"], 
            title=row["title"], 
            year=row["year"], 
            author_ids=row["author_ids"]
        )