"""создание всех операций"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session as DbSession
from models import User, Post, Session

app = FastAPI()
session = Session()

# Модели для запросов
class UserCreate(BaseModel):
    """Класс создания пользователя"""
    username: str
    email: str
    password: str

class PostCreate(BaseModel):
    """Класс создания поста"""
    title: str
    content: str
    user_id: int

class UserUpdate(BaseModel):
    """класс обновления пользователя"""
    email: str

class PostUpdate(BaseModel):
    """класс обновления поста"""
    content: str

@app.post("/users/")
def create_user(user: UserCreate):
    """Создание нового пользователя."""
    new_user = User(username=user.username, email=user.email, password=user.password)
    session.add(new_user)
    session.commit()
    return {"message": "Пользователь создан"}

@app.post("/posts/")
def create_post(post: PostCreate):
    """Создание нового поста."""
    new_post = Post(title=post.title, content=post.content, user_id=post.user_id)
    session.add(new_post)
    session.commit()
    return {"message": "Пост создан"}

@app.get("/users/")
def read_users():
    """Чтение всех пользователей."""
    users = session.query(User).all()
    return users

@app.get("/users/{user_id}")
def read_user(user_id: int):
    """Чтение конкретного пользователя по ID."""
    user = session.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user

@app.get("/posts/")
def read_posts():
    """Чтение всех постов."""
    posts = session.query(Post).all()
    return posts

@app.get("/posts/{post_id}")
def read_post(post_id: int):
    """Чтение конкретного поста по ID."""
    post = session.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Пост не найден")
    return post

@app.get("/users/{user_id}/posts/")
def read_user_posts(user_id: int):
    """Чтение постов конкретного пользователя."""
    posts = session.query(Post).filter(Post.user_id == user_id).all()
    if not posts:
        raise HTTPException(status_code=404, detail="Посты не найдены")
    return posts

@app.patch("/users/{user_id}/")
def update_user(user_id: int, user: UserUpdate):
    """Обновление email пользователя."""
    user_to_update = session.query(User).filter(User.id == user_id).first()
    if user_to_update is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    user_to_update.email = user.email
    session.commit()
    return {"message": "Email обновлен"}

@app.patch("/posts/{post_id}/")
def update_post(post_id: int, post: PostUpdate):
    """Обновление контента поста."""
    post_to_update = session.query(Post).filter(Post.id == post_id).first()
    if post_to_update is None:
        raise HTTPException(status_code=404, detail="Пост не найден")
    post_to_update.content = post.content
    session.commit()
    return {"message": "Контент поста обновлен"}

@app.delete("/posts/{post_id}/")
def delete_post(post_id: int):
    """Удаление поста."""
    post_to_delete = session.query(Post).filter(Post.id == post_id).first()
    if post_to_delete is None:
        raise HTTPException(status_code=404, detail="Пост не найден")
    session.delete(post_to_delete)
    session.commit()
    return {"message": "Пост удален"}

@app.delete("/users/{user_id}/")
def delete_user(user_id: int):
    """Удаление пользователя и всех его постов."""
    user_to_delete = session.query(User).filter(User.id == user_id).first()
    if user_to_delete is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # Удаляем связанные посты
    posts_to_delete = session.query(Post).filter(Post.user_id == user_id).all()
    for post in posts_to_delete:
        session.delete(post)

    session.delete(user_to_delete)
    session.commit()
    return {"message": "Пользователь и его посты удалены"}
