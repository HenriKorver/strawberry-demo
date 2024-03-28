import strawberry
from typing import List, Optional, Dict, Any
from data import author_data, book_data
from enum import Enum
from strawberry.dataloader import DataLoader

@strawberry.enum
class Category(Enum):
    FICTION = "fiction"
    NON_FICTION = "non-fiction"


@strawberry.type
class Author:
    id: int
    name: str


async def load_authors(ids) -> List[Author]:
    print(f"dataloader: {ids}")
    author_list = []
    for author in author_data:
            if author["id"] in ids:
                author_list.append(
                     Author(id=author["id"], name=author["name"]))
    return author_list


loader = DataLoader(load_fn=load_authors)


@strawberry.type 
class Book:
    id: int
    title: str
    year: int | None
    category: Optional[Category] = None
    author_id: int

    @strawberry.field
    async def author(self) -> Author:
         print(f"get author: {self.author_id}")
         return await loader.load(self.author_id)