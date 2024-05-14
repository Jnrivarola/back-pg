from fastapi import FastAPI, HTTPException
from model.user_connection import UserConnection
from schema.user_schema import UserSchema
from schema.book_schema import BookSchema



app = FastAPI()
conn = UserConnection()

@app.get("/")
def root():
    items = conn.read_all()
    return items

@app.get("/api/usuarios/{id}")
def get_one(id: str):
    user = conn.read_one(id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@app.post("/api/insert")
def insert(user_data: UserSchema):
    data = user_data.dict()
    conn.write(data)

@app.put("/api/update/{id}")
def update(id: str, user_data: UserSchema):
    data = user_data.dict()
    data["id"] = id
    conn.update(data)

@app.delete("/api/delete/{id}")
def delete(id: str):
    conn.delete(id)

@app.get("/api/libros")
def get_all_books():
    books = conn.read_all_books()
    return books

@app.get("/api/libros/{id}")
def get_one_book(id: str):
    book = conn.read_one_book(id)
    if not book:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return book

@app.post("/api/libros")
def create_book(book_data: BookSchema):
    data = book_data.dict()
    conn.write_book(data)

@app.put("/api/libros/{id}")
def update_book(id: str, book_data: BookSchema):
    data = book_data.dict()
    data["id"] = id
    conn.update_book(data)

@app.delete("/api/libros/{id}")
def delete_book(id: str):
    conn.delete_book(id)
