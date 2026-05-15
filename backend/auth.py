from jose import jwt
from jose import JWTError

SECRET_KEY = "MEMEVERSE_SECRET"

ALGORITHM = "HS256"

def create_token(data: dict):

    token = jwt.encode(
        data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token

def verify_token(token: str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:

        return None