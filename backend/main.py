from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    UploadFile,
    File
)

from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

import os
import shutil
import random

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

# ==========================================
# CREATE DATABASE TABLES
# ==========================================

models.Base.metadata.create_all(bind=engine)

# ==========================================
# FASTAPI APP
# ==========================================

app = FastAPI()

# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# DATABASE DEPENDENCY
# ==========================================

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()

# ==========================================
# HOME API
# ==========================================

@app.get("/")
async def home():

    return {
        "message": "😂 MemeVerse Backend Running Successfully"
    }

# ==========================================
# SIGNUP API
# ==========================================

@app.post("/signup")
async def signup(
    user: schemas.UserSignup,
    db: Session = Depends(get_db)
):

    existing_user = db.query(
        models.User
    ).filter(
        models.User.username == user.username
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
        username=user.username,
        password=hashed_password
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return {
        "message": "User registered successfully"
    }

# ==========================================
# LOGIN API
# ==========================================

@app.post("/login")
async def login(
    user: schemas.UserLogin,
    db: Session = Depends(get_db)
):

    db_user = db.query(
        models.User
    ).filter(
        models.User.username == user.username
    ).first()

    if not db_user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not verify_password(
        user.password,
        db_user.password
    ):

        raise HTTPException(
            status_code=401,
            detail="Incorrect password"
        )

    token = create_access_token(
        data={"sub": db_user.username}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

# ==========================================
# PROTECTED PROFILE API
# ==========================================

@app.get("/profile")
async def profile(token: str):

    username = verify_token(token)

    if username is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    return {
        "username": username,
        "message": "Protected profile accessed"
    }

# ==========================================
# POST JOKE API
# ==========================================

@app.post("/add-joke")
async def add_joke(
    joke: schemas.JokeCreate,
    db: Session = Depends(get_db)
):

    new_joke = models.Joke(
        joke=joke.joke
    )

    db.add(new_joke)

    db.commit()

    db.refresh(new_joke)

    return {
        "message": "Joke added successfully"
    }

# ==========================================
# GET ALL JOKES API
# ==========================================

@app.get("/get-jokes")
async def get_jokes(
    db: Session = Depends(get_db)
):

    jokes = db.query(
        models.Joke
    ).all()

    return jokes

# ==========================================
# RANDOM AI STYLE JOKE API
# ==========================================

@app.get("/generate-joke")
async def generate_joke():

    jokes = [

        "Why don’t programmers like nature? It has too many bugs 😂",

        "Why did the computer go to therapy? It had too many bytes of trauma 🤖",

        "Why was the Python developer calm? Because he handled exceptions properly 😎",

        "Why do Java developers wear glasses? Because they don’t C# 🤣",

        "Why was the AI model so confident? Because it had deep learning 😁",

        "Why did the database break up? Too many relationships 💔",

        "Why did the backend developer cry? Frontend changed the API again 😭"

    ]

    return {
        "joke": random.choice(jokes)
    }

# ==========================================
# FILE UPLOAD API
# ==========================================

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

# ==========================================
# VIEW UPLOADED FILES API
# ==========================================

@app.get("/files")
async def get_files():

    os.makedirs(
        "uploads",
        exist_ok=True
    )

    files = os.listdir("uploads")

    return {
        "files": files
    }

# ==========================================
# ASYNC API
# ==========================================

@app.get("/async-api")
async def async_api():

    return {
        "message": "⚡ Async API is working successfully"
    }
