import datetime
from typing import List, Union, Optional


import strawberry
 
BOOKS_LOOKUP = {
    "Frank Herbert": [
        {
            "title": "Dune",
            "date_published": "1965-08-01",
            "price": "5.99",
            "isbn": 9780801950773,
        }
    ],
}




@strawberry.type
class Book:
    title: str
    author: "Author"
    date_published: datetime.date
    price: float
    isbn: str



@strawberry.type
class Query:
    @strawberry.field
    def get_books_by_author(root: "Author") -> List["Book"]:
        stored_books = BOOKS_LOOKUP[root.name]


        return [
            Book(
                title=book.get("title"),
                author=root,
                date_published=book.get("date_published"),
                price=book.get("price"),
                isbn=book.get("isbn"),
            )
            for book in stored_books
        ]
    
def get_books_by_author(root: "Author") -> List["Book"]:
    stored_books = BOOKS_LOOKUP[root.name]


    return [
        Book(
            title=book.get("title"),
            author=root,
            date_published=book.get("date_published"),
            price=book.get("price"),
            isbn=book.get("isbn"),
        )
        for book in stored_books
    ]




@strawberry.type
class Author:
    name: str
    books: List[Book] = strawberry.field(resolver=get_books_by_author)




@strawberry.type
class Group:
    name: Optional[str]  # groups of authors don't necessarily have names
    authors: List[Author]


    @strawberry.field
    def books(self) -> List[Book]:
        books = []


        for author in self.authors:
            books += get_books_by_author(author)


        return books
    
schema = strawberry.Schema(query=Query)