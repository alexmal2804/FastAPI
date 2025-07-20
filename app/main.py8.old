from fastapi import Depends, FastAPI
from pydantic import BaseModel

from .database import supabase  # Importing the database connection function


app = FastAPI()


class Item(BaseModel):
    name: str


print(supabase)


@app.post("/items/")
async def create_item(item: Item):
    supabase.table("items").insert({"name": item.name}).execute()
    return {"message": f"Item {item.name} added successfully"}
