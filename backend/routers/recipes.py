
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import crud, models, schemas
from database import get_db
from auth import get_current_user
from pdf_generator import generate_recipe_pdf # Import the generator

router = APIRouter(
    prefix="/recipes",
    tags=["recipes"],
)

@router.get("/{recipe_id}/pdf")
def get_recipe_pdf(recipe_id: int, db: Session = Depends(get_db)):
    db_recipe = crud.get_recipe(db, recipe_id=recipe_id)
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    # Generate PDF
    pdf_buffer = generate_recipe_pdf(db_recipe, db_recipe.owner.username)
    
    headers = {
        'Content-Disposition': f'attachment; filename="{db_recipe.title}.pdf"'
    }
    return StreamingResponse(pdf_buffer, media_type="application/pdf", headers=headers)

@router.post("/", response_model=schemas.Recipe)
def create_recipe(
    recipe: schemas.RecipeCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    # Validar propiedad del recetario si se proporciona
    if recipe.cookbook_id:
        cookbook = crud.get_cookbook(db, recipe.cookbook_id)
        if not cookbook:
             raise HTTPException(status_code=404, detail="Cookbook not found")
        if cookbook.owner_id != current_user.id:
             raise HTTPException(status_code=403, detail="You can only add recipes to your own cookbooks")
             
    return crud.create_recipe(db=db, recipe=recipe, user_id=current_user.id)

@router.get("/", response_model=List[schemas.Recipe])
def read_recipes(
    skip: int = 0, 
    limit: int = 100, 
    country: Optional[str] = None, 
    type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    recipes = crud.get_recipes(db, skip=skip, limit=limit, country=country, type=type)
    return recipes

@router.get("/{recipe_id}", response_model=schemas.Recipe)
def read_recipe(recipe_id: int, db: Session = Depends(get_db)):
    db_recipe = crud.get_recipe(db, recipe_id=recipe_id)
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return db_recipe

@router.put("/{recipe_id}", response_model=schemas.Recipe)
def update_recipe(
    recipe_id: int,
    recipe: schemas.RecipeCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_recipe = crud.get_recipe(db, recipe_id=recipe_id)
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    # Verificar que el usuario sea el dueño de la receta
    if db_recipe.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to edit this recipe")
    
    # Validar propiedad del recetario si se proporciona
    if recipe.cookbook_id:
        cookbook = crud.get_cookbook(db, recipe.cookbook_id)
        if not cookbook:
             raise HTTPException(status_code=404, detail="Cookbook not found")
        if cookbook.owner_id != current_user.id:
             raise HTTPException(status_code=403, detail="You can only add recipes to your own cookbooks")
    
    return crud.update_recipe(db=db, recipe_id=recipe_id, recipe=recipe)

@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_recipe = crud.get_recipe(db, recipe_id=recipe_id)
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
        
    # Verificar que el usuario sea el dueño
    if db_recipe.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this recipe")
    
    crud.delete_recipe(db=db, recipe_id=recipe_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
