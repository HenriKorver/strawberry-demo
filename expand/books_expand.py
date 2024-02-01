import typing
import strawberry
import copy

# source virtualenv/Scripts/activate (in git bash)
# strawberry server books5
# http://127.0.0.1:8000/graphql

"""
To do:
- Paginering
- addAuthor operatie toevoegen
- publish date en geboortedatum toevoegen
- expand mechanisme uitwerken (in graphql is dotnotatie niet nodig)
"""

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
    },
    {
        "id": 2,
        "name": "Willem Frederik Hermans",
    },
    {
        "id": 3,
        "name": "M. Euwe",
    },
    {
        "id": 4,
        "name": "H. Kramer",
    }
]

book_data_backup = copy.deepcopy(book_data)
author_data_backup = copy.deepcopy(author_data)

def get_authors_for_book(root: "Book") -> typing.List["Author"]:
    authors = []
    for book in book_data:
        if root.id == book["id"]:
            for author_id in book["authors"]:
                for author in author_data:
                    if author_id == author["id"]:
                        authors.append(Author(id=author["id"], name=author["name"]))
    return authors

def get_books_for_author(root: "Author") -> typing.List["Book"]:
    books = []
    for book in book_data:
        if root.id in book["authors"]:
            books.append(Book(id=book["id"], title=book["title"], authors=book["authors"]))
    return books
   

@strawberry.type
class Book:
    id: int
    title: str
    authors: typing.List[int]

    @strawberry.field(description="Get a list of authors.")
    def authors_expanded(self, order_by: str = "name", reverse: bool = False) -> typing.List["Author"]:
        authors = []
        for book in book_data:
            if self.id == book["id"]:
                for author_id in book["authors"]:
                    for author in author_data:
                        if author_id == author["id"]:
                            authors.append(Author(id=author["id"], name=author["name"]))
        authors.sort(key=lambda x: getattr(x, order_by),reverse=reverse)
        return authors
    
    # authors: typing.List["Author"] = strawberry.field(resolver=get_authors_for_book)


@strawberry.type
class Author:
    id: int
    name: str
    books: typing.List[Book] = strawberry.field(resolver=get_books_for_author)



def get_books(root) -> typing.List[Book]:
    return [Book(id=item["id"], title=item["title"], authors=item["authors"]) for item in book_data]

@strawberry.type
class Query:
    # authors: typing.List[Author] = strawberry.field(resolver=get_authors)
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
        # print(authors)
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
            return Book(id=id, title=title, authors=authors)     
        else:
            return None 
        
    # @strawberry.mutation
    # def update_book(self, id: int, title: typing.Optional[str] = None, authors: typing.Optional[typing.List[int]] = None ) -> Book | None:
    #     index = index_book(id)
    #     if index > -1 and title != None: #uiteindelijk moeten we als title = None de title ophalen uit book_data, nu wordt de update gewoon niet uitgevoerd.
    #         book_data[index] = {
    #             "id": id,
    #             "title": title,
    #             "authors": authors
    #         }
    #         return Book(id=id, title=title, author_ids=authors)
    #     else:
    #         return None
    
    @strawberry.mutation
    def delete_book(self, id: int) -> Book | None:
        index = index_book(id)
        if index > -1:
            book_row = book_data[index]
            book = Book(id=id, title=book_row["title"], authors=book_row["authors"])
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

# print("test")

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
