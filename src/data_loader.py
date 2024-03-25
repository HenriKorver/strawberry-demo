from typing import List
 
from strawberry.dataloader import DataLoader
import strawberry
 
 
@strawberry.type
class User:
    id: strawberry.ID
 
 
async def load_users(keys) -> List[User]:
    print(f"getUser({keys})")
    return [User(id=key) for key in keys]
 
 
loader = DataLoader(load_fn=load_users)
 
 
@strawberry.type
class Query:
    @strawberry.field
    async def get_user(self, id: strawberry.ID) -> User:
        print(f"getUser({id})")
        return await loader.load(id)
 
 
schema = strawberry.Schema(query=Query)
