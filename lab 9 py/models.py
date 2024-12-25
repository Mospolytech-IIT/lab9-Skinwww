"""Создание таблиц в базе данным"""
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class User(Base):
    """Пользователь"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    # Связь с постами
    posts = relationship("Post", back_populates="user")

class Post(Base):
    """Пост"""
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Связь с пользователем
    user = relationship("User", back_populates="posts")

# Подключение к базе данных
engine = create_engine('postgresql://postgres:qwerty@localhost/mydatabase')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
