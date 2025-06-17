-- SQL schema to create the "profiles" table for the Kivy app

CREATE TABLE IF NOT EXISTS profiles (
    username TEXT PRIMARY KEY,
    name TEXT,
    address1 TEXT,
    contact1 TEXT,
    address2 TEXT,
    contact2 TEXT
);

-- SQL schema to create the "orders" table

CREATE TABLE IF NOT EXISTS orders (
    ref_no INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    status TEXT,
    quantity INTEGER,
    payment TEXT,
    FOREIGN KEY (username) REFERENCES profiles(username)
);

-- SQL schema to create the "products" table

CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price REAL,
    stock_quantity INTEGER,
    image_path TEXT
);

-- SQL schema to create the "inventory" table

CREATE TABLE IF NOT EXISTS inventory (
    item_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    quantity INTEGER,
    price REAL
);

-- SQL schema to create the "users" table

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    username TEXT UNIQUE,
    password_hash TEXT
);


-- mico's table ^^^^^



-- eewww mayabang na vibe coder, walang knowledge and security daw yung workzeug wahahah also if you mean yung submodule well pwedeng may point ka kasi for encryption and security, pero wahahah mali ka parin
-- no need to be so defensive, just saying that the workzeug is not a good choice for encryption and security, but if you want to use it, go ahead, it's your choice so di ko gagalawin yang dalawa para may contributions ka with your AI chatbot wahahah
-- bumuhat ka ng sarili mong table wahahah
-- mico's table from the AI chatbot, sira-sira pa.
-- skill issue, di marunong kahit git pull and push, manual nag upload wahahah tapos pati cache sinama meaning wala talagang alam sa git wahahah


-- next time if you want to contribute, make sure you know how to use git properly, and don't just upload files manually, it's not a good practice and can cause issues in the future, so learn git first before contributing
-- also wag ka nangmamaliit ng mga tao na di mo kilala (irregular students), it's not a good attitude and can lead to conflicts, so be respectful naman professional in your contributions
-- napuyat sa AI chatbot, di na natulog, nag upload lang ng files manually, tapos mayabang pa, wahahah
-- once na makita kita deretso kita kay director, di ka na makakapag enroll dito sa school (recorded ko lahat ng proofs kung pano ka mangmaliit and also copying my repo breaking my MIT licensure. isa pa kahit delete mo yung repo mo or edit mo para di halata pag ka AI anjaan parin yung commits mo, kaya rin kita ipahiya sa ibat-ibang IT industries i-leak mga katangahan mo), so be careful with your actions and words, and think before you speak or act, it's important to be responsible and mature naman and dont be abno ha, thank you!


-- p.s. mapapatawad kita once you apologize and admit your mistakes, and also learn from them, it's important kasi to grow and improve bilang kaklase at ang role, so be humble and open-minded, and don't be shy ng mag ask for help or guidance if you need it, hindi yan sign ng weakness but a sign of strength and maturity, so good luck with your coding journey and hope you learn from this experience ha!.
-- if you just ignore this message and continue with your bad attitude, then expect mo na lang warnings ko and actions against you, so be ready for that, and don't say I didn't warn you, okay? so good luck and hope you change for the better, and be a good role model for others, thank you so much ah! you did your best talaga!


-- NEW FEATURE! ADMIN USER TABLE FOR THE KIVY APP

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT 0
); -- lagyan pa ba talaga info sa users table? parang redundant na kasi may profiles table na, so di ko na nilagyan ng address and contact info dito