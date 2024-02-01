# example.py
from typing import List, TypeVar, Dict, Any, Generic
import strawberry


# user_data = [
#     {
#         "id": 1,
#         "name": "Norman Osborn",
#         "occupation": "Founder, Oscorp Industries",
#         "age": 42,
#     },
#     {
#         "id": 2,
#         "name": "Peter Parker",
#         "occupation": "Freelance Photographer, The Daily Bugle",
#         "age": 20,
#     },
#     {
#         "id": 3,
#         "name": "Harold Osborn",
#         "occupation": "President, Oscorp Industries",
#         "age": 19,
#     },
#     {
#         "id": 4,
#         "name": "Eddie Brock",
#         "occupation": "Journalist, The Eddie Brock Report",
#         "age": 20,
#     },
# ]

user_dict = {
    1: {
        "name": "Norman Osborn",
        "occupation": "Founder, Oscorp Industries",
        "age": 42
    },
    2: {
        "name": "Peter Parker",
        "occupation": "Freelance Photographer, The Daily Bugle",
        "age": 20
    },
    3: {
        "name": "Harold Osborn",
        "occupation": "President, Oscorp Industries",
        "age": 19
    },
    4: {
        "id": 4,
        "name": "Eddie Brock",
        "occupation": "Journalist, The Eddie Brock Report",
        "age": 20
    }
}

@strawberry.type
class User:
    id: int = strawberry.field(description="The id of the user.")
    name: str = strawberry.field(description="The name of the user.")
    occupation: str = strawberry.field(description="The occupation of the user.")
    age: int = strawberry.field(description="The age of the user.")


    @staticmethod
    def from_row(id):
        return User(id=id,name=table[id]["name"], occupation=table[id]["occupation"], age=table[id]["age"])

Item = TypeVar("Item")


@strawberry.type
class PaginationWindow(Generic[Item]):
    items: List[Item] = strawberry.field(
        description="The list of items in this pagination window."
    )


    total_items_count: int = strawberry.field(
        description="Total number of items in the filtered dataset."
    )

@strawberry.type
class Query:
    @strawberry.field(description="Get a list of users.")
    def users(
        self,
        order_by: str,
        limit: int,
        offset: int = 0,
        name: str | None = None,
        occupation: str | None = None,
    ) -> PaginationWindow[User]:
        filters = {}


        if name:
            filters["name"] = name
 
        if occupation:
            filters["occupation"] = occupation
 
        return get_pagination_window(
            dataset=user_dict,
            ItemType=User,
            order_by=order_by,
            limit=limit,
            offset=offset,
            filters=filters,
        )

@strawberry.type
class Mutation:
    @strawberry.field
    def add_user(self, name: str, occupation: str, age: int) -> User:
        new_key = max_key(user_dict) + 1
        user_dict[new_key] = {
            "name": name,
            "occupation": occupation,
            "age": age
        }
        return User.from_row(new_key)
    
    @strawberry.field
    def delete_all() -> None:
        user_dict.clear()


schema = strawberry.Schema(query=Query, mutation=Mutation)



def get_pagination_window(
    dataset: List[Item],
    ItemType: type,
    order_by: str,
    limit: int,
    offset: int = 0,
    filters: dict[str, str] = {},
) -> PaginationWindow:
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


    return PaginationWindow(items=items, total_items_count=total_items_count)




def matches(item, filters):
    """
    Test whether the item matches the given filters.
    This demo only supports filtering by string fields.
    """


    for attr_name, val in filters.items():
        if val not in item[attr_name]:
            return False
    return True