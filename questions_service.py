import re
import random
from pathlib import Path
from typing import Dict, List, Tuple

# Fonction de chargement des questions depuis un fichier SQL
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
	tuple_re = re.compile(r"\(?\s*(['\"])\s*(.*?)\s*\1\s*,\s*(['\"])\s*(.*?)\s*\3\s*\)?", re.DOTALL)

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

if __name__ == "__main__":
	# Test rapide si on exécute le module directement
	sql = Path(__file__).parent / 'Project 0' / 'Script-1.sql'
	try:
		data = load_questions_from_sql(sql)
		for table, items in data.items():
			print(f"{table}: {len(items)} questions")
	except Exception as e:
		print("Erreur lors du chargement des questions:", e)

# Fonction pour obtenir une question BOSS aléatoire par catégorie
def get_boss_question_for_category(categorie: str) -> Tuple[str, str] | None:
	"""Retourne une question aléatoire (q, a) pour une catégorie donnée.

	Les catégories sont mappées aux tables SQL:
	'1': quiz_algo, '2': quiz_metiers, '3': quiz_logique,
	'4': quiz_culture, '5': quiz_anglais
	"""
	# IMPORTANT: mapping aligné avec l'ordre affiché dans MAIN2.py
	# 1: Anglais, 2: Logique, 3: Algorithme, 4: Culture Générale, 5: Métiers
	cat_map = {
		'1': 'quiz_anglais',
		'2': 'quiz_logique',
		'3': 'quiz_algo',
		'4': 'quiz_culture',
		'5': 'quiz_metiers',
	}
	try:
		sql = Path(__file__).parent / 'Project 0' / 'Script-1.sql'
		tables = load_questions_from_sql(sql)
		table_name = cat_map.get(str(categorie))
		if not table_name:
			return None
		items = tables.get(table_name) or []
		if not items:
			return None
		return random.choice(items)
	except Exception:
		return None
