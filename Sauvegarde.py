import json


def sauvegarder_partie(etat, fichier="sauvegarde.json"):
    with open(fichier, "w", encoding="utf-8") as f:
        json.dump(etat, f, indent=4) 

def charger_progression(fichier="progression.json"):
    try:
        with open(fichier, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Aucune sauvegarde trouvée. Nouvelle partie.")
        return None 


def sauvegarder_score(nom: str, score: int, categorie: str, fichier: str = "sauvegarde.json"):
    """Ajoute une entrée (nom, score, categorie, timestamp) à un fichier JSON.

    Le fichier contient une liste d'objets. Si le fichier n'existe pas, il est créé.
    """
    import time
    entree = {
        "nom": nom,
        "score": score,
        "categorie": categorie,
        "timestamp": int(time.time())
    }

    try:
        with open(fichier, "r", encoding="utf-8") as f:
            data = json.load(f) or []
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append(entree)

    with open(fichier, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"Score sauvegardé pour {nom} : {score} (catégorie {categorie})")


def lire_scores(fichier: str = "sauvegarde.json"):
    """Retourne la liste d'entrées sauvegardées (ou [] si fichier absent)."""
    try:
        with open(fichier, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def afficher_leaderboard(top_n: int = 10, fichier: str = "sauvegarde.json"):
    """Affiche les meilleurs scores triés par score décroissant."""
    scores = lire_scores(fichier)
    if not scores:
        print("Aucun score enregistré.")
        return

    # Trier par score décroissant
    scores_sorted = sorted(scores, key=lambda e: e.get('score', 0), reverse=True)

    print(f"--- Top {top_n} des scores ---")
    for i, entry in enumerate(scores_sorted[:top_n], start=1):
        nom = entry.get('nom', 'Anonyme')
        score = entry.get('score', 0)
        categorie = entry.get('categorie', '?')
        ts = entry.get('timestamp', 0)
        from datetime import datetime
        dt = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S') if ts else 'N/A'
        print(f"{i}. {nom} — {score} pts — cat {categorie} — {dt}")


### SQLite helpers (migration) ###
import sqlite3
from pathlib import Path


def init_scores_db(db_path: str = None):
    """Create the scores DB and table if needed. Returns the path used."""
    if db_path is None:
        db_path = str(Path(__file__).parent / 'sauvegarde.db')
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                score INTEGER NOT NULL,
                categorie TEXT,
                timestamp INTEGER
            )
            """
        )
        conn.commit()
    finally:
        conn.close()
    return db_path


def sauvegarder_score_db(nom: str, score: int, categorie: str, db_path: str = None):
    """Insert a score into the SQLite DB. Initializes DB if missing."""
    if db_path is None:
        db_path = init_scores_db()
    else:
        init_scores_db(db_path)

    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        import time
        cur.execute(
            "INSERT INTO scores (nom, score, categorie, timestamp) VALUES (?, ?, ?, ?)",
            (nom, int(score), categorie, int(time.time())),
        )
        conn.commit()
    finally:
        conn.close()


def lire_scores_db(limit: int = 10, db_path: str = None):
    """Return top scores from the DB ordered by score DESC."""
    if db_path is None:
        db_path = str(Path(__file__).parent / 'sauvegarde.db')
    if not Path(db_path).exists():
        return []
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        cur.execute("SELECT nom, score, categorie, timestamp FROM scores ORDER BY score DESC LIMIT ?", (limit,))
        rows = cur.fetchall()
        return [
            {"nom": r[0], "score": r[1], "categorie": r[2], "timestamp": r[3]} for r in rows
        ]
    finally:
        conn.close()


def afficher_leaderboard_db(top_n: int = 10, db_path: str = None):
    rows = lire_scores_db(top_n, db_path)
    if not rows:
        print("Aucun score enregistré dans la DB.")
        return
    print(f"--- Top {top_n} (DB) ---")
    from datetime import datetime
    for i, entry in enumerate(rows, start=1):
        dt = datetime.fromtimestamp(entry.get('timestamp', 0)).strftime('%Y-%m-%d %H:%M:%S') if entry.get('timestamp') else 'N/A'
        print(f"{i}. {entry.get('nom')} — {entry.get('score')} pts — cat {entry.get('categorie')} — {dt}")          
    