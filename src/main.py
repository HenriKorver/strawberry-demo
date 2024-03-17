import strawberry
from query import Query
from mutation import Mutation

schema = strawberry.Schema(query=Query, mutation=Mutation)

# q = Query()
# result = q.books(limit=10, order_by="title")

# pass