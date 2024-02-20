import typing
import strawberry
from data import book_data, author_data, book_data_backup
from datetime import date
import time

""" FUNCTIONS """
def new_book_id() -> int:
    if book_data == []: 
        return 1
    else:
        book_ids = [book["id"] for book in book_data]
        return max(book_ids) + 1


def get_books_for_author(root: "Author") -> typing.List["Book"]:
    books = []
    for book in book_data:
        if root.id in book["author_ids"]:
            # books.append(Book(id=book["id"], title=book["title"]))
            books.append(Book(**book))
    return books

def get_books(root) -> typing.List["Book"]:
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
    books: typing.List["Book"] = strawberry.field(resolver=get_books_for_author)

@strawberry.type
class Book:
    id: int
    title: str
    year: int | None
    author_ids: typing.List[int]

    @strawberry.field(description="Get a list of authors.")
    def authors(self, order_by: str = "name", reverse: bool = False) -> typing.List["Author"]:
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
    

@strawberry.type
class Query:

    @strawberry.field(description="Get a list of authors.")
    def authors(
            self, 
            id: typing.Optional[int] = strawberry.UNSET,
            order_by: str = "name",
            reverse: bool = False,
            name: typing.Optional[str] = strawberry.UNSET
        ) -> typing.List[Author]:
        
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

    books: typing.List[Book] = strawberry.field(resolver=get_books)




@strawberry.type
class Mutation:

    @strawberry.mutation
    def add_book(
            self, 
            id: int, 
            title: str, 
            year: int | None = None,
            author_ids: typing.List[int] = []
        ) -> Book | None:
        if not book_id_exists(id):
            book = {
                "id": id,
                "title": title,
                "year": year,
                "author_ids": author_ids
            }
            book_data.append(book)
            return Book(**book)     
        else:
            return None 
        
        
    @strawberry.mutation
    def update_book(
            self, 
            id: typing.Optional[int] = strawberry.UNSET, 
            title: typing.Optional[str] = None, 
            year: typing.Optional[int] = None, 
            author_ids: typing.Optional[typing.List[int]] = None
        ) -> Book | None:

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
                return None
    
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



schema = strawberry.Schema(query=Query, mutation=Mutation)

m = Mutation()
book = m.update_book(title="De laatste roker", year=1980, author_ids=[3])

pass


# query = """
#     mutation UpdateBook {
#         updateBook(title: "De laatste roker", year: 1980, authorIds: [3]) {
#             id
#             title
#             year
#             authors {
#                 name
#             }
#         }
#     }
# """

# result = schema.execute_sync(
#         query)

# print(result.errors)

# print(result.data)



