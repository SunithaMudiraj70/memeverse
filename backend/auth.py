from jose import jwt, JWTError
from datetime import datetime, timedelta
from passlib.context import CryptContext

# SECRET KEY
SECRET_KEY = "1a114d4ef444dffd4ca39fc87576e2d5989c4a52a16b76de5ac60d5073317c67"

# ALGORITHM
ALGORITHM = "HS256"

# TOKEN EXPIRY
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# PASSWORD HASHING
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# HASH PASSWORD
def hash_password(password: str):

    return pwd_context.hash(password)

# VERIFY PASSWORD
def verify_password(
    plain_password,
    hashed_password
):

    return pwd_context.verify(
        plain_password,
        hashed_password
    )

# CREATE ACCESS TOKEN
def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt

# VERIFY TOKEN
def verify_token(token: str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")

        return email

    except JWTError:

        return None
