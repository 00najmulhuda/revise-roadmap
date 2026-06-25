from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from database import engine
from auth_models import NewUser

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl = "/auth/login"
)

#tool of hashed password and verify password
pwd_context = CryptContext(
    schemes = ["bcrypt"],
    deprecated = "auto"
)

def hash_password(password : str):
    return pwd_context.hash(password)

def verify_password(
    plain_password : str,
    hashed_password : str
    ):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )

SECRET_KEY = "mysecretkey123"
ALGORITHM = "HS256"

def create_access_token(data : dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes = 30)

    to_encode.update(
        {"exp" : expire}
    )

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm = ALGORITHM
    )
    return encoded_jwt

def verify_token(token : str):
    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms = [ALGORITHM]
    )
    user_id = payload.get("user_id")
    role = payload.get("role")
    email = payload.get("email")

    if user_id is None:
        raise HTTPException(status_code = 401, detail = "invalid token")

    return {
        "user_id" : user_id,
        "email" : email,
        "role" : role
    }


def get_current_user(
    token : str = Depends(oauth2_scheme)
):
    token_data = verify_token(token)
    user_id = token_data["user_id"]

    with Session(engine) as session:
        db_user = session.exec(
            select(NewUser)
            .where(NewUser.id == int(user_id))
        ).first()

        if not db_user:
            raise HTTPException(status_code = 401, detail = "user not found")

        return db_user

def require_role(require_role : str):
    def role_checker(current_user : NewUser = Depends(get_current_user)):
        if current_user.role != require_role:
            raise HTTPException(status_code = 403, detail = "Access Denied")
        
        return current_user

    return role_checker

