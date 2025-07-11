from fastapi import Depends, FastAPI
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models import Todo, UserWithPassword
from .database import get_mongo_db, get_supabase  # Importing the database connection function

app = FastAPI()

'''
class Item(BaseModel):
    name: str

@app.post("/items/")
async def create_item(item: Item, supabase=Depends(get_supabase)):
    supabase.table("items").insert({"name": item.name}).execute()
    return {"message": f"Item {item.name} added successfully"}

@app.post("/names")
async def create_name(name: str, mongo_db: AsyncIOMotorDatabase=Depends(get_mongo_db)):
    result = await mongo_db.names.insert_one({"name": name})
    if not result.acknowledged:
        return {"error": "Failed to add name"}
    return {"message": f"Name {name} added successfully", "id": str(result.inserted_id)}
'''
@app.post("/register")
async def register_user(user: UserWithPassword, supabase=Depends(get_supabase)):
    supabase.table("users").insert({
        "name": user.name,
        "password": user.password
    }).execute()
    return {"message": f"User {user.name} registered successfully"}

@app.post("/todo/{user_id}")
async def create_todo(user_id: str, todo: Todo, supabase=Depends(get_supabase)):
    if not user_id:
        return {"error": "User ID must be provided"}
    supabase.table("todos").insert({**todo.dict(), "user_id": user_id}).execute()
    return {"message": f"Todo {todo} added successfully"}

@app.get("/todo/{id}/{user_id}")
async def get_todo(id: str, user_id: str, supabase=Depends(get_supabase)):
    if not id or not user_id:
        return {"error": "ID and User ID must be provided"}
    todo = supabase.table("todos").select("*").eq("id", id).eq("user_id", user_id).execute()
    if not todo:
        return {"error": "Todo not found"}
    return {"todo": todo}

@app.put("/todo/{id}/{user_id}")
async def update_todo(id: str, user_id: str, todo: dict, supabase=Depends(get_supabase)):
    if not id or not user_id:
        return {"error": "ID and User ID must be provided"}
    result = supabase.table("todos").update(todo).eq("id", id).eq("user_id", user_id).execute()
    if not result:
        return {"error": "Failed to update todo"}
    return {"message": f"Todo {id} updated successfully"}

@app.delete("/todo/{id}/{user_id}")
async def delete_todo(id: str, user_id: str, supabase=Depends(get_supabase)):
    if not id or not user_id:
        return {"error": "ID and User ID must be provided"}
    result = supabase.table("todos").delete().eq("id", id).eq("user_id", user_id).execute()
    if not result:
        return {"error": "Failed to delete todo"}
    return {"message": f"Todo {id} deleted successfully"}

@app.delete("/user/{user_id}")
async def delete_user(user_id: str, supabase=Depends(get_supabase)):
    if not user_id:
        return {"error": "User ID must be provided"}
    result = supabase.table("users").delete().eq("id", user_id).execute()
    if supabase.table("todos").delete().eq("user_id", user_id).execute():
        supabase.table("todos").delete().eq("user_id", user_id).execute()
    if not result:
        return {"error": "Failed to delete user"}
    return {"message": f"User {user_id} with todos deleted successfully"}
