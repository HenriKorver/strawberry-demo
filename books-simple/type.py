import strawberry
from typing import List, Optional, Dict, Any
from data import author_data, book_data
from enum import Enum
# from strawberry.dataloader import DataLoader

@strawberry.enum
class Category(Enum):
    FICTION = "fiction"
    NON_FICTION = "non-fiction"


@strawberry.type
class Author:
    id: int
    name: str


# def author(id) -> Author:
#         for author in author_data:
#             if author["id"] == id:
#                 author_name = author["name"]
#         return Author(id=id, name=author_name)

# async def load_authors(ids) -> List[Author]:
#     return [author(id) for id in ids]

# loader = DataLoader(load_fn=load_authors)


@strawberry.type 
class Book:
    id: int
    title: str
    year: int | None
    category: Optional[Category] = None
    author_id: int

    @strawberry.field
    def author(self) -> Author:
        for author in author_data:
            if author["id"] == self.author_id:
                author_name = author["name"]
        return Author(id=self.author_id, name=author_name)

    # @strawberry.field
    # async def author(self) -> Author:
    #      print(f"Author_id: {self.author_id}")
    #      return await loader.load(self.author_id)

    
    @staticmethod
    def from_row(row: Dict[str, Any]):
        return Book(
            id=row["id"], 
            title=row["title"], 
            year=row["year"], 
            author_id= row["author_id"]
        )