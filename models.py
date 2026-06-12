from sqlmodl import SQLModel, Field

class college(SQLModel, table = True):
    id : int | None = Field(default = None, primary_key = True) #in DB - id is primary key
    name : str  #in db column 
    email : str  #in db column

