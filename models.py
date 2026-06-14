from sqlmodel import SQLModel, Field

class College(SQLModel, table = True):
    id : int | None = Field(default = None, primary_key = True) #in DB - id is primary key
    name : str  #in db column 
    email : str  #in db column

class Startups(SQLModel, table = True):
    id : int | None = Field(default = None, primary_key = True)
    name : str 
    email : str

class Founders(SQLModel, table = True):
    id : int | None = Field(default = None, primary_key = True)
    name : str
    email : str