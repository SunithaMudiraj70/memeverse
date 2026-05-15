from fastapi import FastAPI
from fastapi import Depends
from fastapi import HTTPException
from fastapi import UploadFile
from fastapi import File

from sqlalchemy.orm import Session

import models
import schemas

from database import (
    engine,
    SessionLocal
)

from auth import (
    create_token,
    verify_token
)

import shutil
import random
import os

# =========================
# CREATE DATABASE
# =========================

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# =========================
# DATABASE DEPENDENCY
# =========================

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

# =========================
# HOME API
# =========================

@app.get("/")
def home():

    return {
        "message": "😂 Welcome to MemeVerse"
    }

# =========================
# SIGNUP
# =========================

@app.post("/signup")
def signup(
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

    new_user = models.User(
        username=user.username,
        password=user.password
    )

    db.add(new_user)

    db.commit()

    return {
        "message": "User created successfully"
    }

# =========================
# LOGIN
# =========================

@app.post("/login")
def login(
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

    if db_user.password != user.password:

        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    token = create_token(
        {
            "username": user.username
        }
    )

    return {
        "access_token": token
    }

# =========================
# CREATE JOKE
# =========================

@app.post("/jokes")
def create_joke(
    joke: schemas.JokeCreate,
    db: Session = Depends(get_db)
):

    new_joke = models.Joke(
        joke=joke.joke
    )

    db.add(new_joke)

    db.commit()

    db.refresh(new_joke)

    return new_joke

# =========================
# GET JOKES
# =========================

@app.get("/jokes")
def get_jokes(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    jokes = db.query(
        models.Joke
    ).offset(skip).limit(limit).all()

    return jokes

# =========================
# RANDOM JOKE
# =========================

@app.get("/random-joke")
def random_joke(
    db: Session = Depends(get_db)
):

    jokes = db.query(
        models.Joke
    ).all()

    if not jokes:

        raise HTTPException(
            status_code=404,
            detail="No jokes found"
        )

    joke = random.choice(jokes)

    return {
        "joke": joke.joke
    }

# =========================
# SEARCH JOKE
# =========================

@app.get("/search")
def search_joke(
    keyword: str,
    db: Session = Depends(get_db)
):

    jokes = db.query(
        models.Joke
    ).filter(
        models.Joke.joke.contains(keyword)
    ).all()

    return jokes

# =========================
# UPDATE JOKE
# =========================

@app.put("/jokes/{joke_id}")
def update_joke(
    joke_id: int,
    updated_joke: schemas.JokeCreate,
    db: Session = Depends(get_db)
):

    joke = db.query(
        models.Joke
    ).filter(
        models.Joke.id == joke_id
    ).first()

    if not joke:

        raise HTTPException(
            status_code=404,
            detail="Joke not found"
        )

    joke.joke = updated_joke.joke

    db.commit()

    return {
        "message": "Joke updated"
    }

# =========================
# DELETE JOKE
# =========================

@app.delete("/jokes/{joke_id}")
def delete_joke(
    joke_id: int,
    db: Session = Depends(get_db)
):

    joke = db.query(
        models.Joke
    ).filter(
        models.Joke.id == joke_id
    ).first()

    if not joke:

        raise HTTPException(
            status_code=404,
            detail="Joke not found"
        )

    db.delete(joke)

    db.commit()

    return {
        "message": "Joke deleted"
    }

# =========================
# FILE UPLOAD
# =========================

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
        "message": "File uploaded",
        "filename": file.filename
    }

# =========================
# ASYNC API
# =========================

@app.get("/async-api")
async def async_api():

    return {
        "message": "⚡ Async API Running"
    }
# =========================================
# AI GENERATED JOKE API
# =========================================
import requests
import os

from dotenv import load_dotenv
load_dotenv()

OPENROUTER_API_KEY = os.getenv(
    "OPENROUTER_API_KEY"
)

@app.get("/ai-joke")
async def ai_joke():

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": (
                    "Generate one short funny programming joke"
                )
            }
        ]
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload
    )

    data = response.json()

    joke = data["choices"][0]["message"]["content"]

    return {
        "ai_joke": joke
    }