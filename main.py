from fastapi import FastAPI

app = FastAPI()
@app.get("/")
def greet():
    return{"msg":"Hello Najmul!"}

@app.get("/about")
def abouut_me():
    return{"msg":"I am Najmul Huda a student of BTECH CSE at S.I.E.T"}

@app.post("/my-info")
def my_info():
    return{"msg":"I am a AI Fullstack developer"}

@app.put("/update-info")
def update_info():
    return{"msg":"I am AI fullstack developer - FastAPI,PostgreSQL,Python"}

@app.delete("/delete-info")
def delete_info():
    return{"msg":"I deleted my info"}

@app.get("/users/{user_id}")
def get_user(user_id: int, page: int = 1):
    return{"msg": f"user_id: {user_id}, page: {page}"}

@app.get("/products/{product_id}")
def get_product(product_id: int, page: int = 1, limit: int = 10):
    return{"msg": f"product_id: {product_id}, page: {page}, limit: {limit}"}


