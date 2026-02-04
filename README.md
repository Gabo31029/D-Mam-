# 🍳 Proyecto Recetario (Production Ready)

Aplicación web full-stack para gestión de recetas, preparada para despliegue en producción con Docker, PostgreSQL y Cloudinary.

![Estado](https://img.shields.io/badge/Production-Ready-green?style=flat-square)
![Stack](https://img.shields.io/badge/Stack-FastAPI%20%2B%20Vue%203%20%2B%20Postgres-blue?style=flat-square)

## 🚀 Despliegue en Render

Este proyecto está optimizado para desplegarse en [Render.com](https://render.com).

### 1. Base de Datos (PostgreSQL)
Crea un servicio **PostgreSQL** en Render.
- Copia la `Internal Database URL` (para el backend en Render).

### 2. Backend (Web Service)
Crea un **Web Service** conectado a este repositorio.
- **Root Directory**: `backend`
- **Environment**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn -k uvicorn.workers.UvicornWorker main:app`
- **Variables de Entorno**:
    - `DATABASE_URL`: URL de tu base de datos Postgres.
    - `SECRET_KEY`: Una cadena larga y segura.
    - `ALLOWED_ORIGINS`: `https://tu-frontend.onrender.com`

### 3. Frontend (Static Site)
Crea un **Static Site** en Render.
- **Root Directory**: `frontend`
- **Build Command**: `npm install && npm run build`
- **Publish Directory**: `dist`
- **Variables de Entorno**:
    - `VITE_API_URL`: `https://tu-backend.onrender.com`

## 🐳 Docker (Desarrollo Local)

Puedes levantar todo el entorno (Base de datos, Backend, Frontend) usando Docker Compose.

```bash
docker-compose up --build
```

- **Frontend**: http://localhost:8080
- **Backend API**: http://localhost:8000
- **Base de Datos**: Puerto 5432

## 🛠️ Variables de Entorno

| Variable | Descripción |
|----------|-------------|
| `DATABASE_URL` | Connection string de PostgreSQL (o SQLite en local) |
| `SECRET_KEY` | Llave para firmar tokens JWT |
| `ALLOWED_ORIGINS` | Orígenes permitidos para CORS (separados por coma) |
| `CLOUDINARY_*` | Credenciales para subida de imágenes |
| `VITE_API_URL` | URL del backend (Frontend only) |

## 🧪 Tests y Calidad

El proyecto incluye configuración para despliegue robusto:
- **Gunicorn**: Servidor de aplicaciones de producción.
- **PostgreSQL**: Base de datos relacional robusta.
- **Cloudinary**: CDN para imágenes.
- **Docker**: Contenedorización para consistencia.

---
Desarrollado con estándares de ingeniería de software.
