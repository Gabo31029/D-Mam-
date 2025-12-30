
from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os
import uuid

router = APIRouter(
    prefix="/upload",
    tags=["upload"],
)

UPLOAD_DIR = "backend/static/images"

@router.post("/", response_model=dict)
async def upload_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Create unique filename
    extension = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{extension}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    # Save file
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Could not save file")
        
    # Return URL (assuming localhost:8000 for local dev, should be config driven ideally)
    # The static mount will be at /static
    url = f"http://localhost:8000/static/images/{filename}"
    return {"url": url}
