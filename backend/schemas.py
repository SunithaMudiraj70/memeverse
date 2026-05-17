from pydantic import BaseModel, EmailStr

# =========================
# USER SCHEMAS
# =========================

class UserSignup(BaseModel):

    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):

    email: EmailStr
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
