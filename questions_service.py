import sqlite3
import csv
from pathlib import Path
from typing import Dict, List, Tuple
import re


def load_questions_from_sql(sql_path: Path) -> Dict[str, List[Tuple[str, str]]]:
	"""Parse un fichier SQL et retourne un mapping table -> list[(question, answer)].

	Le parser est simple et cible les INSERT INTO statements présents dans
	`Project 0/Script-1.sql` où les valeurs sont des tuples (question, answer).
	"""
	if not sql_path.exists():
		raise FileNotFoundError(f"Fichier SQL introuvable: {sql_path}")

	text = sql_path.read_text(encoding='utf-8')

	# Rechercher tous les INSERT INTO table (...) VALUES ...; (multiligne possible)
	insert_re = re.compile(r"INSERT\s+INTO\s+(\w+)\s*\([^)]*\)\s*VALUES\s*(.+?);", re.IGNORECASE | re.DOTALL)

	# Rechercher des tuples de la forme ('question','answer') ou ["question","answer"]
	tuple_re = re.compile(r"\(?\s*(['\"])(.*?)\1\s*,\s*(['\"])(.*?)\3\s*\)?", re.DOTALL)

	result: Dict[str, List[Tuple[str, str]]] = {}

	for match in insert_re.finditer(text):
		table = match.group(1)
		values_blob = match.group(2)
		pairs: List[Tuple[str, str]] = []

		for tmatch in tuple_re.finditer(values_blob):
			q = tmatch.group(2).strip()
			a = tmatch.group(4).strip()
			pairs.append((q, a))

		if pairs:
			result[table] = pairs

	return result


def load_boss_questions(csv_path: Path | str = "boss_questions.csv") -> List[Tuple[str, str, str]]:
    """Charge les questions BOSS depuis le fichier CSV.
    
    Retourne une liste de tuples (categorie, question, reponse).
    Les questions BOSS sont plus difficiles et valent plus de points.
    """
    csv_path = Path(csv_path)
    if not csv_path.is_file():
        # Essayer dans le dossier parent
        parent_path = csv_path.parent.parent / csv_path.name
        if parent_path.is_file():
            csv_path = parent_path
        else:
            raise FileNotFoundError(f"Fichier boss_questions.csv introuvable dans {csv_path} ou {parent_path}")
    
    questions = []
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 3:
                    cat_id, question, reponse = row[0], row[1], row[2]
                    questions.append((cat_id, question, reponse))
        return questions
    except Exception as e:
        print(f"Erreur lors de la lecture des questions BOSS: {e}")
        return []

def get_boss_question_for_category(category_id: str) -> Tuple[str, str] | None:
    """Récupère une question BOSS pour la catégorie donnée.
    
    Args:
        category_id: L'ID de la catégorie (1-5)
    
    Returns:
        Un tuple (question, reponse) ou None si pas de question trouvée
    """
    try:
        questions = load_boss_questions()
        cat_questions = [
            (q, r) for c, q, r in questions 
            if c == str(category_id)
        ]
        if cat_questions:
            # Pour l'instant on prend la première question de la catégorie
            # On pourrait ajouter de l'aléatoire plus tard
            return cat_questions[0]
        return None
    except Exception:
        return None

if __name__ == "__main__":
    # Test rapide si on exécute le module directement
    sql = Path(__file__).parent / 'Script-1.sql'
    try:
        print("=== Questions normales ===")
        data = load_questions_from_sql(sql)
        for table, items in data.items():
            print(f"{table}: {len(items)} questions")
            
        print("\n=== Questions BOSS ===")
        boss_questions = load_boss_questions()
        by_category = {}
        for cat, q, _ in boss_questions:
            by_category.setdefault(cat, []).append(q)
        
        for cat, questions in by_category.items():
            print(f"Catégorie {cat}: {len(questions)} question(s) boss")
            
        # Test get_boss_question
        test_cat = "1"
        q = get_boss_question_for_category(test_cat)
        if q:
            print(f"\nQuestion BOSS exemple (cat {test_cat}):")
            print(f"Q: {q[0]}")
            print(f"R: {q[1]}")
    except Exception as e:
        print("Erreur lors du chargement des questions:", e)
