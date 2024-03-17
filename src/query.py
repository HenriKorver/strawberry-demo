from typing import List, TypeVar, Dict, Any, Generic, Optional, Union
import strawberry
from data import book_data, author_data, book_data_backup
from datetime import date
import time
from enum import Enum
from type import Book, Author
from query_helper import *
from pagination_window import PaginationWindow

@strawberry.type
class Query:

    @strawberry.field(description="Get a list of authors.")
    def authors(
            self, 
            id: Optional[int] = strawberry.UNSET,
            order_by: str = "name",
            reverse: bool = False,
            name: Optional[str] = strawberry.UNSET
        ) -> List[Author]:
        
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

    books: List[Book] = strawberry.field(resolver=get_books)

    @strawberry.field
    def books_paginated(
        self,
        order_by: str,
        limit: int,
        offset: int = 0,
        title: str | None = None,
        year: str | None = None,
    ) -> PaginationWindow[Book]:
        
        filters = {}

        if title:
            filters["title"] = title
 
        if year:
            filters["year"] = year
 
        return get_pagination_window(
            dataset=book_data,
            ItemType=Book,
            order_by=order_by,
            limit=limit,
            offset=offset,
            filters=filters,
        )