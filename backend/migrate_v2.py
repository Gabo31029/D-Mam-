
from sqlalchemy import create_engine, MetaData, text
import datetime

DATABASE_URL = "sqlite:///../recetario.db"
engine = create_engine(DATABASE_URL)

def upgrade():
    try:
        with engine.connect() as conn:
            # conn.execute(text("ALTER TABLE recipes ADD COLUMN preparation_time_minutes INTEGER DEFAULT 0"))
            # conn.execute(text("ALTER TABLE recipes ADD COLUMN difficulty VARCHAR DEFAULT 'medium'"))
            # conn.execute(text("ALTER TABLE recipes ADD COLUMN notes TEXT"))
            conn.execute(text("ALTER TABLE recipes ADD COLUMN created_at DATETIME"))
            
            # 2. Add columns to cookbooks
            print("Migrating cookbooks...")
            conn.execute(text("ALTER TABLE cookbooks ADD COLUMN created_at DATETIME"))
            
            # 3. Create ratings table
            print("Creating ratings table...")
            conn.execute(text("""
            CREATE TABLE IF NOT EXISTS ratings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                score INTEGER,
                user_id INTEGER,
                recipe_id INTEGER,
                cookbook_id INTEGER,
                FOREIGN KEY(user_id) REFERENCES users(id),
                FOREIGN KEY(recipe_id) REFERENCES recipes(id),
                FOREIGN KEY(cookbook_id) REFERENCES cookbooks(id)
            )
            """))
            conn.commit()
            print("Migration successful.")
    except Exception as e:
        print(f"Migration failed details: {e}")

if __name__ == "__main__":
    upgrade()
