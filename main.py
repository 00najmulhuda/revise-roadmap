from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, Session , select
from database import engine
from models import College, Startups, Founders, FounderCreate, FounderRead, Teacher, Student,Course, Enrollment, Mentor, Skill, MentorSkill, Library, Book, LibraryCreate, LibraryRead , Account, AccountRead, AccountCreate ,LoginRequest
from auth import hash_password , create_access_token, verify_password, verify_token, get_current_user, require_role
from fastapi.security import OAuth2PasswordBearer
from auth_routes import router as auth_router
from auth_models import NewUser



app = FastAPI()

app.include_router(auth_router)#means FAstAPI please include all routes from auth_routes.py without this main.py not consider auth_routes.py routes

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

oauth2_schemes = OAuth2PasswordBearer(
    tokenUrl = "login"
)

#account Signup route -------------------------------------------------------
@app.post("/signup", response_model = AccountRead, status_code = 201)
def signup(account : AccountCreate):
    hashed_password = hash_password(
        account.password
    )

    new_account = Account(
        email = account.email,
        password = hashed_password
    )
    with Session(engine) as session:
        session.add(new_account)
        session.commit()
        session.refresh(new_account)
        return new_account

#login route---------------------------------------------------
@app.post("/login")
def login(data : LoginRequest):
    with Session(engine) as session:
        account = session.exec(
            select(Account)
            .where(Account.email == data.email)
        ).first()
        if not account:
            raise HTTPException(
                status_code = 404, detail = "not found email"
            )
        if not verify_password(
            data.password,
            account.password
        ):
            raise HTTPException(
                status_code = 404,
                detail = "Invalid"
            )

        acceess_token = create_access_token(
            {
                "user_id" : account.id,
                "email" : account.email
            }
        )
        return {
            "access_token" : acceess_token
        }

#Profile protected route------------------------------------------------
@app.get("/profile")
def get_profile(token : Str = Depends(oauth2_schemes)):
    
    payload = verify_token(token)

    return payload
#library------------------------------------------------------------------

#mentor-----------------------------------------------------------------
@app.post("/mentors")
def create_mentor(mentor : Mentor):
    with Session(engine) as session:
        session.add(mentor)
        session.commit()
        session.refresh(mentor)

        return mentor

@app.get("/mentors")
def get_mentors():
    with Session(engine) as session:
        mentors = session.exec(
            select(Mentor)
        ).all()

        if not mentors:
            raise HTTPException(
                status_code = 404, 
                detail = "not found mentors"
            )
        return mentors

@app.get("/mentors/{mentor_id}")
def get_mentor(mentor_id : int):
    with Session(engine) as session:
        mentor = session.get(Mentor, mentor_id)
        if not mentor:
            raise HTTPException(
                status_code = 404, 
                detail = "mentor not found"
            )
        return mentor

@app.get("/mentors/{mentor_id}/skills")
def get_mentor_skills(mentor_id : int):
    with Session(engine) as session:
        mentor = session.get(Mentor, mentor_id)
        if not mentor:
            raise HTTPException(
                status_code = 404,
                detail = "mentor skills not found"
            )
        return mentor.skills
#Skill-----------------------------------------------------------------
@app.post("/skills")
def create_skill(skill : Skill):
    with Session(engine) as session:
        session.add(skill)
        session.commit()
        session.refresh(skill)
        return skill

@app.get("/skills")
def get_skills():
    with Session(engine) as session:
        skills = session.exec(
            select(Skill)
        ).all()
        if not skills:
            raise HTTPException(
                status_code = 404,
                detail = "skills not found"
            )
        return skills

@app.get("/skills/{skill_id}")
def get_skill(skill_id : int):
    with Session(engine) as session:
        skill = session.get(Skill, skill_id)
        if not skill:
            raise HTTPException(
               status_code = 404,
               detail = "skill not found"
            )
        return skill

@app.get("/skills/{skill_id}/mentors")
def get_skill_mentors(skill_id : int):
    with Session(engine) as session:
        skill = session.get(Skill, skill_id)
        if not skill:
            raise HTTPException(
                status_code = 404, 
                detail = "this skill mentors not found"
            )
        return skill.mentors
#MentorSkill-----------------------------------------------------------
@app.post("/mentorskills")
def create_mentor_skill(mentorskill : MentorSkill):
    with Session(engine) as session:
        session.add(mentorskill)
        session.commit()
        session.refresh(mentorskill)
        return mentorskill

@app.get("/mentorskills")
def get_mentor_skills():
    with Session(engine) as session:
        mentorskill = session.exec(
            select(MentorSkill)
        ).all()
        if not mentorskill:
            raise HTTPException(
                status_code = 404,
                detail = "nemtorskill not found"
            )
        return mentorskill
#teachers-----------------------------------------------------------------
@app.post("/teachers")
def create_teacher(teacher: Teacher):
    with Session(engine) as session:
        session.add(teacher)
        session.commit()
        session.refresh(teacher)
    return teacher

@app.get("/teacher")
def get_teachers():
    with Session(engine) as session:
        teachers = session.exec(
            select(Teacher)
        ).all
    return teachers

@app.get("/teachers/{teacher_id}")
def get_teacher(teacher_id: int):
    with Session(engine) as session:
        teacher = session.get(Teacher, teacher_id)
        if not teacher:
            raise HTTPException(status_code = 404, detail = "not found")
    return teacher

@app.get("/teachers/{teacher_id}/students")
def get_teacher_student(teacher_id : int):
    with Session(engine) as session:
        teacher = session.get(Teacher, teacher_id)

        if not teacher:
            raise HTTPException(
                status_code = 404,
                detail = "not found this teacher students"
            )
        return teacher.students


#students -  ------------------------------------------------------
@app.post("/students")
def create_student(student: Student):
    with Session(engine) as session:
        session.add(student)
        session.commit()
        session.refresh(student)
    return student


@app.get("/students")
def get_students():
    with Session(engine) as session:
        students = session.exec(
            select(Student)
        ).all()

    return students

@app.get("/students/{student_id}")
def get_student(student_id : int):
    with Session(engine) as session:
        student = session.get(Student, student_id)
        if not student:
            raise HTTPException(status_code = 404, detail = "Not found Student")
    return student

@app.get("/students/{student_id}/teachers")
def get_student_teacher(student_id : int):
    with Session(engine) as session:
        student = session.get(Student, student_id)
        if not student:
            raise HTTPException(status_code = 404, detail = "this student id not found")
        return student.teacher

@app.get("/students/{student_id}/courses")
def get_student_courses(student_id : int):
    with Session(engine) as session:
        student = session.get(Student, student_id)

        if not student:
            raise HTTPException(
                status_code = 404,
                detail = "student not found"
            )

        return student.courses


#course ----------------------------------------------------------------
@app.post("/courses")
def create_course(course : Course):
    with Session(engine) as session:
        session.add(course)
        session.commit()
        session.refresh(course)

        return course

@app.get("/courses")
def get_course():
    with Session(engine) as session:
        courses = session.exec(select(Course)).all()
        if not courses:
            raise HTTPException(
                status_code = 404, 
                detail = "not found course"
            )
        return courses

@app.get("/courses/{course_id}/students")
def get_course_students(course_id : int):
    with Session(engine) as session:
        course = session.get(Course, course_id)
        
        if not course:
            raise HTTPException(
                status_code = 404,
                detail = "not found students of this course"
            )
        return course.students
#enrollment----------------------------------------------------------------
@app.post("/enrollments")
def create_enrollment(enrollment : Enrollment):
    with Session(engine) as session:
        session.add(enrollment)
        session.commit()
        session.refresh(enrollment)
        return enrollment

@app.get("/enrollments")
def get_enrollments():
    with Session(engine) as session:
        enrollments = session.exec(select(Enrollment)).all()
        if not enrollments:
            raise HTTPException(
                status_code = 404,
                detail = "not found enroll"
            )
        return enrollments


#founders-------------------------------------------------------------------------------
@app.post("/founders", response_model = FounderRead, status_code = 201)
def create_founder(data: FounderCreate):
    with Session(engine) as session:
        founder = Founders(**data.dict())
        session.add(founder)
        session.commit()
        session.refresh(founder)
    return founder

@app.get("/founders", response_model = list[FounderRead])
def get_founders():
    with Session(engine) as session:
        founders = session.exec(select(Founders)).all()
    return founders

@app.get("/founders/{id}", response_model = FounderRead)
def get_founder(id: int):
    with Session(engine) as session:
        founder = session.get(Founders, id)
        if not founder:
            raise HTTPException(status_code = 404, detail = "not found")
    return founder

@app.put("/founders/{id}", response_model = FounderRead)
def update_founder(id: int, update_data: FounderCreate):
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
def delete_founder(id: int, current_user : NewUser = Depends(require_role("admin"))):
    with Session(engine) as session:
        founder = session.get(Founders, id)
        if not founder:
            raise HTTPException(status_code = 404, detail = "not found")
        session.delete(founder)
        session.commit()
    
    return {"msg": "deletedd by admin"}


#colleges ----------------------------------------------------------------

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

#startups-----------------------------------------------------------------
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




#learning route ------------------------------------------------------------------
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


