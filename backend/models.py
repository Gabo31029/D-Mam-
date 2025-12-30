
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, DateTime, JSON
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    recipes = relationship("Recipe", back_populates="owner")
    cookbooks = relationship("Cookbook", back_populates="owner")

class Cookbook(Base):
    __tablename__ = "cookbooks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="cookbooks")
    recipes = relationship("Recipe", back_populates="cookbook")
    ratings = relationship("Rating", back_populates="cookbook")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    ingredients = Column(JSON)
    instructions = Column(Text)
    instructions_format = Column(String, default="numbered")  # 'numbered' or 'plain'
    country = Column(String)
    type = Column(String)
    image_url = Column(String, nullable=True)
    
    preparation_time_minutes = Column(Integer, default=0)
    difficulty = Column(String, default="medium")
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    owner_id = Column(Integer, ForeignKey("users.id"))
    cookbook_id = Column(Integer, ForeignKey("cookbooks.id"), nullable=True)

    owner = relationship("User", back_populates="recipes")
    cookbook = relationship("Cookbook", back_populates="recipes")
    ratings = relationship("Rating", back_populates="recipe")

class Rating(Base):
    __tablename__ = "ratings"
    
    id = Column(Integer, primary_key=True, index=True)
    score = Column(Integer) # 1-5
    
    user_id = Column(Integer, ForeignKey("users.id"))
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=True)
    cookbook_id = Column(Integer, ForeignKey("cookbooks.id"), nullable=True)
    
    user = relationship("User")
    recipe = relationship("Recipe", back_populates="ratings")
    cookbook = relationship("Cookbook", back_populates="ratings")

