import strawberry
from typing import List, Dict, Any





@strawberry.type
class Book:
    id: int
    title: str
    author: str

    @staticmethod
    def from_item(item: Dict):
        return Book(id=item["id"], title=item["title"], author=item["author"])
    
@strawberry.type
class Author:
    id: int
    name: str
    books: Book

books_dict = {
    1: {
        "id": 1,
        "title": "Onthulling",
        "author": "Henri"
    },
    2: {
        "id": 2,
        "title": "Aanslag",
        "author": "Peter"
    },
    
}

def max_key(dict: Dict[int, Any]) -> int:
    if dict == {}:
        return 0
    else:
        return next(reversed(dict.keys()))
    
@strawberry.type
class Query:
    @strawberry.field
    def get_a_book(self, id: int) -> Book:
        item = books_dict[id]
        return Book(id=id, title=item["title"], author=item["author"])
    
    @strawberry.field
    def get_all_books(self) -> List[Book]:
        lijst = []
        for key in list(books_dict.keys()):
            lijst.append(Book.from_item(books_dict[key]))
        return lijst

@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_book(self, title: str, author: str) -> Book:
        new_key = max_key(books_dict) + 1
        books_dict[new_key] = {"id": new_key, "title": title, "author": author}
        return Book(id=new_key, title=title, author=author)
    
    @strawberry.mutation
    def update_book(self, id: int, title: str, author: str) -> Book:
        books_dict[id] = {"id": id, "title": title, "author": author}
        return Book(id=id, title=title, author=author)

schema = strawberry.Schema(query=Query, mutation=Mutation)