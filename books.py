import typing
import strawberry
from data import book_data, author_data, book_data_backup

# source virtualenv/Scripts/activate (in git bash)
# strawberry server books
# http://127.0.0.1:8000/graphql
# strawberry export-schema books5:schema > books5_schema.graphql

"""
To do:
- Paginering
- addAuthor operatie toevoegen
- publish date en geboortedatum toevoegen
- expand mechanisme uitwerken (in graphql is dotnotatie niet nodig)
"""

def get_books_for_author(root: "Author") -> typing.List["Book"]:
    books = []
    for book in book_data:
        if root.id in book["authors"]:
            books.append(Book(id=book["id"], title=book["title"]))
    return books

@strawberry.type
class Author:

    id: int

    name: str

    books: typing.List["Book"] = strawberry.field(resolver=get_books_for_author)

@strawberry.type
class Book:

    id: int

    title: str

    @strawberry.field(description="Get a list of authors.")
    def authors(self, order_by: str = "name", reverse: bool = False) -> typing.List["Author"]:
        authors = []
        for book in book_data:
            if self.id == book["id"]:
                for author_id in book["authors"]:
                    for author in author_data:
                        if author_id == author["id"]:
                            authors.append(Author(id=author["id"], name=author["name"]))
        authors.sort(key=lambda x: getattr(x, order_by),reverse=reverse)
        return authors 





def get_authors_for_book(root: "Book") -> typing.List["Author"]:
    authors = []
    for book in book_data:
        if root.id == book["id"]:
            for author_id in book["authors"]:
                for author in author_data:
                    if author_id == author["id"]:
                        authors.append(Author(id=author["id"], name=author["name"]))
    return authors


def get_books(root) -> typing.List[Book]:
    return [Book(id=item["id"], title=item["title"]) for item in book_data]

@strawberry.type
class Query:

    @strawberry.field(description="Get a list of authors.")
    def authors(
        self, 
        order_by: str = "name",
        reverse: bool = False,
        name: str | None = None,
    ) -> typing.List[Author]:
        authors = [Author(id=item["id"], name=item["name"]) for item in author_data]
        filters = {}
        if name:
            filters["name"] = name
        authors = list(filter(lambda x: matches(x, filters), authors))
        authors.sort(key=lambda x: getattr(x, order_by),reverse=reverse)
        return authors

    books: typing.List[Book] = strawberry.field(resolver=get_books)

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

def update_book(id, title, authors):
    index = index_book(id)
    if index > -1:
        book_data[index] = {
            "title": title,
            "authors": authors
        }

@strawberry.type
class Mutation:

    @strawberry.mutation
    def add_book(self, id: int, title: str, authors: typing.List[int]) -> Book | None:
        if not book_id_exists(id):
            book = {
                "id": id,
                "title": title,
                "authors": authors
            }
            book_data.append(book)
            return Book(id=id, title=title)     
        else:
            return None 
        
    @strawberry.mutation
    def update_book(self, id: int, title: typing.Optional[str] = None, authors: typing.Optional[typing.List[int]] = None ) -> Book | None:
        index = index_book(id)
        if index > -1 and title != None: #uiteindelijk moeten we als title = None de title ophalen uit book_data, nu wordt de update gewoon niet uitgevoerd.
            book_data[index] = {
                "id": id,
                "title": title,
                "authors": authors
            }
            return Book(id=id, title=title)
        else:
            return None
    
    @strawberry.mutation
    def delete_book(self, id: int) -> Book | None:
        index = index_book(id)
        if index > -1:
            book_row = book_data[index]
            book = Book(id=id, title=book_row["title"])
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
        

schema = strawberry.Schema(query=Query, mutation=Mutation)

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

# query = """
#         query Authors {
#             authors (orderBy: "id") {
#                 name
#                 books {
#                     title
#                 }
#             }
#         }
#     """

# result = schema.execute_sync(
#         query)

# print(result.errors)

# print(result.data)

# q = Query()
# q.authors()
