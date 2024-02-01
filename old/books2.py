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

# def get_author_for_book(root) -> "Author":
#     return Author(name="Michael Crichton")

def get_author_for_book(id: int) -> "Author":
    for author in author_data:
        if id in author["books"]:
            return Author(author["id"], author["name"], get_books_for_author(author["id"]))

@strawberry.type
class Book:
    id: int
    title: str
    author: "Author"
    # author: "Author" = strawberry.field(resolver=get_author_for_book)



# def get_books_for_author(root):
#     return [Book(title="Jurassic Park")]

def get_books_for_author(id: int) -> typing.List[Book]:
    books = []
    for book in book_data:
        if id == book["author"]:
            books.append(Book(book["id"], book["title"], get_author_for_book(book["id"])))
    return books

@strawberry.type
class Author:
    id: int
    name: str
    books: typing.List[Book]
    # books: typing.List[Book] = strawberry.field(resolver=get_books_for_author)


# def get_authors(root) -> typing.List[Author]:
#     return [Author(name="Michael Crichton")]

def get_authors(root) -> typing.List[Author]:
    return [Author(item["id"], item["name"], get_books_for_author(item["id"])) for item in author_data]

def get_books(root) -> typing.List[Book]:
    return [Book(item["id"], item["title"], get_author_for_book(item["id"])) for item in book_data]

@strawberry.type
class Query:
    authors: typing.List[Author] = strawberry.field(resolver=get_authors)
    books: typing.List[Book] = strawberry.field(resolver=get_books)

schema = strawberry.Schema(query=Query)