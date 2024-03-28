import strawberry
from type_dl import Book
from data import book_data
from typing import List



@strawberry.type
class Query:

    @strawberry.field(description="Get a list of books.")
    def get_books() -> List["Book"]:
        return [Book(**item) for item in book_data]
    
schema = strawberry.Schema(query=Query)