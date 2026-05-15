from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    UploadFile,
    File,
    Request
)

from fastapi.middleware.cors import CORSMiddleware

from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm
)

from sqlalchemy.orm import Session

import models
import schemas

from database import (
    engine,
    SessionLocal
)

from auth import (
    hash_password,
    verify_password,
    create_access_token,
    verify_token
)

import shutil
import os
import random

# CREATE TABLES
models.Base.metadata.create_all(bind=engine)

# FASTAPI APP
app = FastAPI()

# ==============================
# CORS MIDDLEWARE
# ==============================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================
# OAUTH2
# ==============================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)

# ==============================
# DATABASE DEPENDENCY
# ==============================

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

# ==============================
# REQUEST LOGGER MIDDLEWARE
# ==============================

@app.middleware("http")
async def log_requests(
    request: Request,
    call_next
):

    print(f"Request URL: {request.url}")

    response = await call_next(request)

    print(
        f"Response Status: {response.status_code}"
    )

    return response

# ==============================
# HOME API
# ==============================

@app.get("/")
async def home():

    return {
        "message": "MemeVerse API Running 🚀"
    }

# ==============================
# SIGNUP API
# ==============================

@app.post("/signup")
async def signup(
    user: schemas.SignupSchema,
    db: Session = Depends(get_db)
):

    existing_user = db.query(
        models.User
    ).filter(
        models.User.email == user.email
    ).first()

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    hashed_password = hash_password(
        user.password
    )

    new_user = models.User(
        name=user.name,
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return {
        "message": "User registered successfully"
    }

# ==============================
# LOGIN API
# ==============================

@app.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    db_user = db.query(
        models.User
    ).filter(
        models.User.email == form_data.username
    ).first()

    if not db_user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not verify_password(
        form_data.password,
        db_user.password
    ):

        raise HTTPException(
            status_code=401,
            detail="Incorrect password"
        )

    token = create_access_token(
        data={"sub": db_user.email}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

# ==============================
# PROTECTED PROFILE API
# ==============================

@app.get("/profile")
async def profile(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    email = verify_token(token)

    if email is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user = db.query(
        models.User
    ).filter(
        models.User.email == email
    ).first()

    return {
        "name": user.name,
        "email": user.email
    }

# ==============================
# ADD JOKE API
# ==============================

@app.post("/add-joke")
async def add_joke(
    joke: schemas.JokeSchema,
    db: Session = Depends(get_db)
):

    new_joke = models.Joke(
        content=joke.content
    )

    db.add(new_joke)

    db.commit()

    db.refresh(new_joke)

    return {
        "message": "Joke added successfully 😂"
    }

# ==============================
# GET ALL JOKES API
# ==============================

@app.get("/jokes")
async def get_jokes(
    db: Session = Depends(get_db)
):

    jokes = db.query(
        models.Joke
    ).all()

    return jokes

# ==============================
# RANDOM JOKE API
# ==============================

@app.get("/random-joke")
async def random_joke(
    db: Session = Depends(get_db)
):

    jokes = db.query(
        models.Joke
    ).all()

    if not jokes:

        return {
            "message": "No jokes available"
        }

    joke = random.choice(jokes)

    return {
        "joke": joke.content
    }

# ==============================
# FILE UPLOAD API
# ==============================

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...)
):

    os.makedirs(
        "uploads",
        exist_ok=True
    )

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    return {
        "filename": file.filename,
        "message": "File uploaded successfully"
    }

# ==============================
# ASYNC API
# ==============================

@app.get("/async-api")
async def async_api():

    return {
        "message": "This is async API ⚡"
    }