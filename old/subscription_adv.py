import asyncio
from typing import AsyncGenerator


import strawberry
from strawberry.types import Info

from .auth import authenticate_token



@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "world"




@strawberry.type
class Subscription:
    @strawberry.subscription
    async def count(self, info: Info, target: int = 100) -> AsyncGenerator[int, None]:
        connection_params: dict = info.context.get("connection_params")
        token: str = connection_params.get("authToken")  
        # equal to "Bearer I_AM_A_VALID_AUTH_TOKEN"
        if not authenticate_token(token):
            raise Exception("Forbidden!")
        for i in range(target):
            yield i
            await asyncio.sleep(0.5)




schema = strawberry.Schema(query=Query, subscription=Subscription)