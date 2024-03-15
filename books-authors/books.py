from typing import List, TypeVar, Dict, Any, Generic, Optional, Union
import strawberry
from data import book_data, author_data, book_data_backup
from datetime import date
import time
from enum import Enum

Item = TypeVar("Item")

""" FUNCTIONS """
def get_pagination_window(
    dataset: List[Item],
    ItemType: type,
    order_by: str,
    limit: int,
    offset: int = 0,
    filters: dict[str, str] = {},
) -> "PaginationWindow":
    """
    Get one pagination window on the given dataset for the given limit
    and offset, ordered by the given attribute and filtered using the
    given filters
    """


    if limit <= 0 or limit > 100:
        raise Exception(f"limit ({limit}) must be between 0-100")


    if filters:
        dataset = list(filter(lambda x: matches(x, filters), dataset))


    dataset.sort(key=lambda x: x[order_by])


    if offset != 0 and not 0 <= offset < len(dataset):
        raise Exception(f"offset ({offset}) is out of range " f"(0-{len(dataset) - 1})")


    total_items_count = len(dataset)


    items = dataset[offset : offset + limit]


    items = [ItemType.from_row(x) for x in items]


    return PaginationWindow(
        items=items, 
        total_items_count=total_items_count
    )


def new_book_id() -> int:
    if book_data == []: 
        return 1
    else:
        book_ids = [book["id"] for book in book_data]
        return max(book_ids) + 1


def get_books_for_author(root: "Author") -> List["Book"]:
    books = []
    for book in book_data:
        if root.id in book["author_ids"]:
            books.append(Book(**book))
    return books

def get_books(root) -> List["Book"]:
    return [Book(**item) for item in book_data]

def book_id_exists(id: int) -> bool:
    for book in book_data:
        if book["id"] == id:
            return True
    return False

def index_book(id: int) -> int:
    for i, book in enumerate(book_data):
        if book["id"] == id:
            return i
    return -1

def matches(item, filters):
    """
    Test whether the item matches the given filters.
    The match is case insensitive.
    This demo only supports filtering by string fields.
    """
    for attr_name, val in filters.items():
        if val.lower() not in getattr(item, attr_name).lower():
            return False
    return True

""" SCHEMA """
@strawberry.type
class Author:
    id: int
    name: str
    books: List["Book"] = strawberry.field(resolver=get_books_for_author)

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

    @strawberry.field(description="Get a list of authors.")
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
    
    @staticmethod
    def from_row(row: Dict[str, Any]):
        return Book(id=row["id"], title=row["title"], year=row["year"], author_ids=row["author_ids"])


@strawberry.type
class PaginationWindow(Generic[Item]):
    items: List[Item] = strawberry.field(
        description="The list of items in this pagination window."
    )


    total_items_count: int = strawberry.field(
        description="Total number of items in the filtered dataset."
    )

@strawberry.type
class Query:

    @strawberry.field(description="Get a list of authors.")
    def authors(
            self, 
            id: Optional[int] = strawberry.UNSET,
            order_by: str = "name",
            reverse: bool = False,
            name: Optional[str] = strawberry.UNSET
        ) -> List[Author]:
        
        if (id is not strawberry.UNSET) and (id is not None):
            for author in author_data:
                if author["id"] == id:
                    return [Author(**author)]
            return []
        else:
            if order_by is strawberry.UNSET: 
                order_by = "name"
            if reverse is strawberry.UNSET: 
                reverse = False
            if name is strawberry.UNSET:
                name = None

            authors = [Author(id=item["id"], name=item["name"]) for item in author_data]
            filters = {}
            if name is not (strawberry.UNSET or None):
                filters["name"] = name
            authors = list(filter(lambda x: matches(x, filters), authors))
            authors.sort(key=lambda x: getattr(x, order_by),reverse=reverse)
            return authors

        
    
    @strawberry.field
    def author_by_id(self, id: int) -> Author | None:
        for author in author_data:
            if author["id"] == id:
                return Author(**author)
        return None

    books: List[Book] = strawberry.field(resolver=get_books)

    @strawberry.field
    def books_paginated(
        self,
        order_by: str,
        limit: int,
        offset: int = 0,
        title: str | None = None,
        year: str | None = None,
    ) -> PaginationWindow[Book]:
        
        filters = {}

        if title:
            filters["title"] = title
 
        if year:
            filters["year"] = year
 
        return get_pagination_window(
            dataset=book_data,
            ItemType=Book,
            order_by=order_by,
            limit=limit,
            offset=offset,
            filters=filters,
        )

# q = Query()
# result = q.books(limit=10, order_by="title")

# pass


@strawberry.type
class Error:
    code: str
    description: str



@strawberry.type
class Mutation:

    @strawberry.mutation
    def add_book(
            self, 
            title: str, 
            year: int | None = None,
            category: Category | None = None,
            author_ids: List[int] = []
        ) -> Book | None:
            book = {
                "id": new_book_id(),
                "title": title,
                "year": year,
                "category": Category,
                "author_ids": author_ids
            }
            book_data.append(book)
            return Book(**book)     
        
        
    @strawberry.mutation
    def update_book(
            self, 
            id: Optional[int] = strawberry.UNSET, 
            title: Optional[str] = None, 
            year: Optional[int] = None, 
            author_ids: Optional[List[int]] = None
        ) -> Union[Book, Error]:

        if (id is strawberry.UNSET) or (id is None):
            book = {
                "id": new_book_id(),
                "title": title,
                "year": year,
                "author_ids": author_ids
            }
            book_data.append(book)
            return(Book(**book))
        else: 
            id = int(id or -1) # if id is not een integer convert it to -1
            index = index_book(id)
            if index > -1: 
                '''
                uiteindelijk als title = None de title ophalen uit book_data, 
                nu wordt de update gewoon niet uitgevoerd.
                '''
                if title != None:
                    book_data[index]["title"] = title
                if year != None:
                    book_data[index]["year"] = year
                if author_ids != None:
                    book_data[index]["author_ids"] = author_ids
                
                return Book(**book_data[index])
            else:
                # raise Exception(f"Book id {id} does not exist")
                return Error(description=f"Book ID {id} does not exist", code="201")
    
    @strawberry.mutation
    def delete_book(self, id: int) -> Book | None:
        index = index_book(id)
        if index > -1:
            book_row = book_data[index]
            book = Book(**book_row)
            book_data.pop(index)
            return book
        else:
            return None
        
    @strawberry.mutation
    def delete_all_books(self) -> None:
        book_data.clear()

    @strawberry.mutation
    def reset_books(self) -> None:
        # instructie 'book_data = book_data_backup' werkt helaas niet
        book_data.clear()
        book_data.extend(book_data_backup)

    
    @strawberry.mutation
    def generate_books(self, number: int) -> None:
        book_data.clear()
        for i in range(1, number):
            book = {
                "id": i,
                "title": f"Title {i}",
                "year": 1900 + (i % 2023),
                "category": Category.FICTION,
                "author_ids": [1, 2]
            }
            book_data.append(book)


schema = strawberry.Schema(query=Query, mutation=Mutation)

