from fastapi import APIRouter, HTTPException, Depends 
from sqlmodel import Session , select

from database import engine
from auth_models import NewUser
from auth_schemas import RegisterUser, LoginUser
from auth import hash_password, verify_password, create_access_token, verify_token, get_current_user, require_role,oauth2_scheme






router = APIRouter(
    prefix = "/auth",
    tags = ["Authentication"]
)

@router.post("/register")
def register_user(user : RegisterUser):
    with Session(engine) as session:
        check_email = session.exec(
            select(NewUser)
            .where(NewUser.email == user.email)
        ).first()
        
        hashed_pw = hash_password(user.password)

        db_user = NewUser(
            username = user.username,
            email = user.email,
            hashed_password = hashed_pw 
        )

        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        return {
            "Message" : " NewUser Registered successfully"
        }


@router.post("/login")
def user_login(user : LoginUser):
    with Session(engine) as session:
        check_email = session.exec(
                select(NewUser)
                .where(NewUser.email == user.email)
        ).first()
        if not check_email:
                raise HTTPException(status_code = 401, detail = "invalid email or password")

        if not verify_password(
                user.password,
                check_email.hashed_password
        ):
           raise HTTPException(status_code = 401, detail = "invalid email or password")

        access_token = create_access_token(
                {
                    "user_id" : check_email.id,
                    "email" : check_email.email,
                    "role" : check_email.role
                }
        )
        return {
                "access_token": access_token,
                "token_type" : "Bearer"
            }

@router.get("/profile")
def get_user_profile(token : str = Depends(oauth2_scheme)):
    user_id = verify_token(token)

    return {
        "message" : "Protected route access granted",
        "user_id" : user_id
    }


@router.get("/me")
def get_me(current_user = Depends(get_current_user)):
    return {
        "id" : current_user.id,
        "username" : current_user.username,
        "email" : current_user.email,
        "role" : current_user.role
    }

@router.get("/admin")
def admin_dashboard(current_user : NewUser = Depends(require_role("admin"))):
    return {
        "message" : "welcome admin",
        "user" : current_user.username
    }