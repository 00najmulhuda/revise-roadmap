from sqlmodel import SQLModel

#response model INPUT model------------------------------------------
class RegisterUser(SQLModel):
    username : str
    email : str
    password : str


#Login request response model-- login input model-----------------------------
class LoginUser(SQLModel):
    email : str
    password : str