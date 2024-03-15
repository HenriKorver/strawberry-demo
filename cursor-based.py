# example.py


from base64 import b64encode, b64decode
from typing import List, Optional, Dict, Any, cast


import strawberry
 
user_data = [
    {
        "id": 1,
        "name": "Norman Osborn",
        "occupation": "Founder, Oscorp Industries",
        "age": 42,
    },
    {
        "id": 2,
        "name": "Peter Parker",
        "occupation": "Freelance Photographer, The Daily Bugle",
        "age": 20,
    },
    {
        "id": 3,
        "name": "Harold Osborn",
        "occupation": "President, Oscorp Industries",
        "age": 19,
    },
    {
        "id": 4,
        "name": "Eddie Brock",
        "occupation": "Journalist, The Eddie Brock Report",
        "age": 20,
    },
]




def encode_user_cursor(id: int) -> str:
    """
    Encodes the given user ID into a cursor.

    :param id: The user ID to encode.

    :return: The encoded cursor.
    """
    return b64encode(f"user:{id}".encode("ascii")).decode("ascii")




def decode_user_cursor(cursor: str) -> int:
    """
    Decodes the user ID from the given cursor.

    :param cursor: The cursor to decode.

    :return: The decoded user ID.
    """
    cursor_data = b64decode(cursor.encode("ascii")).decode("ascii")
    return int(cursor_data.split(":")[1])




@strawberry.type
class User:
    id: str = strawberry.field(description="ID of the user.")


    name: str = strawberry.field(description="The name of the user.")


    occupation: str = strawberry.field(description="The occupation of the user.")


    age: int = strawberry.field(description="The age of the user.")


    @staticmethod
    def from_row(row: Dict[str, Any]) -> "User":
        return User(
            id=row["id"], name=row["name"], occupation=row["occupation"], age=row["age"]
        )




@strawberry.type
class PageMeta:
    next_cursor: Optional[str] = strawberry.field(
        description="The next cursor to continue with."
    )




@strawberry.type
class UserResponse:
    users: List[User] = strawberry.field(description="The list of users.")


    page_meta: PageMeta = strawberry.field(description="Metadata to aid in pagination.")




@strawberry.type
class Query:
    @strawberry.field(description="Get a list of users.")
    def get_users(self, limit: int, cursor: Optional[str] = None) -> UserResponse:
        if cursor is not None:
            # decode the user ID from the given cursor.
            user_id = decode_user_cursor(cursor=cursor)
        else:
            # no cursor was given (this happens usually when the
            # client sends a query for the first time).
            user_id = 0


        # filter the user data, going through the next set of results.
        filtered_data = [user for user in user_data if user["id"] >= user_id]


        # slice the relevant user data (Here, we also slice an
        # additional user instance, to prepare the next cursor).
        sliced_users = filtered_data[: limit + 1]


        if len(sliced_users) > limit:
            # calculate the client's next cursor.
            last_user = sliced_users.pop(-1)
            next_cursor = encode_user_cursor(id=last_user["id"])
        else:
            # We have reached the last page, and
            # don't have the next cursor.
            next_cursor = None


        sliced_users = [User.from_row(x) for x in sliced_users]


        return UserResponse(
            users=sliced_users, page_meta=PageMeta(next_cursor=next_cursor)
        )




schema = strawberry.Schema(query=Query)