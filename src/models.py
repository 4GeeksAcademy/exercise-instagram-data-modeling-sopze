import os
import sys
from sqlalchemy import Column, ForeignKey, Boolean, Integer, String, Enum, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    password = Column(String(16), nullable=False)
    bio = Column(String(512), nullable=False)
    avatar_url = Column(String(1024), nullable=False)

    # only set to_dict here dunno why
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "password": self.password,
            "bio": self.bio,
            "avatar_url": self.avatar_url
        }

class User_Like(Base):
    __tablename__ = "user_like"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)

    user = relationship('User', uselist=False)
    post = relationship('Post', uselist=False)

class User_DirectMessage(Base):
    __tablename__ = "user_directmessage"
    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    receiver_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    data_url = Column(String(1024), nullable=False)

    user = relationship('User')

class User_Follow(Base):
    __tablename__ = "user_follow"
    id = Column(Integer, primary_key=True)
    follower_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    following_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    user = relationship('User')

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    media_id = Column(Integer, ForeignKey('media.id'), nullable=False)
    is_story= Column(Boolean, nullable=False)
    time_created = Column(DateTime(timezone=False), server_default=func.now(), nullable=False)
    impressions = Column(Integer, nullable=False)
    views = Column(Integer, nullable=False)
    likes = Column(Integer, nullable=False)
    time_scheduled = Column(DateTime(timezone=False), nullable=True)
    published = Column(Boolean, nullable=False)
    comments_enabled= Column(Boolean, nullable=False)

    user= relationship("User")
    media= relationship("Media")

class Post_Comment(Base):
    __tablename__ = "post_comment"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    time_created = Column(DateTime(timezone=False), server_default=func.now(), nullable=False)
    likes = Column(Integer, nullable=False)
    data_url = Column(String(1024), nullable=False)

    user = relationship('User')
    post = relationship('Post', uselist=False)

class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    type = Column(Enum("photo", "video", name="type_enum"))
    file_url = Column(String(1024), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)

    post = relationship('Post', uselist=False)

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram") # notice the word "genering" someone wrote here xd... nice one!
    raise e
