from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List, Optional
import crud
import models
import schemas
from database import get_db
from routers.auth import get_current_user
from pdf_generator import generate_cookbook_pdf


router = APIRouter(
    prefix="/cookbooks",
    tags=["cookbooks"],
)

@router.get("/{cookbook_id}/pdf")
def get_cookbook_pdf(cookbook_id: int, db: Session = Depends(get_db)):
    # Usar crud.get_cookbook para cargar owner y recipes
    db_cookbook = crud.get_cookbook(db, cookbook_id=cookbook_id)
    if db_cookbook is None:
        raise HTTPException(status_code=404, detail="Cookbook not found")
        
    # Generate PDF (bytes)
    pdf_bytes = generate_cookbook_pdf(db_cookbook, db_cookbook.owner.username)
    
    # Upload to Supabase
    filename = f"cookbook_{cookbook_id}_{db_cookbook.title.replace(' ', '_')}.pdf"
    try:
        from ..services.storage import StorageService
        public_url = StorageService.upload_pdf(pdf_bytes, filename)
        
        # Save URL to DB
        # We need to update existing cookbook instance.
        db_cookbook.pdf_url = public_url
        db.commit()
        db.refresh(db_cookbook)
        
        return {"url": public_url}
    except Exception as e:
        print(f"Error handling PDF: {e}")
        # Fallback: returing styled error or original behavior if upload fails?
        # Requirement says "Generar y guardar". 
        raise HTTPException(status_code=500, detail="Error generating/uploading PDF")

@router.post("/", response_model=schemas.Cookbook)
def create_cookbook(
    cookbook: schemas.CookbookCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    return crud.create_cookbook(db=db, cookbook=cookbook, user_id=current_user.id)

@router.get("/", response_model=List[schemas.Cookbook])
def read_cookbooks(
    skip: int = 0, 
    limit: int = 100, 
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    cookbooks = crud.get_cookbooks(db, skip=skip, limit=limit, search=search)
    return cookbooks

@router.get("/{cookbook_id}", response_model=schemas.Cookbook)
def read_cookbook(cookbook_id: int, db: Session = Depends(get_db)):
    cookbook = crud.get_cookbook(db, cookbook_id=cookbook_id)
    if cookbook is None:
        raise HTTPException(status_code=404, detail="Cookbook not found")
    return cookbook

@router.put("/{cookbook_id}", response_model=schemas.Cookbook)
def update_cookbook(
    cookbook_id: int,
    cookbook: schemas.CookbookUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_cookbook = crud.get_cookbook(db, cookbook_id=cookbook_id)
    if db_cookbook is None:
        raise HTTPException(status_code=404, detail="Cookbook not found")
    
    # Verificar que el usuario sea el dueño
    if db_cookbook.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to edit this cookbook")
    
    return crud.update_cookbook(db=db, cookbook_id=cookbook_id, cookbook=cookbook)

@router.delete("/{cookbook_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cookbook(
    cookbook_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_cookbook = crud.get_cookbook(db, cookbook_id=cookbook_id)
    if db_cookbook is None:
        raise HTTPException(status_code=404, detail="Cookbook not found")
        
    # Verificar que el usuario sea el dueño
    if db_cookbook.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this cookbook")
    
    crud.delete_cookbook(db=db, cookbook_id=cookbook_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
