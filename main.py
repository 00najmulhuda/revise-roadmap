from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Session , select
from database import engine
from models import College, Startups, Founders

app = FastAPI()

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

#founders
@app.post("/founders")
def create_founders(founders: Founders):
    with Session(engine) as session:
        session.add(founders)
        session.commit()
        session.refresh(founders)
    return founders

@app.get("/founders")
def get_founders():
    with Session(engine) as session:
        founders = session.exec(select(Founders)).all()
    return founders

@app.get("/founders/{id}")
def get_founder(id: int):
    with Session(engine) as session:
        founder = session.get(Founders, id)
        if not founder:
            raise HTTPException(status_code = 404, detail = "not found")
    return founder

@app.put("/founders/{id}")
def update_founder(id: int, update_data: Founders):
    with Session(engine) as session:
        founder = session.get(Founders, id)
        if not founder:
            raise HTTPException(status_code = 404, detail = "not found")
        founder.name = update_data.name
        founder.email = update_data.email

        session.commit()
        session.refresh(founder)
    return founder

@app.delete("/founders/{id}")
def delete_founder(id: int):
    with Session(engine) as session:
        founder = session.get(Founders, id)
        if not founder:
            raise HTTPException(status_code = 404, detail = "not found")
        session.delete(founder)
        session.commit()
    
    return {"msg": "deletedd"}




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
        if not college:
            raise HTTPException(status_code = 404, detail = "not found")
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

@app.delete("/colleges/{id}")
def delete_college(id: int):
    with Session(engine) as session:
        college = session.get(College, id)
        session.delete(college)
        session.commit()
    return {"msg":"deleted successfully"}

#startups
@app.post("/startups")
def create_startups(startups: Startups):
    with Session(engine) as session:
        session.add(startups)
        session.commit()
        session.refresh(startups)
    return startups

@app.get("/startups")
def get_startups():
    with Session(engine) as session:
        startups = session.exec(select(Startups)).all()
    return startups

@app.get("/startups/{id}")
def get_startup(id: int):
    with Session(engine) as session:
        startup = session.get(Startups, id)
        if not startup:
            raise HTTPException(status_code = 404, detail = "not found")
        return startup

@app.put("/startups/{id}")
def update_startup(id: int, update_data: Startups):
    with Session(engine) as session:
        startup = session.get(Startups, id)
        if not startup:
            raise HTTPException(status_code = 404, detail = "not found")
        startup.name = update_data.name
        startup.email = update_data.email
        
        session.add(startup)
        session.commit()
        session.refresh(startup)
    return startup

@app.delete("/startups/{id}")
def delete_startup(id: int):
    with Session(engine) as session:
        startup = session.get(Startups, id)
        if not startup:
            raise HTTPException(status_code = 404, detail = "not found")

        session.delete(startup)
        session.commit()
    
    return {"msg": "deleted"}

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


