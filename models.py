from sqlmodel import SQLModel, Field

class College(SQLModel, table = True):
    id : int | None = Field(default = None, primary_key = True) #in DB - id is primary key
    name : str  #in db column 
    email : str  #in db column

class Company(SQLModel, table = True):
    id : int | None = Field(default = None, primary_key = True)#in DB - id is primary_key
    name :str #in DB column
    email : str #in DB column