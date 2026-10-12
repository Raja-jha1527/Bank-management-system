from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import List
app = FastAPI()

class Book(BaseModel):
    Name:str
    page:int
    year:int

books = []
@app.post("/item",response_model=Book)
async def items(book:Book):
    books.append(book)
    return book
@app.get("/item",response_model=List[Book])
async def get():
    return books