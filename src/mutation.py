import strawberry
from typing import List, Optional, Union
from type import Book, Category
from data import book_data, book_data_backup
from mutation_helper import new_book_id, index_book


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

    @strawberry.mutation(description="Reset books")
    def reset_books(self) -> None:
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