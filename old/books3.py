import typing
import strawberry

book_data= [
    {
        "id": 1,
        "title": "De Aanslag",
        "author": 1
    },
    {
        "id": 2,
        "title": "De Donkere Kamer van Damocles",
        "author": 2
    },
    {
        "id": 3,
        "title": "Nooit meer slapen",
        "author": 2
    },
]

author_data= [
    {
        "id": 1,
        "name": "Harry Mulisch",
        "books": [1]
    },
    {
        "id": 2,
        "name": "Willem Frederik Hermans",
        "books": [2,3]
    },
]


def get_author_for_book(root) -> typing.Optional["Author"]:
    for author in author_data:
        if root.id in author["books"]:
            return Author(id=author["id"], name=author["name"])
        
def get_books_for_author(root) -> typing.List["Book"]:
    books = []
    for book in book_data:
        if root.id == book["author"]:
            books.append(Book(id=book["id"], title=book["title"]))
    return books

@strawberry.type
class Book:
    id: int
    title: str
    author: "Author" = strawberry.field(resolver=get_author_for_book)

@strawberry.type
class Author:
    id: int
    name: str
    books: typing.List[Book] = strawberry.field(resolver=get_books_for_author)


def get_authors(root) -> typing.List[Author]:
    return [Author(id=item["id"], name=item["name"]) for item in author_data]

def get_books(root) -> typing.List[Book]:
    return [Book(id=item["id"], title=item["title"]) for item in book_data]

@strawberry.type
class Query:
    authors: typing.List[Author] = strawberry.field(resolver=get_authors)
    books: typing.List[Book] = strawberry.field(resolver=get_books)

schema = strawberry.Schema(query=Query)