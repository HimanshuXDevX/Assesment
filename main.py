from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import os
from typing import List

from utils.db import init_db
from model.user import User, UserCreate, UserUpdate, UserResponse
from beanie import PydanticObjectId

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing database...")
    await init_db()
    
    yield
    logger.info("Shutdown complete.")


app = FastAPI(
    title="Assesment",
    version="1.0.0",
    description="Assesment for interview at Phykon",
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
        "service": "Assesment",
        "version": "1.0.0",
        "status": "running",
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Assesment for Phykon",
    }


@app.post("/users", response_model=UserResponse)
async def create_user(payload: UserCreate):
    user = User(**payload.dict())
    await user.insert()
    return user


@app.get("/users", response_model=List[UserResponse])
async def get_users():
    return await User.find_all().to_list()


@app.get("/users/{id}", response_model=UserResponse)
async def get_user(id: PydanticObjectId):
    user = await User.get(id)
    if not user:
        raise HTTPException(404, "User not found")
    return user


@app.put("/users/{id}", response_model=UserResponse)
async def update_user(id: PydanticObjectId, payload: UserUpdate):
    user = await User.get(id)
    if not user:
        raise HTTPException(404, "User not found")

    update_data = payload.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    await user.save()
    return user


@app.delete("/users/{id}")
async def delete_user(id: PydanticObjectId):
    user = await User.get(id)
    if not user:
        raise HTTPException(404, "User not found")

    await user.delete()
    return {"message": "User deleted successfully"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)