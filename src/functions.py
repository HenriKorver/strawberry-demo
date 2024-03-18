from typing import List, TypeVar, Dict, Any, Generic, Optional, Union
import strawberry
from data import book_data, author_data, book_data_backup
from datetime import date
import time
from enum import Enum
from pagination_window import Item, PaginationWindow
from books import Book
from authors import Author


""" FUNCTIONS """
def get_pagination_window(
    dataset: List[Item],
    ItemType: type,
    order_by: str,
    limit: int,
    offset: int = 0,
    filters: dict[str, str] = {},
) -> "PaginationWindow":
    """
    Get one pagination window on the given dataset for the given limit
    and offset, ordered by the given attribute and filtered using the
    given filters
    """


    if limit <= 0 or limit > 100:
        raise Exception(f"limit ({limit}) must be between 0-100")


    if filters:
        dataset = list(filter(lambda x: matches(x, filters), dataset))


    dataset.sort(key=lambda x: x[order_by])


    if offset != 0 and not 0 <= offset < len(dataset):
        raise Exception(f"offset ({offset}) is out of range " f"(0-{len(dataset) - 1})")


    total_items_count = len(dataset)


    items = dataset[offset : offset + limit]


    items = [ItemType.from_row(x) for x in items]


    return PaginationWindow(
        items=items, 
        total_items_count=total_items_count
    )


def new_book_id() -> int:
    if book_data == []: 
        return 1
    else:
        book_ids = [book["id"] for book in book_data]
        return max(book_ids) + 1


def get_books_for_author(root: "Author") -> List["Book"]:
    books = []
    for book in book_data:
        if root.id in book["author_ids"]:
            books.append(Book(**book))
    return books

def get_books(root) -> List["Book"]:
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
