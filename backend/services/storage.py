import os
from supabase import create_client, Client
from fastapi import UploadFile, HTTPException
import uuid

# Initialize Supabase Client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Create client only if creds are present
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL and SUPABASE_KEY else None

class StorageService:
    @staticmethod
    def upload_file(file: bytes, bucket: str, path: str, content_type: str = "image/jpeg") -> str:
        """
        Uploads a file to Supabase Storage and returns the public URL.
        """
        if not supabase:
            raise HTTPException(status_code=500, detail="Supabase not configured")

        try:
            # Upload file
            res = supabase.storage.from_(bucket).upload(
                path=path,
                file=file,
                file_options={"content-type": content_type}
            )
            
            # Get public URL
            public_url = supabase.storage.from_(bucket).get_public_url(path)
            return public_url
        except Exception as e:
            print(f"Error uploading to Supabase: {e}")
            raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

    @staticmethod
    async def upload_image(file: UploadFile, bucket: str = "recetario-images") -> str:
        """
        Helper for UploadFile objects (images).
        Generates a unique filename.
        """
        file_ext = file.filename.split(".")[-1]
        file_name = f"{uuid.uuid4()}.{file_ext}"
        content = await file.read()
        
        return StorageService.upload_file(
            file=content,
            bucket=bucket,
            path=file_name,
            content_type=file.content_type
        )

    @staticmethod
    def upload_pdf(pdf_bytes: bytes, filename: str) -> str:
        """
        Helper for generated PDFs.
        """
        return StorageService.upload_file(
            file=pdf_bytes,
            bucket="recetarios-pdf",
            path=filename,
            content_type="application/pdf"
        )
