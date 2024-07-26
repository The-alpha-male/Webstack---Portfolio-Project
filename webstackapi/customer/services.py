import datetime
import os
import secrets
from typing import List, Optional
import aiofiles
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordBearer,
)
from fastapi.staticfiles import StaticFiles
from jose import JWTError
from passlib.context import CryptContext
import re
import bcrypt
from fastapi import Depends, FastAPI, HTTPException, Request, Security, UploadFile
import jwt
from customer.schema import UserLogin
from customer.schema import User
from customer.models import BlogImage, BlogPost, User as userModel
from sqlalchemy.orm import Session
from db import engine
from db import Base
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import uuid

app = FastAPI()


UPLOAD_FOLDER = "./static/images/"
ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg", "gif"]

"""give access to static files"""
app.mount("/static", StaticFiles(directory="static"), name="static")


Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "6d86aee92efa30764e31bc2cb4663d4a254133132b8d90d21757ac7cc203abed"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class OptionalBearer:
    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        authorization: str = request.headers.get("Authorization")
        if authorization:
            try:
                return await HTTPBearer()(request)
            except:
                return


security = HTTPBearer()

optional = OptionalBearer()


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=401, detail="Invalid authentication credentials"
            )
        truncated_email = username.split("@")[0]
        return truncated_email
    except JWTError:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def validate_password(password: str) -> bool:
    if len(password) < 8:
        raise HTTPException(
            status_code=400, detail="Password must be at least 8 characters long."
        )
    if not re.search(r"[A-Z]", password):
        raise HTTPException(
            status_code=400,
            detail="Password must contain at least one uppercase letter.",
        )
    if not re.search(r"[a-z]", password):
        raise HTTPException(
            status_code=400,
            detail="Password must contain at least one lowercase letter.",
        )
    if not re.search(r"[0-9]", password):
        raise HTTPException(
            status_code=400, detail="Password must contain at least one digit."
        )
    if not re.search(r"[!@#\$%\^&\*]", password):
        raise HTTPException(
            status_code=400,
            detail="Password must contain at least one special character.",
        )
    return True


async def create_user(db: Session, user: userModel) -> userModel:
    existing_user = await get_user_by_email(db=db, email=user.email)
    if existing_user:
        raise HTTPException(
            status_code=400, detail="user with this email already exists"
        )
    validate_password(user.password)
    hashed_password = hash_password(user.password)
    new_user = userModel(name=user.name, email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def get_user_by_email(db: Session, email: str) -> userModel:
    return db.query(userModel).filter(userModel.email == email).first()


def decoded_user(user: object) -> dict:
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "password": user.password,
    }


def decoded_users(users) -> list:
    return [decoded_user(user) for user in users]


async def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> list:
    users = db.query(userModel).offset(skip).limit(limit).all()
    users_data = decoded_users(users)
    return users_data


def allowed_file(filename: str) -> bool:
    filename = filename.lower()
    filename = filename.replace(" ", "_")
    filename = secure_filename(filename)
    filename = str(uuid.uuid4()) + filename
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


async def save_images(images: List[UploadFile]):
    saved_images = []
    for image in images:
        if allowed_file(image.filename):
            image.filename = secure_filename(image.filename)
            image.filename = secrets.token_hex(32) + image.filename
            image_path = os.path.join(UPLOAD_FOLDER, image.filename)
            async with aiofiles.open(image_path, "wb") as f:
                await f.write(await image.read())
                url = {
                    "src": "localhost:80/static/images/" + image_path.split("/")[-1]
                }
                saved_images.append(url)
    return saved_images

async def get_all_blogs(db: Session, skip: int = 0, limit: int = 100) -> list:
    blog_post = db.query(BlogPost).offset(skip).limit(limit).all()
    return blog_post

async def delete_allblogs(db: Session, ) -> dict:
    db.query(BlogPost).delete()
    db.query(BlogImage).delete()
    db.commit()
    return {
        "message":"deleted all"
    }

def decoded_blog(blog: object) -> dict:
    return {
        "id": blog.id,
        "title": blog.title,
        "content": blog.content,
        "category": blog.category,
        "author": blog.author,
        "created_at": blog.created_at,
        "images": [{"id": image.id, "blog_post_id": image.blog_post_id, "image_url": image.image_url} for image in blog.images],
    }

def get_blog_by_id(post_id: int, db:Session)  -> dict:
    blog = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    if blog is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return decoded_blog(blog)
