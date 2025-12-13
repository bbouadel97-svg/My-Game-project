import json
import time
from datetime import datetime
import sqlite3
from pathlib import Path


def sauvegarder_partie(etat, fichier="sauvegarde.json"):
    with open(fichier, "w", encoding="utf-8") as f:
        json.dump(etat, f, indent=4)

# Fonction de gestion de la progression
def sauvegarder_progression(nom: str, score: int, categories_jouees: list, bosses_defeated: dict = None, final_unlocked: bool = False, last_boss_questions: list = None, fichier: str = "progression.json"):
    """Sauvegarde l'état courant d'une campagne.

    - nom: nom du joueur
    - score: score actuel
    - categories_jouees: iterable des clés de catégories jouées
    - bosses_defeated: dict mapping key->bool indiquant si boss a été vaincu
    - final_unlocked: bool indiquant si le boss final est débloqué
    """
    if bosses_defeated is None:
        bosses_defeated = {}
    etat = {
        "nom": nom,
        "score": score,
        "categories_jouees": list(categories_jouees),
        "bosses_defeated": bosses_defeated,
        "final_unlocked": bool(final_unlocked),
        "last_boss_questions": last_boss_questions,
        "timestamp": int(time.time()),
    }
    with open(fichier, "w", encoding="utf-8") as f:
        json.dump(etat, f, ensure_ascii=False, indent=4)
    print(f"Progression sauvegardée pour {nom} (score: {score})")

# Fonction de chargement de la progression

def charger_progression(fichier: str = "progression.json") -> dict:
    """Charge la progression d'une campagne. Retourne None si pas de sauvegarde valide."""
    try:
        with open(fichier, "r", encoding="utf-8") as f:
            etat = json.load(f)
            if not isinstance(etat, dict):
                return None
            # Normalize fields and provide defaults
            etat.setdefault("score", 0)
            etat.setdefault("nom", "Anonyme")
            etat.setdefault("categories_jouees", [])
            etat.setdefault("bosses_defeated", {})
            etat.setdefault("final_unlocked", False)
            # Convert categories_jouees to a set for caller convenience
            etat["categories_jouees"] = set(str(c) for c in etat.get("categories_jouees", []))
            # Ensure bosses_defeated keys are strings
            etat["bosses_defeated"] = {str(k): bool(v) for k, v in etat.get("bosses_defeated", {}).items()}
            ts = etat.get("timestamp")
            if ts:
                dt = datetime.fromtimestamp(ts)
                print(f"Partie trouvée pour {etat['nom']} du {dt:%Y-%m-%d %H:%M}")
            else:
                print(f"Partie trouvée pour {etat['nom']}")
            return etat
    except (FileNotFoundError, json.JSONDecodeError):
        print("Aucune partie sauvegardée trouvée.")
        return None

#Fonctions de gestion des progressions
def reset_progression(fichier: str = "progression.json") -> bool:
    """Supprime le fichier de progression ou le réinitialise.

    Retourne True si une progression existante a été supprimée / réinitialisée.
    """
    p = Path(fichier)
    if not p.exists():
        return False
    try:
        # Choix simple: supprimer le fichier; il sera recréé lors de la prochaine sauvegarde
        p.unlink()
        print("Progression supprimée (reset).")
        return True
    except Exception:
        # fallback: vider le contenu
        try:
            with open(p, "w", encoding="utf-8") as f:
                f.write("{}")
            print("Progression réinitialisée (contenu vidé).")
            return True
        except Exception:
            return False

# Fonction de sauvegarde des scores
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

# Fonction de lecture des scores et affichage
def lire_scores(fichier: str = "sauvegarde.json"):
    """Retourne la liste d'entrées sauvegardées (ou [] si fichier absent)."""
    try:
        with open(fichier, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Fonction d'affichage du leaderboard et des scores
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

# FONCTIONS DE GESTION DES SCORES AVEC SQLITE
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

#Fonction de sauvegarde des scores dans la base de données

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

# Fonction de lecture des scores depuis la base de données

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

# Fonction d'affichage du leaderboard depuis la base de données

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