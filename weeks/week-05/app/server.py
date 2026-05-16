from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
import strawberry
from typing import List, Optional
from datetime import datetime
from uuid import uuid4

items_db = {}

@strawberry.type
class Item:
    id: strawberry.ID
    name: str
    sku: str
    price: float
    quantity: int
    created_at: str

@strawberry.input
class CreateItemInput:
    name: str
    sku: str
    price: float
    quantity: int

@strawberry.type
class Query:
    @strawberry.field
    async def items(self) -> List[Item]:
        """Получение списка всех items"""
        return list(items_db.values())
    
    @strawberry.field
    async def item(self, id: strawberry.ID) -> Optional[Item]:
        """Получение одного item по ID"""
        return items_db.get(str(id))

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_item(self, input: CreateItemInput) -> Item:
        """Создание нового item"""
        item_id = str(uuid4())
        new_item = Item(
            id=strawberry.ID(item_id),
            name=input.name,
            sku=input.sku,
            price=input.price,
            quantity=input.quantity,
            created_at=datetime.now().isoformat()
        )
        items_db[item_id] = new_item
        return new_item

schema = strawberry.Schema(query=Query, mutation=Mutation)

app = FastAPI(title="Items Service S01", version="1.0.0")

graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

@app.get("/api/items")
async def get_items():
    return {"items": list(items_db.values())}

@app.get("/")
async def root():
    return {
        "service": "items-svc-s01",
        "group": "332",
        "student_id": "s01",
        "week": "05",
        "graphql_endpoint": "/graphql",
        "rest_endpoint": "/api/items"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8101)