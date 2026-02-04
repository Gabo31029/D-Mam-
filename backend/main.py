from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from fastapi.staticfiles import StaticFiles
from routers import auth, recipes, cookbooks, upload
from dotenv import load_dotenv
import os

load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Recetario API")

# CORS setup
# CORS setup
# In production, set ALLOWED_ORIGINS to "https://recetario.onrender.com,https://www.recetario.com"
allowed_origins_str = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
origins = allowed_origins_str.split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging (Basic setup)
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    logger.info("Application starting up...")


# Mount static files
# Mount static files if directory exists
import os
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
else:
    logger.warning(f"Static directory '{static_dir}' not found. Skipping mount.")

app.include_router(auth.router)
app.include_router(recipes.router)
app.include_router(cookbooks.router)
app.include_router(upload.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Recetario API"}
