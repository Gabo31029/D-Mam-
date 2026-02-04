from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from services.storage import StorageService

router = APIRouter(
    prefix="/upload",
    tags=["upload"],
)

@router.post("/", response_model=dict)
async def upload_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Upload to Supabase 'recetario-images' bucket (or separate for consistency)
        # We can use a single bucket or the specific one. Plan said 'recetarios-images' and 'recetas-images'.
        # Since this endpoint is generic, let's stick to a default or decide based on input? 
        # For simplicity, let's use 'recetario-images' for now as defined in service default.
        url = await StorageService.upload_image(file, bucket="recetario-images")
        
        return {"url": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
