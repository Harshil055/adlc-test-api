from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


# --- Existing models ---

class Item(BaseModel):
    name: str
    price: float


# --- Password reset models ---

class PasswordResetRequest(BaseModel):
    email: str

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str


# --- Existing endpoints ---

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.post("/items", status_code=201)
def create_item(item: Item):
    return {"name": item.name, "price": item.price}


# --- Password reset endpoints ---

@app.post("/password-reset/request", status_code=200)
def request_password_reset(payload: PasswordResetRequest):
    if not payload.email or "@" not in payload.email:
        raise HTTPException(status_code=422, detail="Invalid email address")
    return {
        "message": "If that email is registered, a reset link has been sent."
    }


@app.post("/password-reset/confirm", status_code=200)
def confirm_password_reset(payload: PasswordResetConfirm):
    if not payload.token or not payload.token.strip():
        raise HTTPException(status_code=422, detail="Token is required")
    if not payload.new_password or len(payload.new_password) < 8:
        raise HTTPException(
            status_code=422, detail="Password must be at least 8 characters"
        )
    # Stub: treat any non-empty token as valid
    return {"message": "Password has been reset successfully."}
