-- SQL Schema generated from SQLAlchemy models

-- Table: users
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR NOT NULL UNIQUE,
    email VARCHAR NOT NULL UNIQUE,
    hashed_password VARCHAR NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_users_id ON users (id);
CREATE INDEX IF NOT EXISTS ix_users_username ON users (username);
CREATE INDEX IF NOT EXISTS ix_users_email ON users (email);

-- Table: cookbooks
CREATE TABLE IF NOT EXISTS cookbooks (
    id SERIAL PRIMARY KEY,
    title VARCHAR,
    description VARCHAR,
    pdf_url VARCHAR,
    owner_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS ix_cookbooks_id ON cookbooks (id);
CREATE INDEX IF NOT EXISTS ix_cookbooks_title ON cookbooks (title);

-- Table: recipes
CREATE TABLE IF NOT EXISTS recipes (
    id SERIAL PRIMARY KEY,
    title VARCHAR,
    ingredients JSONB,
    instructions TEXT,
    instructions_format VARCHAR DEFAULT 'numbered',
    country VARCHAR,
    type VARCHAR,
    image_url VARCHAR,
    preparation_time_minutes INTEGER DEFAULT 0,
    difficulty VARCHAR DEFAULT 'medium',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    owner_id INTEGER REFERENCES users(id),
    cookbook_id INTEGER REFERENCES cookbooks(id)
);
CREATE INDEX IF NOT EXISTS ix_recipes_id ON recipes (id);
CREATE INDEX IF NOT EXISTS ix_recipes_title ON recipes (title);

-- Table: ratings
CREATE TABLE IF NOT EXISTS ratings (
    id SERIAL PRIMARY KEY,
    score INTEGER,
    user_id INTEGER REFERENCES users(id),
    recipe_id INTEGER REFERENCES recipes(id),
    cookbook_id INTEGER REFERENCES cookbooks(id)
);
CREATE INDEX IF NOT EXISTS ix_ratings_id ON ratings (id);
