from sqlmodel import SQLModel, Field, Relationship
from typing import List


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

class FounderCreate(SQLModel):
    name: str
    email:str

class FounderRead(SQLModel):
    id : int
    name : str
    email : str

class Teacher(SQLModel, table = True):
    id : int | None = Field(default = None, primary_key = True)
    name : str

    students : List["Student"] = Relationship(
        back_populates = "teacher"
    )



class Enrollment(SQLModel, table = True):
    student_id : int = Field(
        foreign_key = "student.id",
        primary_key = True
    )

    course_id : int = Field(
        foreign_key = "course.id",
        primary_key = True
    )


class Student(SQLModel, table = True):
    id : int | None = Field(default = None, primary_key = True)
    name : str

    teacher_id : int = Field(
        foreign_key = "teacher.id"
    )

    teacher : "Teacher" = Relationship(
        back_populates = "students"
    )
    courses : List["Course"] = Relationship(
        back_populates = "students",
        link_model = Enrollment
    )



class Course(SQLModel, table = True):
    id : int | None = Field(default = None, primary_key = True)
    course_name : str
    
    students : List["Student"] = Relationship(
        back_populates = "courses",
        link_model = Enrollment
    )


#MentorSkill class
class MentorSkill(SQLModel, table = True):
    mentor_id : int = Field(
        foreign_key = "mentor.id",
        primary_key = True
    )

    skill_id : int = Field(
        foreign_key = "skill.id",
        primary_key = True
    )

#mentor class 
class Mentor(SQLModel, table = True):
    id : int | None = Field(default = None, primary_key = True)
    mentor_name : str

    skills : List["Skill"] = Relationship(
        back_populates = "mentors",
        link_model = MentorSkill
    )

class Skill(SQLModel, table = True):
    id : int | None = Field(default = None, primary_key = True)
    skill_name : str

    mentors : List["Mentor"] = Relationship(
        back_populates = "skills",
        link_model = MentorSkill
    )


#Company - employee classes - ------------------------------------------------
class Library(SQLModel, table = True):
    id: int | None = Field(default = None, primary_key = True)
    name : str

    books : List["Book"] = Relationship(
        back_populates = "library"
    )
    
    

class Book(SQLModel, table = True):
    id: int | None = Field(default = None, primary_key = True)
    name : str

    library_id : int = Field(
        foreign_key = "library.id"
    )

    library : "Library" = Relationship(
        back_populates = "books"
    )

    library_id : int = Field(
        foreign_key = "library.id"
    )

#response_model
class LibraryCreate(SQLModel):
    name : str
    

class LibraryRead(SQLModel):
    id : int
    name : str
    

class BookCreate(SQLModel):
    name : str
    library_id : int

class BookRead(SQLModel):
    id : int
    name : str
    library_id : int


#account-------------------------------------------------------------------------
class Account(SQLModel, table = True):
    id : int | None = Field(default = None, primary_key = True)
    email : str
    password : str

#Account response_model-------
class AccountCreate(SQLModel):
    email : str
    password : str

#potput model
class AccountRead(SQLModel):
    id : int 
    email : str

#Login request model
class LoginRequest(SQLModel):
    email : str
    password : str