
import sqlite3

from pathlib import Path

# Chemin absolu vers la base de données (utiliser un raw string pour éviter les séquences d'échappement)
db_path = Path(r"C:\Users\User\OneDrive\Dokumenty\Spoot\My Game project\database.db")

if not db_path.exists():
    print(f"Attention: le fichier de base de données n'a pas été trouvé: {db_path}")
else:
    print(f"Utilisation de la base de données: {db_path}")

try:
    # Connexion à la base (convertir en str pour sqlite)
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    # Exemple : lire les questions de la table quiz_algo
    cursor.execute("SELECT question, answer FROM quiz_algo")

    questions = cursor.fetchall()

    # Affichage
    for q in questions:
        print("Question :", q[0])
        print("Réponse attendue :", "Vrai" if q[1] == 1 else "Faux")
        print("---")

except sqlite3.Error as e:
    print("Erreur SQLite:", e)

finally:
    # Fermer la connexion si elle a été ouverte
    try:
        conn.close()
    except NameError:
        pass

