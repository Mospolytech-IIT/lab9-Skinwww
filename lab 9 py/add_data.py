"""Добавление данных в бд"""
from sqlalchemy.orm import sessionmaker
from models import engine, User, Post

Session = sessionmaker(bind=engine)
session = Session()

# Добавление пользователей
user1 = User(username='user1', email='user1@example.com', password='password1')
user2 = User(username='user2', email='user2@example.com', password='password2')

session.add(user1)
session.add(user2)
session.commit()

# Добавление постов
post1 = Post(title='Пост 1', content='Тело пост 1', user_id=user1.id)
post2 = Post(title='Пост 2', content='Тело пост 2', user_id=user2.id)

session.add(post1)
session.add(post2)
session.commit()
