'''
source virtualenv/Scripts/activate (in git bash)
strawberry server books
http://127.0.0.1:8000/graphql
strawberry export-schema books5:schema > books5_schema.graphql
'''

'''
To do:
- Paginering
- addAuthor operatie toevoegen
- publish date en geboortedatum toevoegen
- expand mechanisme uitwerken (in graphql is dotnotatie niet nodig)
'''

'''
query = """
        query Authors {
            authors (orderBy: "id") {
                name
                books {
                    title
                }
            }
        }
    """

result = schema.execute_sync(
        query)

print(result.errors)

print(result.data)

q = Query()
q.authors()
'''