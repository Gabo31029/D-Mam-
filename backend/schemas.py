
from pydantic import BaseModel
from typing import List, Optional

from datetime import datetime

class Ingredient(BaseModel):
    name: str
    amount: Optional[str] = None
    unit: Optional[str] = None

class RatingBase(BaseModel):
    score: int

class RatingCreate(RatingBase):
    pass

class Rating(RatingBase):
    id: int
    user_id: int
    recipe_id: Optional[int] = None
    cookbook_id: Optional[int] = None
    
    class Config:
        from_attributes = True

# Schema básico de usuario para evitar referencias circulares
class UserBasic(BaseModel):
    id: int
    username: str
    email: str
    
    class Config:
        from_attributes = True

class RecipeBase(BaseModel):
    title: str
    ingredients: List[Ingredient]
    instructions: str
    instructions_format: str = "numbered"  # 'numbered' or 'plain'
    country: Optional[str] = None
    type: Optional[str] = None
    image_url: Optional[str] = None
    cookbook_id: Optional[int] = None
    preparation_time_minutes: int = 0
    difficulty: str = "medium"
    notes: Optional[str] = None

class RecipeCreate(RecipeBase):
    pass

class Recipe(RecipeBase):
    id: int
    owner_id: int
    created_at: datetime
    owner: Optional[UserBasic] = None  # Información del autor
    
    class Config:
        from_attributes = True

class CookbookBase(BaseModel):
    title: str
    description: Optional[str] = None

class CookbookCreate(CookbookBase):
    recipe_ids: List[int] = []

class CookbookUpdate(CookbookBase):
    recipe_ids: Optional[List[int]] = None

class Cookbook(CookbookBase):
    id: int
    owner_id: int
    created_at: datetime
    recipes: List[Recipe] = []
    owner: Optional[UserBasic] = None  # Información del autor

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    recipes: List[Recipe] = []
    cookbooks: List[Cookbook] = []

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Resolver referencias circulares
Recipe.model_rebuild()
Cookbook.model_rebuild()
User.model_rebuild()
