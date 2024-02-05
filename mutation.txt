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
        ...

    @strawberry.mutation
    def update_book(
        self, 
        id: int, 
        title: typing.Optional[str] = None, 
        year: typing.Optional[int] = None, 
        author_ids: typing.Optional[typing.List[int]] = None
        ) -> Book | None:
        ...

    @strawberry.mutation
    def delete_book(self, id: int) -> Book | None:
        ...
        
    @strawberry.mutation
    def delete_all_books(self) -> None:
        book_data.clear()

    @strawberry.mutation
    def reset_books(self) -> None:
        book_data.clear()
        book_data.extend(book_data_backup)