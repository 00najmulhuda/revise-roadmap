from sqlmodel import SQLModel
from pydantic import Field, EmailStr

#response model INPUT model------------------------------------------
class RegisterUser(SQLModel):
    username : str = Field(min_length = 3, max_length = 30, pattern = r"^[a-zA-Z0-9_]+$")
    email : EmailStr
    password : str = Field(min_length = 8, max_length = 24)


#Login request response model-- login input model-----------------------------
class LoginUser(SQLModel):
    email : EmailStr
    password : str = Field(min_length = 8, max_length = 24)