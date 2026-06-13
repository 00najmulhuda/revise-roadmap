from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Session , select
from database import engine
from models import College, Company

app = FastAPI()

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


@app.post("/colleges")
def create_college(college: College):
    with Session(engine) as session:
        session.add(college)
        session.commit()
        session.refresh(college)
    return college

@app.get("/colleges")
def get_colleges():
    with Session(engine) as session:
        colleges = session.exec(select(College)).all()
    return colleges

@app.put("/colleges/{id}")
def update_college(id: int, update_data: College):
    with Session(engine) as session:
        college = session.get(College, id)
        college.name = update_data.name
        college.email = update_data.email
        session.commit()
        session.refresh(college)
    return college


#college GET by ID
@app.get("/colleges/{id}")
def get_college(id:int):
    with Session(engine) as session:
        college = session.get(College, id)
        if not college:
            raise HTTPException(status_code = 404, detail = "college not found")
    return college


# @app.post("/company")
# def create_company():
#     with Session(engine) as session:
#         company 




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


