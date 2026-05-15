from pydantic import BaseModel

# =========================
# USER SCHEMAS
# =========================

class UserSignup(BaseModel):

    username: str
    password: str

class UserLogin(BaseModel):

    username: str
    password: str

# =========================
# JOKE SCHEMAS
# =========================

class JokeCreate(BaseModel):

    joke: str

class JokeResponse(BaseModel):

    id: int
    joke: str

    class Config:

        from_attributes = True