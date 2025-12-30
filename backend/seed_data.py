
from .database import SessionLocal, engine, Base
from . import models, schemas, crud
import random

# Crear tablas si no existen (esto reinicia la db si se borró el archivo)
models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

def seed():
    db = SessionLocal()
    try:
        # Verificar si ya hay datos
        if db.query(models.User).count() > 0:
            print("La base de datos ya contiene datos. Saltando seed.")
            return

        print("Iniciando carga de datos...")

        # --- USUARIOS ---
        users_data = [
            {"username": "ChefJulia", "email": "julia@example.com", "password": "password123"},
            {"username": "GordonB", "email": "gordon@example.com", "password": "heatingup"},
            {"username": "GrandmaRose", "email": "rose@example.com", "password": "secretrecipe"},
        ]

        created_users = []
        for u in users_data:
            user_in = schemas.UserCreate(username=u["username"], email=u["email"], password=u["password"])
            user = crud.create_user(db, user_in)
            created_users.append(user)
            print(f"Usuario creado: {user.username}")

        # --- RECETAS ---
        # ChefJulia (Alta cocina, imágenes bonitas)
        recipes_julia = [
            {
                "title": "Boeuf Bourguignon Clásico",
                "description": "Un estofado francés tradicional cocinado a fuego lento.",
                "country": "Francia",
                "type": "salty",
                "difficulty": "hard",
                "preparation_time_minutes": 180,
                "image_url": "https://images.unsplash.com/photo-1534939561126-855f86654015?auto=format&fit=crop&w=800&q=80",
                "ingredients": [
                    {"name": "Carne de res", "amount": "1", "unit": "kg"},
                    {"name": "Vino tinto", "amount": "500", "unit": "ml"},
                    {"name": "Zanahorias", "amount": "4", "unit": "unid"},
                    {"name": "Cebolla", "amount": "2", "unit": "unid"}
                ],
                "instructions": "1. Cortar la carne en cubos.\n2. Marinar con vino y verduras.\n3. Dorar la carne.\n4. Cocinar a fuego lento por 3 horas.",
                "notes": "Usar un buen vino para mejor sabor."
            },
            {
                "title": "Soufflé de Queso",
                "country": "Francia",
                "type": "salty",
                "difficulty": "medium",
                "preparation_time_minutes": 45,
                "image_url": None, # Sin imagen
                "ingredients": [
                    {"name": "Queso Gruyer", "amount": "200", "unit": "g"},
                    {"name": "Huevos", "amount": "4", "unit": "unid"},
                    {"name": "Leche", "amount": "1", "unit": "taza"}
                ],
                "instructions": "Hacer una bechamel. Añadir queso. Montar claras. Hornear.",
            }
        ]

        # GordonB (Rápido y furioso)
        recipes_gordon = [
            {
                "title": "Huevos Revueltos Perfectos",
                "country": "Reino Unido",
                "type": "salty",
                "difficulty": "medium",
                "preparation_time_minutes": 10,
                "image_url": "https://images.unsplash.com/photo-1525351484163-7529414395d8?auto=format&fit=crop&w=800&q=80",
                "ingredients": [
                    {"name": "Huevos", "amount": "3", "unit": "unid"},
                    {"name": "Mantequilla", "amount": "1", "unit": "cda"},
                    {"name": "Creme fraiche", "amount": "1", "unit": "cdita"}
                ],
                "instructions": "1. Romper huevos en la sartén fría con mantequilla.\n2. Poner al fuego alto moviendo constantemente.\n3. Retirar del fuego cada 30 segundos.\n4. Añadir creme fraiche al final.",
                "notes": "¡No dejes de mover la olla!"
            },
            {
                "title": "Wellington de Carne",
                "country": "Reino Unido",
                "type": "salty",
                "difficulty": "chef",
                "preparation_time_minutes": 120,
                "image_url": "https://images.unsplash.com/photo-1600891964092-4316c288032e?auto=format&fit=crop&w=800&q=80",
                "ingredients": [
                    {"name": "Filete de lomo", "amount": "1", "unit": "kg"},
                    {"name": "Hojaldre", "amount": "1", "unit": "lámina"},
                    {"name": "Champiñones", "amount": "500", "unit": "g"},
                    {"name": "Jamón serrano", "amount": "200", "unit": "g"}
                ],
                "instructions": "Sellar carne. Hacer duxelle. Envolver en jamón y hojaldre. Hornear.",
                "notes": "La carne debe quedar rosada."
            }
        ]

        # GrandmaRose (Postres y tradicional, algunas sin fotos)
        recipes_rose = [
            {
                "title": "Galletas de Chips de Chocolate",
                "country": "USA",
                "type": "sweet",
                "difficulty": "easy",
                "preparation_time_minutes": 30,
                "image_url": "https://images.unsplash.com/photo-1499636138143-bd630f5cf38a?auto=format&fit=crop&w=800&q=80",
                "ingredients": [
                    {"name": "Harina", "amount": "2", "unit": "tazas"},
                    {"name": "Azúcar", "amount": "1", "unit": "taza"},
                    {"name": "Chips de chocolate", "amount": "1", "unit": "taza"},
                    {"name": "Mantequilla", "amount": "100", "unit": "g"}
                ],
                "instructions": "Mezclar todo. Hacer bolitas. Hornear a 180C por 15 min.",
                "notes": "El secreto es el amor."
            },
            {
                "title": "Pie de Manzana",
                "country": "USA",
                "type": "sweet",
                "difficulty": "medium",
                "preparation_time_minutes": 90,
                "image_url": None, # Sin imagen
                "ingredients": [
                    {"name": "Manzanas", "amount": "6", "unit": "unid"},
                    {"name": "Masa de tarta", "amount": "2", "unit": "tapas"},
                    {"name": "Canela", "amount": "1", "unit": "cdita"}
                ],
                "instructions": "Poner manzanas en la masa. Tapar. Hornear hasta que dore.",
            },
               {
                "title": "Sopa de Pollo para el Alma",
                "country": "Internacional",
                "type": "salty",
                "difficulty": "easy",
                "preparation_time_minutes": 60,
                "image_url": None,
                "ingredients": [
                    {"name": "Pollo", "amount": "1", "unit": "unid"},
                    {"name": "Fideos", "amount": "200", "unit": "g"},
                    {"name": "Vegetales varios", "amount": "500", "unit": "g"}
                ],
                "instructions": "Hervir el pollo. Añadir vegetales. Añadir fideos al final.",
            }
        ]

        # Función helper para crear receta
        def add_recipes(user, recipes_list):
            created = []
            for r_data in recipes_list:
                recipe_in = schemas.RecipeCreate(
                    title=r_data["title"],
                    country=r_data.get("country"),
                    type=r_data.get("type"),
                    ingredients=r_data["ingredients"],
                    instructions=r_data["instructions"],
                    instructions_format="numbered",
                    preparation_time_minutes=r_data.get("preparation_time_minutes", 0),
                    difficulty=r_data.get("difficulty", "medium"),
                    image_url=r_data.get("image_url"),
                    notes=r_data.get("notes")
                )
                recipe = crud.create_recipe(db, recipe_in, user.id)
                created.append(recipe)
                print(f"Receta creada: {recipe.title} (Autor: {user.username})")
            return created

        julia_recipes = add_recipes(created_users[0], recipes_julia)
        gordon_recipes = add_recipes(created_users[1], recipes_gordon)
        rose_recipes = add_recipes(created_users[2], recipes_rose)

        # --- RECETARIOS ---
        
        # Julia hace un recetario de "Clásicos Franceses"
        cookbook_julia = crud.create_cookbook(
            db, 
            schemas.CookbookCreate(
                title="Mis Clásicos Franceses", 
                description="Una colección de mis platos favoritos de la cocina francesa.",
                recipe_ids=[julia_recipes[0].id, julia_recipes[1].id]
            ), 
            created_users[0].id
        )
        print(f"Recetario creado: {cookbook_julia.title} (Autor: ChefJulia)")

        # Gordon hace un recetario "Cena Express" (solo 1 receta)
        cookbook_gordon = crud.create_cookbook(
            db,
            schemas.CookbookCreate(
                title="Cena en 10 Minutos",
                description="Para cuando no tienes tiempo que perder.",
                recipe_ids=[gordon_recipes[0].id]
            ),
            created_users[1].id
        )
        print(f"Recetario creado: {cookbook_gordon.title} (Autor: GordonB)")
        
        # Rose hace un recetario de "Postres de la Abuela"
        cookbook_rose = crud.create_cookbook(
            db,
            schemas.CookbookCreate(
                title="Dulces Recuerdos",
                description="Recetas que he horneado para mis nietos durante años.",
                recipe_ids=[rose_recipes[0].id, rose_recipes[1].id]
            ),
            created_users[2].id
        )
        print(f"Recetario creado: {cookbook_rose.title} (Autor: GrandmaRose)")

        print("--- Carga de datos completada exitosamente ---")

    except Exception as e:
        print(f"Error durante el seed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
