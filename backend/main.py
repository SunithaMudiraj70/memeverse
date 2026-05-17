from fastapi import (
    FastAPI,
    HTTPException,
    UploadFile,
    File
)

from fastapi.middleware.cors import CORSMiddleware

import random
import os

app = FastAPI()

# =========================================
# CORS
# =========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================
# STORAGE
# =========================================

jokes_db = []

UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

# =========================================
# ROOT
# =========================================

@app.get("/")
def home():

    return {
        "message": "😂 MemeVerse Backend Running"
    }

# =========================================
# ADD JOKE
# =========================================

@app.post("/jokes")
def add_joke(data: dict):

    joke_text = data.get("joke")

    if not joke_text:

        raise HTTPException(
            status_code=400,
            detail="Joke cannot be empty"
        )

    joke = {
        "id": len(jokes_db) + 1,
        "joke": joke_text
    }

    jokes_db.append(joke)

    return {
        "message": "Joke Added Successfully",
        "data": joke
    }

# =========================================
# GET ALL JOKES
# =========================================

@app.get("/get-jokes")
def get_jokes():

    return jokes_db

# =========================================
# RANDOM JOKE
# =========================================

@app.get("/random-joke")
def random_joke():

    if len(jokes_db) == 0:

        return {
            "joke": "No jokes available 😂"
        }

    joke = random.choice(jokes_db)

    return joke

# =========================================
# AI JOKE GENERATOR
# =========================================

@app.get("/ai-joke")
def ai_joke():

    ai_jokes = [

        "Why don’t programmers like nature? Too many bugs 😂",

        "Why did Python go to therapy? Too many indentation issues 😂",

        "Why do Java developers wear glasses? Because they don’t C# 😂",

        "Why was the computer cold? It forgot to close Windows 😂",

        "Why did the AI break up? Lack of emotional bandwidth 😂"
    ]

    return {
        "ai_joke": random.choice(ai_jokes)
    }

# =========================================
# SEARCH JOKE
# =========================================

@app.get("/search")
def search_joke(keyword: str):

    results = []

    for joke in jokes_db:

        if keyword.lower() in joke["joke"].lower():

            results.append(joke)

    return results

# =========================================
# UPDATE JOKE
# =========================================

@app.put("/jokes/{joke_id}")
def update_joke(
    joke_id: int,
    data: dict
):

    for joke in jokes_db:

        if joke["id"] == joke_id:

            joke["joke"] = data.get(
                "joke",
                joke["joke"]
            )

            return {
                "message": "Joke Updated Successfully"
            }

    raise HTTPException(
        status_code=404,
        detail="Joke not found"
    )

# =========================================
# DELETE JOKE
# =========================================

@app.delete("/jokes/{joke_id}")
def delete_joke(joke_id: int):

    for joke in jokes_db:

        if joke["id"] == joke_id:

            jokes_db.remove(joke)

            return {
                "message": "Joke Deleted Successfully"
            }

    raise HTTPException(
        status_code=404,
        detail="Joke not found"
    )

# =========================================
# FILE UPLOAD
# =========================================

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...)
):

    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(file_path, "wb") as f:

        f.write(await file.read())

    return {
        "filename": file.filename
    }
