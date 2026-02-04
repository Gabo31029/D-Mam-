# 🍳 Proyecto Recetario (D'Mamá)

Aplicación web full-stack para gestión de recetas con diseño editorial y funcionalidades modernas, impulsada por tecnología escalable.

![Estado](https://img.shields.io/badge/Production-Ready-green?style=flat-square)
![Stack](https://img.shields.io/badge/Stack-FastAPI%20%2B%20Vue%203%20%2B%20Supabase-blue?style=flat-square)
![Deploy](https://img.shields.io/badge/Deploy-Vercel-black?style=flat-square&logo=vercel)

## 🚀 Arquitectura y Tecnologías

El proyecto utiliza una arquitectura moderna y desacoplada:

- **Frontend**: Vue 3 + Vite + TailwindCSS. Diseño responsivo y "Mobile First". Alojado en **Vercel**.
- **Backend**: FastAPI (Python). API RESTful de alto rendimiento. Alojado en **Vercel** (Serverless Functions) o servicio compatible.
- **Base de Datos**: PostgreSQL (vía **Supabase**).
- **Almacenamiento**: Supabase Storage (para imágenes de recetas y PDFs).
- **Autenticación**: JWT (JSON Web Tokens).

## 🛠️ Configuración Local

### 1. Clonar el repositorio

```bash
git clone https://github.com/Gabo31029/D-Mam-.git
cd D-Mam-
```

### 2. Backend (FastAPI)

```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

Crea un archivo `.env` en la carpeta `backend/` con las siguientes variables de Supabase:

```env
SUPABASE_URL="tu_url_de_supabase"
SUPABASE_KEY="tu_anon_public_key"
SECRET_KEY="tu_secret_para_jwt"
ALLOWED_ORIGINS="http://localhost:5173,https://tu-proyecto.vercel.app"
```

Para correr el servidor localmente:

```bash
uvicorn main:app --reload
```

### 3. Frontend (Vue 3)

```bash
cd frontend
npm install
```

Crea un archivo `.env` en la carpeta `frontend/`:

```env
VITE_API_URL="http://localhost:8000"
```

_(Para producción, VITE_API_URL debe apuntar a la URL de tu backend)_

Para correr el frontend:

```bash
npm run dev
```

## ☁️ Despliegue en Vercel

Este proyecto está configurado para desplegarse fácilmente en Vercel.

1.  Conecta tu repositorio de GitHub a Vercel.
2.  Configura el **Root Directory** del frontend (si prefieres separar deployments) o usa la configuración `vercel.json` incluida para el manejo de rutas SPA.
3.  **Variables de Entorno en Vercel**:
    - Agrega las mismas variables (`SUPABASE_URL`, `SUPABASE_KEY`, `SECRET_KEY`) en la configuración del proyecto en Vercel.
    - Asegúrate de que `VITE_API_URL` en el frontend apunte a la URL de producción de tu API.

## ✅ Funcionalidades Actuales

- Gestión completa de Recetas (CRUD).
- Filtrado dinámico por país/región y tipo de plato.
- Generación automática de PDFs de recetas.
- Autenticación de usuarios (Registro/Login).
- Colecciones de recetas (Cookbooks).
- Diseño responsive adaptado a dispositivos móviles.

## 🔮 Próximos Pasos

- Implementar mayor seguridad (Rate limiting, validaciones extendidas).
- Implementar registro con OAuth (Google/GitHub).
- Implementar carga de imágenes con IA para transcripción automática a receta digitalizada.

---

**Open Source Project made by Gabriel Chupa :)**
_Developed using software engineering standards._
