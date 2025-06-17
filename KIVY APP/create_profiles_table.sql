CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    stock_quantity INTEGER NOT NULL,
    image_path TEXT
);

CREATE TABLE IF NOT EXISTS profiles (
    username TEXT PRIMARY KEY,
    name TEXT,
    address1 TEXT,
    contact1 TEXT,
    address2 TEXT,
    contact2 TEXT,
    FOREIGN KEY (username) REFERENCES users (username)
);

CREATE TABLE IF NOT EXISTS orders (
    ref_no INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    status TEXT DEFAULT 'Pending',
    quantity INTEGER,
    payment TEXT,
    FOREIGN KEY (username) REFERENCES users (username)
);