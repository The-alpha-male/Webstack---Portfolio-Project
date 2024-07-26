from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from customer import services as customers_model
from customer import schema as customers_schema
from sqlalchemy.orm import Session
from typing import List, Optional
from db import get_db
from datetime import datetime, timedelta
from customer.models import BlogImage, BlogPost, User as userModel


router = APIRouter()


@router.get("/get_me")
async def read_current_user(username: str = Depends(customers_model.get_current_user)):
    return {"username": username}


@router.post(
    "/add_users",
    tags=["users"],
)
async def add_user(user: customers_schema.User, db: Session = Depends(get_db)):
    user = await customers_model.create_user(db=db, user=user)
    return user


@router.get("/get_all", tags=["users"], response_model=List[customers_schema.User])
async def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = await customers_model.get_all_users(db=db, skip=skip, limit=limit)
    return users


@router.post("/login/", tags=["users"], response_model=customers_schema.Token)
def login(user: customers_schema.UserLogin, db: Session = Depends(get_db)):
    if not user.email or not user.password:
        raise HTTPException(status_code=400, detail="Email and password are required")

    db_user = db.query(userModel).filter(userModel.email == user.email).first()
    if db_user is None:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not customers_model.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    access_token_expires = timedelta(
        minutes=customers_model.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = customers_model.create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/blog_posts", tags=["blogs"])
async def create_blog_post(
    title: str = Form(...),
    content: str = Form(...),
    category: str = Form(...),
    images: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: str = Depends(customers_model.get_current_user),
):
    db_blog_post = BlogPost(
        title=title,
        content=content,
        category=category,
        author=current_user,
    )
    db.add(db_blog_post)
    db.commit()
    db.refresh(db_blog_post)

    if images:
        saved_images = await customers_model.save_images(images)
        for image in saved_images:
            db_blog_image = BlogImage(
                blog_post_id=db_blog_post.id,
                image_url=image["src"],
            )
            db.add(db_blog_image)
        db.commit()

    return {
        "id": db_blog_post.id,
        "title": db_blog_post.title,
        "content": db_blog_post.content,
        "category": db_blog_post.category,
        "author": db_blog_post.author,
        "created_at": db_blog_post.created_at,
        "images": saved_images if images else [],
    }

@router.get("/get_all_blogs", tags=["blogs"], response_model=List[customers_schema.BlogPostBase])
async def get_blogs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    blogs = await customers_model.get_all_blogs(db=db, skip=skip, limit=limit)
    return blogs

@router.delete("/delete_all_blogs", tags=["blogs"])
async def delete_blogs( db: Session = Depends(get_db)):
    blogs = await customers_model.delete_allblogs(db=db)
    return blogs

@router.get("/blog_posts/{post_id}",tags=["blogs"], response_model=customers_schema.BlogPostBase)
async def read_blog_post(post_id: int, db: Session = Depends(get_db)):
    blog =  customers_model.get_blog_by_id(post_id=post_id, db=db)
    return blog