import strawberry
from aiohttp import web
from strawberry.aiohttp.views import GraphQLView
from strawberry.aiohttp import web




@strawberry.type
class Query:
    @strawberry.field
    def hello(self, name: str = "World") -> str:
        return f"Hello, {name}!"




schema = strawberry.Schema(query=Query)


app = web.



app.router.add_route("*", "/graphql", GraphQLView(schema=schema))