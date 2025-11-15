-- Table for players-- Table for players

CREATE TABLE IF NOT EXISTS player (CREATE TABLE IF NOT EXISTS player (

    id_player INTEGER PRIMARY KEY AUTOINCREMENT,    id_player INTEGER PRIMARY KEY AUTOINCREMENT,

    player_name TEXT NOT NULL UNIQUE,    player_name TEXT NOT NULL UNIQUE,

    player_score INTEGER DEFAULT 0    player_score INTEGER DEFAULT 0

););



-- Table for categories-- Table for categories

CREATE TABLE IF NOT EXISTS category (CREATE TABLE IF NOT EXISTS category (

    id INTEGER PRIMARY KEY AUTOINCREMENT,    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name_category TEXT NOT NULL    name_category TEXT NOT NULL

););



-- Table for questions-- Table for questions

CREATE TABLE IF NOT EXISTS questions (CREATE TABLE IF NOT EXISTS questions (

    id INTEGER PRIMARY KEY AUTOINCREMENT,    id INTEGER PRIMARY KEY AUTOINCREMENT,

    question TEXT NOT NULL,    question TEXT NOT NULL,

    reponse TEXT NOT NULL,    reponse TEXT NOT NULL,

    id_category INTEGER,    id_category INTEGER,

    is_boss BOOLEAN DEFAULT 0,    FOREIGN KEY (id_category) REFERENCES category(id)

    FOREIGN KEY (id_category) REFERENCES category(id));

);

-- Table for game sessions

-- Table for game sessionsCREATE TABLE IF NOT EXISTS game_session (

CREATE TABLE IF NOT EXISTS game_session (    id_session INTEGER PRIMARY KEY AUTOINCREMENT,

    id_session INTEGER PRIMARY KEY AUTOINCREMENT,    id_player INTEGER,

    id_player INTEGER,    score INTEGER DEFAULT 0,

    score INTEGER DEFAULT 0,    date_played DATETIME DEFAULT CURRENT_TIMESTAMP,

    date_played DATETIME DEFAULT CURRENT_TIMESTAMP,    FOREIGN KEY (id_player) REFERENCES player(id_player)

    FOREIGN KEY (id_player) REFERENCES player(id_player));

);

-- Table linking sessions and questions

-- Table linking sessions and questionsCREATE TABLE IF NOT EXISTS session_questions (

CREATE TABLE IF NOT EXISTS session_questions (    id_session INTEGER,

    id_session INTEGER,    id_question INTEGER,

    id_question INTEGER,    answered_correctly INTEGER,

    answered_correctly INTEGER,    FOREIGN KEY (id_session) REFERENCES game_session(id_session),

    FOREIGN KEY (id_session) REFERENCES game_session(id_session),    FOREIGN KEY (id_question) REFERENCES questions(id)

    FOREIGN KEY (id_question) REFERENCES questions(id));

);


-- Initial categories
INSERT OR IGNORE INTO category (id, name_category) VALUES
    (1, 'Anglais'),
    (2, 'Logique'),
    (3, 'Algorithme'),
    (4, 'Culture Générale'),
    (5, 'Métiers de l''informatique');