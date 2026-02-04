
from sqlalchemy.orm import Session, joinedload
import models, schemas
import bcrypt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica que la contraseña coincida con el hash"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password: str) -> str:
    """Genera un hash bcrypt de la contraseña"""
    # Generar salt y hash
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_cookbooks(db: Session, skip: int = 0, limit: int = 100, search: str = None):
    query = db.query(models.Cookbook).options(joinedload(models.Cookbook.owner))
    if search:
        query = query.filter(models.Cookbook.title.contains(search))
    return query.offset(skip).limit(limit).all()

def create_cookbook(db: Session, cookbook: schemas.CookbookCreate, user_id: int):
    # Extraer recipe_ids del dict porque no es columna del modelo
    cookbook_data = cookbook.dict()
    recipe_ids = cookbook_data.pop('recipe_ids', [])
    
    db_cookbook = models.Cookbook(**cookbook_data, owner_id=user_id)
    
    if recipe_ids:
        # Buscar recetas del usuario que coincidan con los IDs
        recipes = db.query(models.Recipe).filter(
            models.Recipe.id.in_(recipe_ids),
            models.Recipe.owner_id == user_id
        ).all()
        db_cookbook.recipes = recipes
        
    db.add(db_cookbook)
    db.commit()
    db.refresh(db_cookbook)
    return db_cookbook

def update_cookbook(db: Session, cookbook_id: int, cookbook: schemas.CookbookUpdate):
    db_cookbook = db.query(models.Cookbook).filter(models.Cookbook.id == cookbook_id).first()
    if db_cookbook:
        # Obtener los datos a actualizar
        update_data = cookbook.dict(exclude_unset=True)
        recipe_ids = update_data.pop('recipe_ids', None)

        # Actualizar campos simples
        for key, value in update_data.items():
            setattr(db_cookbook, key, value)
            
        # Actualizar recetas si se proporcionaron
        if recipe_ids is not None:
            # Buscar las nuevas recetas seleccionadas (deben ser del mismo dueño)
            new_recipes = db.query(models.Recipe).filter(
                models.Recipe.id.in_(recipe_ids),
                models.Recipe.owner_id == db_cookbook.owner_id
            ).all()
            
            # Asignar la nueva lista de recetas (SQLAlchemy maneja la actualización de FKs)
            # Las recetas que estaban antes y no están ahora tendrán cookbook_id=NULL
            db_cookbook.recipes = new_recipes

        db.commit()
        db.refresh(db_cookbook)
    return db_cookbook

def get_recipes(db: Session, skip: int = 0, limit: int = 100, country: str = None, type: str = None):
    query = db.query(models.Recipe).options(joinedload(models.Recipe.owner))
    if country:
        query = query.filter(models.Recipe.country == country)
    if type:
        query = query.filter(models.Recipe.type == type)
    return query.offset(skip).limit(limit).all()

def create_recipe(db: Session, recipe: schemas.RecipeCreate, user_id: int):
    db_recipe = models.Recipe(**recipe.dict(), owner_id=user_id)
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

def update_recipe(db: Session, recipe_id: int, recipe: schemas.RecipeCreate):
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if db_recipe:
        for key, value in recipe.dict().items():
            setattr(db_recipe, key, value)
        db.commit()
        db.refresh(db_recipe)
    return db_recipe

def get_recipe(db: Session, recipe_id: int):
    return db.query(models.Recipe).options(joinedload(models.Recipe.owner)).filter(models.Recipe.id == recipe_id).first()

def get_cookbook(db: Session, cookbook_id: int):
    return db.query(models.Cookbook).options(
        joinedload(models.Cookbook.owner),
        joinedload(models.Cookbook.recipes).joinedload(models.Recipe.owner)
    ).filter(models.Cookbook.id == cookbook_id).first()

def delete_recipe(db: Session, recipe_id: int):
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if db_recipe:
        db.delete(db_recipe)
        db.commit()
    return db_recipe

def delete_cookbook(db: Session, cookbook_id: int):
    db_cookbook = db.query(models.Cookbook).filter(models.Cookbook.id == cookbook_id).first()
    if db_cookbook:
        db.delete(db_cookbook)
        db.commit()
    return db_cookbook

def get_unique_countries(db: Session):
    return db.query(models.Recipe.country).distinct().filter(models.Recipe.country.isnot(None)).all()
