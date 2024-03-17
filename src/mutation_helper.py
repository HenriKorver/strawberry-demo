from data import book_data

def new_book_id() -> int:
    if book_data == []: 
        return 1
    else:
        book_ids = [book["id"] for book in book_data]
        return max(book_ids) + 1

def index_book(id: int) -> int:
    for i, book in enumerate(book_data):
        if book["id"] == id:
            return i
    return -1

