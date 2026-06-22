from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

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
    return payload.get("user_id")