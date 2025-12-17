--- création des tables dans la base de données SQL Server
-- pour les joueurs
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[player]') AND type in (N'U'))
BEGIN
    CREATE TABLE player (
        id_player INT PRIMARY KEY IDENTITY(1,1),
        player_name NVARCHAR(255) NOT NULL UNIQUE,
        player_score INT DEFAULT 0
    );
END
GO

-- pour les catégories de questions
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[category]') AND type in (N'U'))
BEGIN
    CREATE TABLE category (
        id INT PRIMARY KEY IDENTITY(1,1),
        name_category NVARCHAR(255) NOT NULL
    );
END
GO

-- pour les questions
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[questions]') AND type in (N'U'))
BEGIN
    CREATE TABLE questions (
        id INT PRIMARY KEY IDENTITY(1,1),
        question NVARCHAR(MAX) NOT NULL,
        reponse NVARCHAR(MAX) NOT NULL,
        id_category INT,
        is_boss BIT DEFAULT 0,
        FOREIGN KEY (id_category) REFERENCES category(id)
    );
END
GO

-- Pour les sessions de jeu
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[game_session]') AND type in (N'U'))
BEGIN
    CREATE TABLE game_session (
        id_session INT PRIMARY KEY IDENTITY(1,1),
        id_player INT,
        score INT DEFAULT 0,
        date_played DATETIME DEFAULT GETDATE(),
        FOREIGN KEY (id_player) REFERENCES player(id_player)
    );
END
GO

-- Pour joindre les sessions de jeu et les questions posées
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[session_questions]') AND type in (N'U'))
BEGIN
    CREATE TABLE session_questions (
        id_session INT,
        id_question INT,
        answered_correctly INT,
        FOREIGN KEY (id_session) REFERENCES game_session(id_session),
        FOREIGN KEY (id_question) REFERENCES questions(id)
    );
END
GO

-- Initial categories insertion
IF NOT EXISTS (SELECT * FROM category WHERE id = 1)
BEGIN
    INSERT INTO category (name_category) VALUES ('Anglais');
END

IF NOT EXISTS (SELECT * FROM category WHERE id = 2)
BEGIN
    INSERT INTO category (name_category) VALUES ('Logique');
END

IF NOT EXISTS (SELECT * FROM category WHERE id = 3)
BEGIN
    INSERT INTO category (name_category) VALUES ('Algorithme');
END

IF NOT EXISTS (SELECT * FROM category WHERE id = 4)
BEGIN
    INSERT INTO category (name_category) VALUES ('Culture Générale');
END

IF NOT EXISTS (SELECT * FROM category WHERE id = 5)
BEGIN
    INSERT INTO category (name_category) VALUES ('Métiers de l''informatique');
END
GO