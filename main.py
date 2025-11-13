from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from contextlib import asynccontextmanager
import logging
import os
from typing import List

from utils.db import init_db
from utils.auth import verify_password, create_access_token
from model.user import User, UserCreate, UserUpdate, UserResponse
from beanie import PydanticObjectId
from jose import JWTError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    from utils.auth import decode_token

    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
        user = await User.get(user_id)
        if not user:
            raise HTTPException(401, "Invalid token")
        return user
    except JWTError:
        raise HTTPException(401, "Invalid or expired token")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing database...")
    await init_db()
    
    yield
    logger.info("Shutdown complete.")


app = FastAPI(
    title="Assessment",
    version="1.0.0",
    description="Assessment for interview at Phykon",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "service": "Assessment",
        "version": "1.0.0",
        "status": "running",
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Assessment for Phykon",
    }


@app.post("/register", response_model=UserResponse)
async def register_user(payload: UserCreate):
    exists = await User.find_one(User.email == payload.email)
    if exists:
        raise HTTPException(400, "Email already registered")

    user = User(
        email=payload.email,
        first_name=payload.first_name,
        last_name=payload.last_name,
        phone_number=payload.phone_number,
        roles=payload.roles,
        password=""
    )

    await user.set_password(payload.password)
    await user.insert()

    return user


@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await User.find_one(User.email == form_data.username)
    if not user:
        raise HTTPException(401, "Invalid email or password")
    
    if not verify_password(form_data.password, user.password):
        raise HTTPException(401, "Invalid email or password")

    token = create_access_token({"sub": str(user.id)})

    return {"access_token": token, "token_type": "bearer"}


@app.post("/users", response_model=UserResponse)
async def create_user(payload: UserCreate, current_user: User = Depends(get_current_user)):
    user = User(**payload.dict())
    await user.set_password(payload.password)
    await user.insert()
    return user


@app.get("/users", response_model=List[UserResponse])
async def get_users(current_user: User = Depends(get_current_user)):
    return await User.find_all().to_list()


@app.get("/users/{id}", response_model=UserResponse)
async def get_user(id: PydanticObjectId, current_user: User = Depends(get_current_user)):
    user = await User.get(id)
    if not user:
        raise HTTPException(404, "User not found")
    return user


@app.put("/users/{id}", response_model=UserResponse)
async def update_user(id: PydanticObjectId, payload: UserUpdate, current_user: User = Depends(get_current_user)):
    user = await User.get(id)
    if not user:
        raise HTTPException(404, "User not found")

    update_data = payload.dict(exclude_unset=True)

    if "password" in update_data:
        await user.set_password(update_data["password"])
        del update_data["password"]

    for field, value in update_data.items():
        setattr(user, field, value)

    await user.save()
    return user


@app.delete("/users/{id}")
async def delete_user(id: PydanticObjectId, current_user: User = Depends(get_current_user)):
    user = await User.get(id)
    if not user:
        raise HTTPException(404, "User not found")

    await user.delete()
    return {"message": "User deleted successfully"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
