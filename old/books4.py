import typing
import strawberry

book_data= [
    {
        "id": 1,
        "title": "De Aanslag",
        "authors": [1]
    },
    {
        "id": 2,
        "title": "De Donkere Kamer van Damocles",
        "authors": [2]
    },
    {
        "id": 3,
        "title": "Nooit meer slapen",
        "authors": [2]
    },
    {
        "id": 4,
        "title": "Theorie van het schaakspel: Het middenspel 1",
        "authors": [3,4]
    }
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
    {
        "id": 3,
        "name": "M. Euwe",
        "books": [4]
    },
    {
        "id": 4,
        "name": "H. Kramer",
        "books": [4]
    }
]

def get_authors_for_book(root) -> typing.List["Author"]:
    authors = []
    for author in author_data:
        if root.id in author["books"]:
            authors.append(Author(id=author["id"], name=author["name"]))
    return authors

def get_books_for_author(root) -> typing.List["Book"]:
    books = []
    for book in book_data:
        if root.id in book["authors"]:
            books.append(Book(id=book["id"], title=book["title"]))
    return books

@strawberry.type
class Book:
    id: int
    title: str
    authors: typing.List["Author"] = strawberry.field(resolver=get_authors_for_book)

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